"""Framework-light agent roles with explicit typed contracts."""

from __future__ import annotations

import json
from typing import Generic, TypeVar

import weave
from pydantic import BaseModel

from .inference import InferenceClient, compact_context
from .schemas import (
    CandidatePatch,
    Critique,
    Diagnosis,
    QAResult,
    RepairPlan,
    RepairRequest,
    VerificationResult,
)

T = TypeVar("T", bound=BaseModel)

COMMON_RULES = """You are one stage in a deterministic software repair pipeline.
Return only the requested JSON schema. Base every claim on supplied evidence. Do not edit tests,
invent command output, include secrets, or broaden scope. Prefer the smallest correct change."""


class Agent(Generic[T]):
    output_schema: type[T]
    role: str

    def __init__(self, inference: InferenceClient, model: str | None = None) -> None:
        self.inference = inference
        self.model = model

    def run(self, prompt: str) -> T:
        return self.inference.complete_json(
            system=f"{COMMON_RULES}\nYour role is {self.role}.",
            user=prompt,
            schema=self.output_schema,
            model=self.model,
        )


class Diagnoser(Agent[Diagnosis]):
    output_schema = Diagnosis
    role = "Diagnoser: identify root causes from the task, failure output, and repository context"

    @weave.op()
    def diagnose(self, request: RepairRequest) -> Diagnosis:
        return self.run(
            compact_context(
                [
                    f"TASK:\n{request.task}",
                    f"FAILURE OUTPUT:\n{request.failure_output}",
                    f"REPOSITORY CONTEXT:\n{request.context}",
                ]
            )
        )


class Manager(Agent[RepairPlan]):
    output_schema = RepairPlan
    role = "Manager: produce a minimal ordered implementation and verification plan"

    @weave.op()
    def plan(self, request: RepairRequest, diagnosis: Diagnosis) -> RepairPlan:
        return self.run(
            compact_context(
                [
                    f"TASK:\n{request.task}",
                    f"DIAGNOSIS:\n{diagnosis.model_dump_json(indent=2)}",
                    f"REPOSITORY CONTEXT:\n{request.context}",
                ]
            )
        )


class Fixer(Agent[CandidatePatch]):
    output_schema = CandidatePatch
    role = "Fixer: create a complete valid unified diff implementing the plan"

    def __init__(
        self,
        inference: InferenceClient,
        candidate_id: str,
        strategy: str,
        model: str | None = None,
    ) -> None:
        super().__init__(inference, model)
        self.candidate_id = candidate_id
        self.strategy = strategy

    @weave.op()
    def fix(self, request: RepairRequest, diagnosis: Diagnosis, plan: RepairPlan) -> CandidatePatch:
        candidate = self.run(
            compact_context(
                [
                    f"Candidate ID must be {self.candidate_id!r}. Strategy: {self.strategy}.",
                    f"TASK:\n{request.task}",
                    f"DIAGNOSIS:\n{diagnosis.model_dump_json(indent=2)}",
                    f"PLAN:\n{plan.model_dump_json(indent=2)}",
                    f"REPOSITORY CONTEXT:\n{request.context}",
                    "Emit a git-compatible unified diff in the diff field.",
                ]
            )
        )
        if candidate.candidate_id != self.candidate_id:
            candidate = candidate.model_copy(update={"candidate_id": self.candidate_id})
        return candidate


class Critic(Agent[Critique]):
    output_schema = Critique
    role = "Critic/Reflexion: find correctness, scope, safety, and verification weaknesses"

    @weave.op()
    def critique(
        self,
        request: RepairRequest,
        diagnosis: Diagnosis,
        plan: RepairPlan,
        candidate: CandidatePatch,
        verification: VerificationResult,
    ) -> Critique:
        return self.run(
            compact_context(
                [
                    f"TASK:\n{request.task}",
                    f"DIAGNOSIS:\n{diagnosis.model_dump_json(indent=2)}",
                    f"PLAN:\n{plan.model_dump_json(indent=2)}",
                    f"CANDIDATE:\n{candidate.model_dump_json(indent=2)}",
                    f"EXECUTABLE VERIFICATION:\n{verification.model_dump_json(indent=2)}",
                    "Set candidate_id exactly to the supplied candidate's ID.",
                ]
            )
        )


class QA(Agent[QAResult]):
    output_schema = QAResult
    role = "QA: make the final evidence-based release decision"

    @weave.op()
    def assess(self, payload: dict[str, object]) -> QAResult:
        return self.run("FINAL EVIDENCE:\n" + json.dumps(payload, indent=2, default=str))
