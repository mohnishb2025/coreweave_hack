import io
import json
import zipfile
from pathlib import Path

import httpx
import pytest

from repair_loop.schemas import (
    CandidatePatch,
    GitHubActionsConfig,
    RepairRequest,
)
from repair_loop.verifiers.github_actions import (
    GitHubActionsVerifier,
    RemoteVerificationError,
)


def _archive(payload: dict) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as bundle:
        bundle.writestr("result.json", json.dumps(payload))
    return stream.getvalue()


def test_dispatches_polls_and_validates_artifact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "POST":
            captured.update(json.loads(request.content))
            return httpx.Response(204, request=request)
        request_id = captured["inputs"]["request_id"]
        candidate_id = captured["inputs"]["candidate_id"]
        if path.endswith("/workflows/verify-candidate.yml/runs"):
            return httpx.Response(
                200,
                request=request,
                json={
                    "workflow_runs": [
                        {
                            "id": 7,
                            "display_title": f"repair-loop:{request_id}",
                            "status": "completed",
                            "conclusion": "success",
                            "html_url": "https://github.test/actions/runs/7",
                        }
                    ]
                },
            )
        if path.endswith("/actions/runs/7/artifacts"):
            return httpx.Response(
                200,
                request=request,
                json={"artifacts": [{"id": 9, "name": f"verification-{request_id}"}]},
            )
        if path.endswith("/actions/artifacts/9/zip"):
            return httpx.Response(
                200,
                request=request,
                content=_archive(
                    {
                        "candidate_id": candidate_id,
                        "request_id": request_id,
                        "passed": True,
                        "public_passed": True,
                        "hidden_passed": True,
                        "exit_code": 0,
                        "stdout": "1 passed",
                        "stderr": "",
                        "duration_seconds": 1.0,
                        "run_url": None,
                    }
                ),
            )
        raise AssertionError(path)

    monkeypatch.setenv("REPAIR_LOOP_REMOTE_EXECUTION", "1")
    client = httpx.Client(
        base_url="https://api.github.test",
        transport=httpx.MockTransport(handler),
    )
    verifier = GitHubActionsVerifier(
        GitHubActionsConfig(owner="owner", repository="repo"),
        token="test-token",
        client=client,
        sleep=lambda _: None,
    )
    request = RepairRequest(
        case_id="01_clamp_boundary",
        task="repair",
        repository=tmp_path,
        failure_output="failed",
    )
    candidate = CandidatePatch(
        candidate_id="1-candidate-1",
        rationale="fix",
        diff="small patch",
    )

    result = verifier.verify(request, candidate)

    assert result.passed
    assert result.run_url == "https://github.test/actions/runs/7"
    assert captured["inputs"]["case_id"] == "01_clamp_boundary"


def test_owner_and_repository_are_parsed_from_github_repository(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY_OWNER", raising=False)
    monkeypatch.setenv("GITHUB_REPOSITORY", "mohnishb2025/coreweave_hack")
    verifier = GitHubActionsVerifier(GitHubActionsConfig(), token="test-token")
    assert verifier.owner == "mohnishb2025"
    assert verifier.repository == "coreweave_hack"


def test_remote_execution_is_off_by_default(tmp_path: Path) -> None:
    verifier = GitHubActionsVerifier(
        GitHubActionsConfig(owner="owner", repository="repo"),
        token="test-token",
    )
    request = RepairRequest(
        case_id="case",
        task="repair",
        repository=tmp_path,
        failure_output="failed",
    )

    with pytest.raises(RemoteVerificationError, match="disabled"):
        verifier.baseline(request)
