"""Standalone integrity tests for the checked-in Repair Loop corpus."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

import pytest

ROOT = Path(__file__).parents[1]
CASES_ROOT = ROOT / "benchmarks" / "cases"
MANIFESTS = sorted(CASES_ROOT.glob("*/manifest.json"))
REQUIRED_KEYS = {
    "schema_version",
    "id",
    "language",
    "difficulty",
    "tags",
    "repository",
    "hidden_tests",
    "allowed_source_paths",
    "test_commands",
    "expected_failure",
}


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_corpus_has_exactly_fifteen_uniquely_named_cases():
    assert len(MANIFESTS) == 15
    manifests = [load_manifest(path) for path in MANIFESTS]
    assert len({manifest["id"] for manifest in manifests}) == 15
    assert all(path.parent.name == manifest["id"] for path, manifest in zip(MANIFESTS, manifests))


@pytest.mark.parametrize("manifest_path", MANIFESTS, ids=lambda path: path.parent.name)
def test_manifest_schema_and_layout(manifest_path: Path):
    manifest = load_manifest(manifest_path)
    case_root = manifest_path.parent
    repo = case_root / manifest["repository"]
    hidden = case_root / manifest["hidden_tests"]

    assert set(manifest) == REQUIRED_KEYS
    assert manifest["schema_version"] == 1
    assert manifest["language"] == "python"
    assert manifest["difficulty"] in {"easy", "medium", "hard"}
    assert manifest["tags"] and all(isinstance(tag, str) for tag in manifest["tags"])
    assert repo.is_dir()
    assert hidden.is_dir()
    assert hidden.parent == repo.parent and hidden not in repo.parents
    assert list((repo / "tests").glob("test_*.py"))
    assert list(hidden.glob("test_*.py"))

    allowed = manifest["allowed_source_paths"]
    assert allowed
    for relative in allowed:
        path = PurePosixPath(relative)
        assert not path.is_absolute() and ".." not in path.parts
        assert not relative.startswith("tests/")
        assert (repo / Path(*path.parts)).is_file()

    commands = manifest["test_commands"]
    assert set(commands) == {"public", "hidden"}
    assert commands["public"] == "python -m pytest -q tests"
    assert commands["hidden"] == "python -m pytest -q ../hidden_tests"
    assert manifest["expected_failure"]["nodeid"].startswith("tests/")
    assert manifest["expected_failure"]["reason"].strip()


def test_required_defect_categories_and_multifile_cases_are_present():
    manifests = [load_manifest(path) for path in MANIFESTS]
    tags = {tag for manifest in manifests for tag in manifest["tags"]}
    assert {"boundary", "mutable-state", "parsing", "async", "exceptions", "transformation"} <= tags
    assert sum("multi-file" in manifest["tags"] for manifest in manifests) >= 3
    for manifest in manifests:
        if "multi-file" in manifest["tags"]:
            assert len(manifest["allowed_source_paths"]) >= 2


@pytest.mark.parametrize("manifest_path", MANIFESTS, ids=lambda path: path.parent.name)
def test_buggy_repository_reproduces_declared_public_failure(manifest_path: Path):
    manifest = load_manifest(manifest_path)
    repo = manifest_path.parent / manifest["repository"]
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests"],
        cwd=repo,
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    output = (result.stdout + result.stderr).replace("\\", "/")
    assert result.returncode == 1, output
    assert manifest["expected_failure"]["nodeid"] in output, output
