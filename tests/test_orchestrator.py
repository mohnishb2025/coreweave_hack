import re
import threading
from pathlib import Path

from repair_loop.checkpoint import CheckpointStore
from repair_loop.orchestrator import RepairLoop
from repair_loop.schemas import (
    Budget,
    CandidatePatch,
    Critique,
    Diagnosis,
    Issue,
    LoopConfig,
    QAResult,
    RepairPlan,
    RepairRequest,
    Usage,
    VerificationResult,
)

PATCH = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ -1 +1 @@
-old
+new
"""


class FakeInference:
    def __init__(self) -> None:
        self._usage = Usage()
        self._lock = threading.Lock()

    @property
    def usage(self) -> Usage:
        with self._lock:
            return self._usage.model_copy()

    def complete_json(self, *, system: str, user: str, schema: type, model=None):
        with self._lock:
            self._usage.model_calls += 1
            self._usage.input_tokens += 2
            self._usage.output_tokens += 1
        if schema is Diagnosis:
            return Diagnosis(summary="root cause", issues=[Issue(title="bug")])
        if schema is RepairPlan:
            return RepairPlan(hypothesis="fix it", steps=["edit source"])
        if schema is CandidatePatch:
            match = re.search(r"Candidate ID must be '([^']+)'", user)
            candidate_id = match.group(1)
            return CandidatePatch(candidate_id=candidate_id, rationale="small fix", diff=PATCH)
        if schema is Critique:
            candidate_id = re.search(r'"candidate_id": "([^"]+)"', user).group(1)
            return Critique(
                candidate_id=candidate_id,
                score=90 if candidate_id.endswith("candidate-1") else 80,
                accepted=True,
                reflection="sound",
            )
        if schema is QAResult:
            return QAResult(approved=True, summary="all checks passed")
        raise AssertionError(schema)


class FakeVerifier:
    def __init__(self) -> None:
        self.seen: list[str] = []

    def cancel(self) -> None:
        pass

    def verify(self, request: RepairRequest, candidate: CandidatePatch) -> VerificationResult:
        self.seen.append(candidate.candidate_id)
        return VerificationResult(
            candidate_id=candidate.candidate_id,
            passed=True,
            exit_code=0,
            stdout="1 passed",
        )


def test_runs_two_fixers_and_selects_deterministically(tmp_path: Path) -> None:
    checkpoints = CheckpointStore(tmp_path / "checkpoints")
    verifier = FakeVerifier()
    loop = RepairLoop(
        LoopConfig(checkpoint_dir=tmp_path / "checkpoints"),
        inference=FakeInference(),
        verifier=verifier,
        checkpoints=checkpoints,
    )
    result = loop.run(RepairRequest(task="repair", repository=tmp_path, failure_output="failed"))
    assert result.success
    assert result.selected_patch.candidate_id == "1-candidate-1"
    assert len(result.state.candidates) == 2
    assert verifier.seen == ["1-candidate-1", "1-candidate-2"]
    assert checkpoints.load(result.run_id).phase == "done"


def test_run_ids_include_variant_and_model(tmp_path: Path) -> None:
    request = RepairRequest(task="repair", repository=tmp_path, failure_output="failed")
    first = RepairLoop(
        LoopConfig(variant="single_pass", model="cheap", checkpoint_dir=tmp_path / "a"),
        inference=FakeInference(),
        verifier=FakeVerifier(),
    )
    second = RepairLoop(
        LoopConfig(variant="full_team", model="cheap", checkpoint_dir=tmp_path / "b"),
        inference=FakeInference(),
        verifier=FakeVerifier(),
    )
    assert first._run_id(request) != second._run_id(request)


def test_budget_failure_is_checkpointed(tmp_path: Path) -> None:
    config = LoopConfig(
        checkpoint_dir=tmp_path / "checkpoints",
        budgets=Budget(max_model_calls=1),
    )
    loop = RepairLoop(config, inference=FakeInference(), verifier=FakeVerifier())
    result = loop.run(RepairRequest(task="repair", repository=tmp_path, failure_output="failed"))
    assert not result.success
    assert result.state.phase == "failed"
    assert "BudgetExceeded" in result.state.error


def test_case_path_allowlist_blocks_model_scope_creep(tmp_path: Path) -> None:
    verifier = FakeVerifier()
    loop = RepairLoop(
        LoopConfig(checkpoint_dir=tmp_path / "checkpoints"),
        inference=FakeInference(),
        verifier=verifier,
    )

    result = loop.run(
        RepairRequest(
            task="repair",
            repository=tmp_path,
            failure_output="failed",
            allowed_source_paths=["src/only_this.py"],
        )
    )

    assert not result.success
    assert verifier.seen == []
    assert all("outside the case allowlist" in item.concerns[0] for item in result.state.critiques)


def test_cancellation_stops_at_a_safe_boundary(tmp_path: Path) -> None:
    loop = RepairLoop(
        LoopConfig(checkpoint_dir=tmp_path / "checkpoints"),
        inference=FakeInference(),
        verifier=FakeVerifier(),
    )
    loop.cancel()

    result = loop.run(RepairRequest(task="repair", repository=tmp_path, failure_output="failed"))

    assert not result.success
    assert "cancelled" in result.state.error
