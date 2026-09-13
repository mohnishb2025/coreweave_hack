"""Typed handoffs shared by every repair-loop stage."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Annotated, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Issue(StrictModel):
    title: str
    evidence: list[str] = Field(default_factory=list)
    suspected_files: list[str] = Field(default_factory=list)
    severity: Severity = Severity.MEDIUM


class Diagnosis(StrictModel):
    summary: str
    issues: list[Issue]
    constraints: list[str] = Field(default_factory=list)


class RepairPlan(StrictModel):
    hypothesis: str
    steps: list[str]
    files_to_modify: list[str] = Field(default_factory=list)
    verification_commands: list[str] = Field(default_factory=list)


class CandidatePatch(StrictModel):
    candidate_id: str
    rationale: str
    diff: str
    expected_tests: list[str] = Field(default_factory=list)


class Critique(StrictModel):
    candidate_id: str
    score: Annotated[int, Field(ge=0, le=100)]
    accepted: bool
    concerns: list[str] = Field(default_factory=list)
    reflection: str


class VerificationResult(StrictModel):
    candidate_id: str
    passed: bool
    public_passed: bool = False
    hidden_passed: bool = False
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    duration_seconds: float = 0
    request_id: str | None = None
    run_url: str | None = None


class QAResult(StrictModel):
    approved: bool
    summary: str
    risks: list[str] = Field(default_factory=list)


class Usage(StrictModel):
    model_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0

    def add(self, other: Usage) -> None:
        self.model_calls += other.model_calls
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        self.cost_usd += other.cost_usd


class Budget(StrictModel):
    max_model_calls: int = Field(default=24, gt=0)
    max_input_tokens: int = Field(default=200_000, gt=0)
    max_output_tokens: int = Field(default=50_000, gt=0)
    max_candidates: int = Field(default=6, gt=0)
    max_cost_usd: float = Field(default=10.0, gt=0)

    def assert_available(
        self,
        usage: Usage,
        *,
        candidates: int = 0,
        required_model_calls: int = 0,
        required_candidates: int = 0,
    ) -> None:
        limits = (
            (
                usage.model_calls + required_model_calls,
                self.max_model_calls,
                "model calls",
            ),
            (usage.input_tokens, self.max_input_tokens, "input tokens"),
            (usage.output_tokens, self.max_output_tokens, "output tokens"),
            (candidates + required_candidates, self.max_candidates, "candidates"),
            (usage.cost_usd, self.max_cost_usd, "cost USD"),
        )
        for used, maximum, label in limits:
            if used > maximum:
                raise BudgetExceeded(f"{label} budget exhausted ({used}/{maximum})")


class BudgetExceeded(RuntimeError):
    pass


class PatchPolicy(StrictModel):
    max_bytes: int = Field(default=40_000, gt=0)
    max_changed_lines: int = Field(default=800, gt=0)
    max_files: int = Field(default=12, gt=0)
    forbidden_roots: tuple[str, ...] = ("tests",)


class SandboxConfig(StrictModel):
    image: str = "repair-loop-runner:latest"
    command: list[str] = Field(default_factory=lambda: ["python", "-m", "pytest", "-q"])
    hidden_command: list[str] = Field(
        default_factory=lambda: ["python", "-m", "pytest", "-q", "/hidden_tests"]
    )
    timeout_seconds: int = Field(default=600, gt=0)
    cpus: float = Field(default=2.0, gt=0)
    memory: str = "4g"
    pids_limit: int = Field(default=256, gt=0)


class GitHubActionsConfig(StrictModel):
    owner: str | None = None
    repository: str | None = None
    workflow: str = "verify-candidate.yml"
    ref: str = "main"
    api_url: str = "https://api.github.com"
    timeout_seconds: int = Field(default=900, gt=0)
    poll_interval_seconds: float = Field(default=5.0, gt=0)
    max_payload_bytes: int = Field(default=48_000, gt=0)


class LoopConfig(StrictModel):
    variant: str = "full_team"
    model: str | None = None
    role_models: dict[str, str] = Field(default_factory=dict)
    project: str | None = None
    temperature: float = Field(default=0.0, ge=0, le=2)
    seed: int = 17
    max_iterations: int = Field(default=3, gt=0)
    candidates_per_iteration: int = Field(default=2, ge=1, le=4)
    use_diagnoser: bool = True
    use_critic: bool = True
    budgets: Budget = Field(default_factory=Budget)
    patch_policy: PatchPolicy = Field(default_factory=PatchPolicy)
    sandbox: SandboxConfig = Field(default_factory=SandboxConfig)
    verifier: Literal["github_actions"] = "github_actions"
    github_actions: GitHubActionsConfig = Field(default_factory=GitHubActionsConfig)
    checkpoint_dir: Path = Path(".repair-loop/checkpoints")

    @classmethod
    def from_yaml(cls, path: str | Path) -> LoopConfig:
        return cls.model_validate(yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {})


class RepairRequest(StrictModel):
    case_id: str = "adhoc"
    task: str
    repository: Path
    failure_output: str
    context: str = ""
    hidden_tests: Path | None = None
    allowed_source_paths: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def repository_exists(self) -> RepairRequest:
        if not self.repository.is_dir():
            raise ValueError(f"repository does not exist: {self.repository}")
        if self.hidden_tests is not None and not self.hidden_tests.is_dir():
            raise ValueError(f"hidden tests do not exist: {self.hidden_tests}")
        return self


class LoopState(StrictModel):
    run_id: str
    phase: Literal[
        "baseline", "diagnose", "manage", "fix", "critic", "verify", "qa", "done", "failed"
    ]
    iteration: int = 0
    request: RepairRequest | None = None
    diagnosis: Diagnosis | None = None
    plan: RepairPlan | None = None
    candidates: list[CandidatePatch] = Field(default_factory=list)
    critiques: list[Critique] = Field(default_factory=list)
    verifications: list[VerificationResult] = Field(default_factory=list)
    qa: QAResult | None = None
    usage: Usage = Field(default_factory=Usage)
    selected_candidate_id: str | None = None
    error: str | None = None


class RepairResult(StrictModel):
    run_id: str
    success: bool
    selected_patch: CandidatePatch | None = None
    state: LoopState
