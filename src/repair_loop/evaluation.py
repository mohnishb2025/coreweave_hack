"""Offline-safe evaluation and Weave integration helpers.

The core repair engine is intentionally not imported here.  This module accepts
plain dictionaries, dataclasses, or Pydantic models so it can sit on top of the
typed schemas without coupling the presentation layer to their implementation.
"""

from __future__ import annotations

import inspect
import json
import os
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


def _mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    if is_dataclass(value):
        return asdict(value)
    for method in ("model_dump", "dict"):
        dump = getattr(value, method, None)
        if callable(dump):
            return dict(dump())
    return dict(vars(value)) if hasattr(value, "__dict__") else {"value": value}


def _get(value: Any, *names: str, default: Any = None) -> Any:
    data = _mapping(value)
    for name in names:
        if name in data:
            return data[name]
    return default


def _number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _state(output: Any) -> dict[str, Any]:
    return _mapping(_get(output, "state", default={}))


def repair_success_scorer(output: Any, **_: Any) -> dict[str, Any]:
    """Score whether the candidate passed its validation suite."""
    passed = _get(output, "passed", "success", "tests_passed", default=False)
    if isinstance(passed, (int, float)) and not isinstance(passed, bool):
        passed = passed > 0
    return {"repair_success": bool(passed)}


def regression_scorer(output: Any, **_: Any) -> dict[str, Any]:
    """Reward candidates with no newly failing tests."""
    state = _state(output)
    regressions = _get(output, "regressions", "new_failures", "regression_count", default=0)
    count = (
        len(regressions)
        if isinstance(regressions, Sequence) and not isinstance(regressions, (str, bytes))
        else int(_number(regressions))
    )
    verifications = state.get("verifications", [])
    if verifications and repair_success_scorer(output)["repair_success"]:
        latest = _mapping(verifications[-1])
        count = 0 if latest.get("hidden_passed", latest.get("passed", False)) else 1
    return {"regression_free": count == 0, "regression_count": count}


def efficiency_scorer(output: Any, **_: Any) -> dict[str, float]:
    """Score useful repairs per attempt and expose cost/latency diagnostics."""
    state = _state(output)
    usage = _mapping(state.get("usage", {}))
    attempts = max(
        1.0,
        _number(
            _get(output, "attempts", "iterations", default=state.get("iteration", 1)),
            1,
        ),
    )
    success = repair_success_scorer(output)["repair_success"]
    return {
        "attempt_efficiency": (1.0 / attempts) if success else 0.0,
        "attempts": attempts,
        "cost_usd": _number(_get(output, "cost_usd", "cost", default=usage.get("cost_usd", 0))),
        "latency_seconds": _number(_get(output, "latency_seconds", "duration_seconds", default=0)),
    }


def patch_quality_scorer(output: Any, **_: Any) -> dict[str, float]:
    """Prefer successful, focused patches; never reward empty patches."""
    selected = _mapping(_get(output, "selected_patch", default={}))
    additions = _number(_get(output, "additions", "lines_added", default=0))
    deletions = _number(_get(output, "deletions", "lines_deleted", default=0))
    changed = additions + deletions
    patch = _get(output, "patch", "diff", default=selected.get("diff", ""))
    if patch and changed == 0:
        changed = sum(
            1
            for line in str(patch).splitlines()
            if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
        )
    has_patch = bool(patch) or changed > 0
    success = repair_success_scorer(output)["repair_success"]
    score = (1.0 / (1.0 + changed / 50.0)) if success and has_patch else 0.0
    return {"patch_quality": score, "changed_lines": changed}


DEFAULT_SCORERS: tuple[Callable[..., dict[str, Any]], ...] = (
    repair_success_scorer,
    regression_scorer,
    efficiency_scorer,
    patch_quality_scorer,
)


class LLMQualityScore(BaseModel):
    maintainability: float = Field(ge=0, le=1)
    explanation_quality: float = Field(ge=0, le=1)
    concerns: list[str] = Field(default_factory=list)


