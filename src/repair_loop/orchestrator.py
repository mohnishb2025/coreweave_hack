"""Deterministic orchestration for the multi-agent repair loop."""

from __future__ import annotations

import hashlib
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import weave

from .agents import QA, Critic, Diagnoser, Fixer, Manager
from .checkpoint import CheckpointStore
from .inference import InferenceClient, compact_context
from .observability import initialize_weave
from .patch_safety import UnsafePatch, validate_unified_diff
from .repository import repository_snapshot
from .schemas import (
    CandidatePatch,
    Critique,
    Diagnosis,
    Issue,
    LoopConfig,
    LoopState,
    RepairRequest,
    RepairResult,
    VerificationResult,
)
from .verifiers import GitHubActionsVerifier, Verifier


class RepairLoop:
    def __init__(
        self,
        config: LoopConfig,
        *,
        inference: InferenceClient | None = None,
        verifier: Verifier | None = None,
        checkpoints: CheckpointStore | None = None,
    ) -> None:
        self.config = config
        self.inference = inference or InferenceClient(
            model=config.model,
            project=config.project,
            temperature=config.temperature,
            seed=config.seed,
        )
        self.verifier = verifier or GitHubActionsVerifier(config.github_actions)
        self.checkpoints = checkpoints or CheckpointStore(config.checkpoint_dir)
        self.weave_client = initialize_weave(config.project)
        self._cancelled = Event()

    def cancel(self) -> None:
        """Request cancellation at the next safe stage boundary."""
        self._cancelled.set()
        self.verifier.cancel()

    def _role_model(self, role: str) -> str | None:
        return self.config.role_models.get(role, self.config.model)

    def _run_id(self, request: RepairRequest) -> str:
        material = "\0".join(
            [
                str(request.repository.resolve()),
                request.task,
                request.failure_output,
                self.config.variant,
                self.config.model or "",
            ]
        )
        return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]

    def _sync_usage(self, state: LoopState) -> None:
        state.usage = self.inference.usage
        self.config.budgets.assert_available(state.usage, candidates=len(state.candidates))

    def _ensure_capacity(self, state: LoopState, *, calls: int = 1, candidates: int = 0) -> None:
        if self._cancelled.is_set():
            raise RuntimeError("repair run cancelled")
        state.usage = self.inference.usage
        self.config.budgets.assert_available(
            state.usage,
            candidates=len(state.candidates),
            required_model_calls=calls,
            required_candidates=candidates,
        )

    def _save(self, state: LoopState) -> None:
        state.usage = self.inference.usage
        self.checkpoints.save(state)

    def _reflexive_request(self, request: RepairRequest, state: LoopState) -> RepairRequest:
        if not state.critiques and not state.verifications:
            return request
        feedback = "\n".join(
            [
                request.context,
                "PRIOR CRITIQUES:",
                *[item.model_dump_json() for item in state.critiques[-2:]],
                "PRIOR VERIFICATION:",
                *[item.model_dump_json() for item in state.verifications[-2:]],
                "PRIOR QA:",
                state.qa.model_dump_json() if state.qa else "none",
            ]
        )
        return request.model_copy(update={"context": feedback})

    @weave.op(name="repair_loop.run")
    def run(self, request: RepairRequest) -> RepairResult:
        request = request.model_copy(
            update={
                "context": compact_context(
                    [
                        request.context,
                        "VISIBLE REPOSITORY SNAPSHOT:\n" + repository_snapshot(request.repository),
                    ]
                )
            }
        )
        state = LoopState(run_id=self._run_id(request), phase="baseline", request=request)
        try:
            reproduce = getattr(self.verifier, "baseline", None)
            if callable(reproduce):
                baseline = reproduce(request)
                state.verifications.append(baseline)
                self._save(state)
                if baseline.passed:
                    state.phase = "failed"
                    state.error = "baseline public tests pass; no reproducible repair target"
                    self._save(state)
                    return RepairResult(run_id=state.run_id, success=False, state=state)
                request = request.model_copy(
                    update={
                        "failure_output": compact_context(
                            [request.failure_output, baseline.stdout, baseline.stderr],
                            max_chars=30_000,
                        )
                    }
                )
            state.phase = "diagnose"
            if self.config.use_diagnoser:
                self._ensure_capacity(state)
                state.diagnosis = Diagnoser(self.inference, self._role_model("diagnoser")).diagnose(
                    request
                )
            else:
                state.diagnosis = Diagnosis(
                    summary=request.task,
                    issues=[
                        Issue(
                            title="Unassisted diagnosis",
                            evidence=[request.failure_output],
                        )
                    ],
                )
            self._sync_usage(state)
            self._save(state)

            state.phase = "manage"
            self._ensure_capacity(state)
            state.plan = Manager(self.inference, self._role_model("manager")).plan(
                request, state.diagnosis
            )
            self._sync_usage(state)
            self._save(state)

            for iteration in range(1, self.config.max_iterations + 1):
                state.iteration = iteration
                current_request = self._reflexive_request(request, state)
                if iteration > 1 and self.config.use_diagnoser:
                    state.phase = "diagnose"
                    self._ensure_capacity(state, calls=2)
                    state.diagnosis = Diagnoser(
                        self.inference, self._role_model("diagnoser")
                    ).diagnose(current_request)
                    state.phase = "manage"
                    state.plan = Manager(self.inference, self._role_model("manager")).plan(
                        current_request, state.diagnosis
                    )
                    self._sync_usage(state)
                    self._save(state)
                state.phase = "fix"
                candidate_count = self.config.candidates_per_iteration
                self._ensure_capacity(state, calls=candidate_count, candidates=candidate_count)
                strategies = [
                    "minimal root-cause fix",
                    "defensive robust fix",
                    "alternative implementation with the smallest safe diff",
                    "edge-case-first repair",
                ]
                fixers = [
                    Fixer(
                        self.inference,
                        f"{iteration}-candidate-{index + 1}",
                        strategies[index],
                        self._role_model("fixer"),
                    )
                    for index in range(candidate_count)
                ]
                with ThreadPoolExecutor(
                    max_workers=candidate_count, thread_name_prefix="fixer"
                ) as pool:
                    futures = [
                        pool.submit(fixer.fix, current_request, state.diagnosis, state.plan)
                        for fixer in fixers
                    ]
                    candidates = [future.result() for future in futures]
                state.candidates.extend(candidates)
                self._sync_usage(state)

                critic = Critic(self.inference, self._role_model("critic"))
                viable: list[tuple[CandidatePatch, Critique, VerificationResult]] = []
                for candidate in candidates:
                    try:
                        changed_paths = validate_unified_diff(
                            candidate.diff, self.config.patch_policy
                        )
                        allowed = {path.replace("\\", "/") for path in request.allowed_source_paths}
                        disallowed = set(changed_paths) - allowed if allowed else set()
                        if disallowed:
                            raise UnsafePatch(
                                "patch edits paths outside the case allowlist: "
                                + ", ".join(sorted(disallowed))
                            )
                    except UnsafePatch as exc:
                        critique = Critique(
                            candidate_id=candidate.candidate_id,
                            score=0,
                            accepted=False,
                            concerns=[str(exc)],
                            reflection="Generate a smaller valid patch within the safety policy.",
                        )
                        state.critiques.append(critique)
                    else:
                        state.phase = "verify"
                        verification = self.verifier.verify(request, candidate)
                        state.verifications.append(verification)
                        self._save(state)
                        state.phase = "critic"
                        if self.config.use_critic:
                            self._ensure_capacity(state)
                            critique = critic.critique(
                                current_request,
                                state.diagnosis,
                                state.plan,
                                candidate,
                                verification,
                            )
                        else:
                            critique = Critique(
                                candidate_id=candidate.candidate_id,
                                score=100 if verification.passed else 0,
                                accepted=verification.passed,
                                concerns=[] if verification.passed else ["verification failed"],
                                reflection=(
                                    "Candidate passed deterministic verification."
                                    if verification.passed
                                    else "Use the verifier evidence in the next attempt."
                                ),
                            )
                        if critique.candidate_id != candidate.candidate_id:
                            critique = critique.model_copy(
                                update={"candidate_id": candidate.candidate_id}
                            )
                        state.critiques.append(critique)
                        if verification.passed and critique.accepted:
                            viable.append((candidate, critique, verification))
                    self._sync_usage(state)
                self._save(state)

                viable.sort(key=lambda item: (-item[1].score, item[0].candidate_id))
                for candidate, critique, verification in viable:
                    state.selected_candidate_id = candidate.candidate_id
                    state.phase = "qa"
                    self._ensure_capacity(state)
                    state.qa = QA(self.inference, self._role_model("qa")).assess(
                        {
                            "task": request.task,
                            "diagnosis": state.diagnosis.model_dump(),
                            "plan": state.plan.model_dump(),
                            "candidate": candidate.model_dump(),
                            "critique": critique.model_dump(),
                            "verification": verification.model_dump(),
                        }
                    )
                    self._sync_usage(state)
                    if state.qa.approved:
                        state.phase = "done"
                        self._save(state)
                        return RepairResult(
                            run_id=state.run_id,
                            success=True,
                            selected_patch=candidate,
                            state=state,
                        )
                self._save(state)

            state.phase = "failed"
            state.error = "no candidate passed critic, verification, and QA"
        except Exception as exc:
            state.phase = "failed"
            state.error = f"{type(exc).__name__}: {exc}"
        self._save(state)
        return RepairResult(run_id=state.run_id, success=False, state=state)

    def resume(self, run_id: str, max_attempts: int | None = None) -> RepairResult:
        """Resume a checkpoint, preserving its failure evidence as Reflexion context."""
        self._cancelled.clear()
        state = self.checkpoints.load(run_id)
        if state.phase == "done":
            selected = next(
                (
                    candidate
                    for candidate in state.candidates
                    if candidate.candidate_id == state.selected_candidate_id
                ),
                None,
            )
            return RepairResult(
                run_id=run_id,
                success=True,
                selected_patch=selected,
                state=state,
            )
        if state.request is None:
            raise ValueError(f"checkpoint {run_id!r} does not contain its repair request")
        if max_attempts is not None:
            self.config = self.config.model_copy(update={"max_iterations": max_attempts})
        resumed_request = self._reflexive_request(state.request, state)
        return self.run(resumed_request)
