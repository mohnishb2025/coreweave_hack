from pathlib import Path

import pytest
from pydantic import ValidationError

from repair_loop.schemas import Budget, BudgetExceeded, LoopConfig, RepairRequest, Usage


def test_request_requires_existing_repository(tmp_path: Path) -> None:
    request = RepairRequest(task="fix", repository=tmp_path, failure_output="boom")
    assert request.repository == tmp_path
    with pytest.raises(ValidationError):
        RepairRequest(task="fix", repository=tmp_path / "missing", failure_output="boom")


def test_yaml_config_is_typed(tmp_path: Path) -> None:
    path = tmp_path / "config.yaml"
    path.write_text("max_iterations: 2\nbudgets:\n  max_model_calls: 5\n", encoding="utf-8")
    config = LoopConfig.from_yaml(path)
    assert config.max_iterations == 2
    assert config.budgets.max_model_calls == 5


def test_budget_supports_projected_usage() -> None:
    budget = Budget(max_model_calls=2)
    budget.assert_available(Usage(model_calls=1), required_model_calls=1)
    with pytest.raises(BudgetExceeded):
        budget.assert_available(Usage(model_calls=1), required_model_calls=2)
