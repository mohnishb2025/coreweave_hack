from pathlib import Path

from repair_loop.repository import repository_snapshot


def test_snapshot_includes_source_and_tests_but_excludes_secrets(tmp_path: Path) -> None:
    (tmp_path / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_module.py").write_text("def test_value(): pass\n", encoding="utf-8")
    (tmp_path / ".env").write_text("WANDB_API_KEY=secret\n", encoding="utf-8")

    snapshot = repository_snapshot(tmp_path)

    assert "--- module.py ---" in snapshot
    assert "--- tests/test_module.py ---" in snapshot
    assert "WANDB_API_KEY" not in snapshot
