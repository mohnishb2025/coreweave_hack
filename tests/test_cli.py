import json
from pathlib import Path

from typer.testing import CliRunner

from repair_loop import cli

runner = CliRunner()


class FakeOrchestrator:
    def __init__(self, **kwargs):
        self.options = kwargs

    def repair(self, **kwargs):
        return {
            "passed": True,
            "attempts": 1,
            "patch": "diff",
            "case_id": kwargs.get("case_id"),
            "model": kwargs.get("model"),
        }

    def resume(self, **kwargs):
        return {"passed": True, "run_id": kwargs["run_id"]}


def test_help_lists_presentation_commands() -> None:
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0
    for command in ("models", "cases", "repair", "benchmark", "resume"):
        assert command in result.stdout


def test_models_discovers_profiles(tmp_path: Path) -> None:
    (tmp_path / "fast.yaml").write_text("model: fast", encoding="utf-8")
    result = runner.invoke(cli.app, ["models", "--directory", str(tmp_path)])
    assert result.exit_code == 0
    assert "fast" in result.stdout


def test_repair_uses_core_adapter_and_prints_weave_url(monkeypatch) -> None:
    monkeypatch.setattr(cli, "_orchestrator_class", lambda: FakeOrchestrator)
    monkeypatch.setattr(cli, "_repair_request", lambda case: {"id": case})
    result = runner.invoke(
        cli.app,
        [
            "repair",
            "case-1",
            "--model",
            "model-a",
            "--entity",
            "team",
            "--project",
            "repairs",
        ],
    )
    assert result.exit_code == 0
    assert '"passed": true' in result.stdout
    assert "https://wandb.ai/team/repairs/weave" in result.stdout


def test_benchmark_writes_offline_leaderboard(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(cli, "_orchestrator_class", lambda: FakeOrchestrator)
    monkeypatch.setattr(cli, "_repair_request", lambda case: {"id": case})
    cases = tmp_path / "cases.json"
    output = tmp_path / "board.json"
    cases.write_text(json.dumps([{"id": "case-1"}]), encoding="utf-8")

    result = runner.invoke(
        cli.app,
        [
            "benchmark",
            str(cases),
            "--model",
            "model-a",
            "--output",
            str(output),
        ],
    )
    assert result.exit_code == 0
    assert output.exists()
    assert json.loads(output.read_text(encoding="utf-8"))[0]["success_rate"] == 1.0


def test_missing_core_is_a_clean_cli_error(monkeypatch) -> None:
    def unavailable():
        raise RuntimeError("core unavailable")

    monkeypatch.setattr(cli, "_orchestrator_class", unavailable)
    result = runner.invoke(cli.app, ["resume", "run-1"])
    assert result.exit_code == 1
    assert getattr(result.exception, "message", "") == "core unavailable"