def llm_patch_quality_scorer(
    output: Any,
    *,
    inference: Any,
    model: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Optional model-based scorer; deterministic gates remain authoritative."""
    selected = _mapping(_get(output, "selected_patch", default={}))
    score = inference.complete_json(
        system=(
            "You are an independent code-review scorer. Judge only maintainability "
            "and explanation quality; never claim tests passed."
        ),
        user=json.dumps(selected, indent=2, default=str),
        schema=LLMQualityScore,
        model=model,
    )
    return score.model_dump()


@dataclass(frozen=True)
class EvaluationRow:
    case_id: str
    model: str
    variant: str
    scores: dict[str, Any]
    output: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "model": self.model,
            "variant": self.variant,
            **self.scores,
            "output": self.output,
        }


def evaluate_records(
    records: Iterable[Any],
    scorers: Sequence[Callable[..., Mapping[str, Any]]] = DEFAULT_SCORERS,
) -> list[dict[str, Any]]:
    """Evaluate existing outputs locally without contacting Weights & Biases."""
    rows: list[dict[str, Any]] = []
    for record in records:
        output = _get(record, "output", "result", default=record)
        scores: dict[str, Any] = {}
        for scorer in scorers:
            scores.update(scorer(output=output))
        row = EvaluationRow(
            case_id=str(_get(record, "case_id", "id", default="unknown")),
            model=str(_get(record, "model", "model_id", default="unknown")),
            variant=str(_get(record, "variant", default="unknown")),
            scores=scores,
            output=_mapping(output),
        )
        rows.append(row.as_dict())
    return rows


def build_leaderboard(rows: Iterable[Any]) -> list[dict[str, Any]]:
    """Aggregate scored rows by model, ordered by success then efficiency."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        item = _mapping(row)
        key = f"{item.get('variant', 'unknown')}::{item.get('model', 'unknown')}"
        grouped.setdefault(key, []).append(item)

    board: list[dict[str, Any]] = []
    for key, items in grouped.items():
        variant, model = key.split("::", 1)
        count = len(items)
        successes = sum(bool(item.get("repair_success", False)) for item in items)
        board.append(
            {
                "model": model,
                "variant": variant,
                "cases": count,
                "success_rate": successes / count if count else 0.0,
                "avg_attempts": sum(_number(i.get("attempts"), 1) for i in items) / count,
                "avg_cost_usd": sum(_number(i.get("cost_usd")) for i in items) / count,
                "avg_latency_seconds": sum(_number(i.get("latency_seconds")) for i in items)
                / count,
            }
        )
    return sorted(
        board,
        key=lambda row: (-row["success_rate"], row["avg_attempts"], row["avg_cost_usd"]),
    )


def save_leaderboard(rows: Iterable[Any], destination: str | Path) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_leaderboard(rows), indent=2), encoding="utf-8")
    return path


def weave_url(entity: str | None, project: str | None) -> str | None:
    entity = entity or os.getenv("WANDB_ENTITY")
    project = project or os.getenv("WANDB_PROJECT")
    if not entity or not project:
        return None
    return f"https://wandb.ai/{entity}/{project}/weave"


def trace_operation(name: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorate with ``weave.op`` when installed, otherwise return unchanged."""

    def decorate(function: Callable[..., Any]) -> Callable[..., Any]:
        try:
            import weave  # type: ignore

            op = weave.op(name=name) if name else weave.op()
            return op(function)
        except (ImportError, RuntimeError):
            return function

    return decorate


async def run_weave_evaluation(
    dataset: Iterable[Mapping[str, Any]],
    model: Any,
    *,
    project: str | None = None,
    scorers: Sequence[Callable[..., Mapping[str, Any]]] = DEFAULT_SCORERS,
) -> Any:
    """Run a Weave Evaluation, importing and initializing Weave only on demand."""
    try:
        import weave  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Install the optional 'weave' dependency to upload evaluations") from exc

    if project:
        weave.init(project)
    evaluation = weave.Evaluation(dataset=list(dataset), scorers=list(scorers))
    result = evaluation.evaluate(model)
    return await result if inspect.isawaitable(result) else result


def publish_weave_leaderboard(
    evaluation: Any,
    *,
    name: str = "Repair Loop Leaderboard",
    scorer_name: str = "repair_success_scorer",
    summary_metric_path: str = "true_fraction",
) -> Any:
    """Publish a Weave leaderboard backed by an existing Evaluation object."""
    try:
        import weave
        from weave.flow import leaderboard
        from weave.trace.ref_util import get_ref
    except ImportError as exc:
        raise RuntimeError("Install weave to publish a leaderboard") from exc

    evaluation_ref = get_ref(evaluation)
    if evaluation_ref is None:
        raise ValueError("evaluation must be published before creating a leaderboard")
    board = leaderboard.Leaderboard(
        name=name,
        description="Compare repair-loop models and orchestration variants.",
        columns=[
            leaderboard.LeaderboardColumn(
                evaluation_object_ref=evaluation_ref.uri(),
                scorer_name=scorer_name,
                summary_metric_path=summary_metric_path,
            )
        ],
    )
    return weave.publish(board)
