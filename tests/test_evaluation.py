from dataclasses import dataclass

from repair_loop.evaluation import (
    build_leaderboard,
    efficiency_scorer,
    evaluate_records,
    patch_quality_scorer,
    regression_scorer,
    repair_success_scorer,
    trace_operation,
    weave_url,
)


@dataclass
class Result:
    passed: bool
    attempts: int
    additions: int
    deletions: int
    regressions: list[str]
    cost_usd: float = 0.0


def test_scorers_accept_typed_objects() -> None:
    output = Result(True, 2, 3, 1, [], 0.25)
    assert repair_success_scorer(output)["repair_success"] is True
    assert regression_scorer(output) == {
        "regression_free": True,
        "regression_count": 0,
    }
    assert efficiency_scorer(output)["attempt_efficiency"] == 0.5
    assert patch_quality_scorer(output)["patch_quality"] > 0


def test_local_evaluation_and_leaderboard_are_offline(monkeypatch) -> None:
    monkeypatch.delenv("WANDB_API_KEY", raising=False)
    rows = evaluate_records(
        [
            {
                "case_id": "one",
                "model": "steady",
                "output": Result(True, 1, 1, 0, []),
            },
            {
                "case_id": "two",
                "model": "steady",
                "output": Result(False, 3, 0, 0, ["test_x"]),
            },
            {
                "case_id": "one",
                "model": "slow",
                "output": Result(True, 4, 2, 0, []),
            },
        ]
    )
    board = build_leaderboard(rows)
    assert [row["model"] for row in board] == ["slow", "steady"]
    assert board[1]["success_rate"] == 0.5


def test_trace_decorator_is_safe_without_weave() -> None:
    def operation(value: int) -> int:
        return value + 1

    decorated = trace_operation("test.operation")(operation)
    assert decorated(2) == 3


def test_weave_url(monkeypatch) -> None:
    monkeypatch.setenv("WANDB_ENTITY", "team")
    monkeypatch.setenv("WANDB_PROJECT", "repairs")
    assert weave_url(None, None) == "https://wandb.ai/team/repairs/weave"
    assert weave_url(None, "") == "https://wandb.ai/team/repairs/weave"
