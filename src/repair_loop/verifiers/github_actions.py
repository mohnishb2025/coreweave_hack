"""GitHub Actions-backed verifier for fully remote candidate execution."""

from __future__ import annotations

import base64
import gzip
import io
import json
import os
import threading
import time
import uuid
import zipfile
from collections.abc import Callable
from typing import Any

import httpx

from ..schemas import (
    CandidatePatch,
    GitHubActionsConfig,
    RepairRequest,
    VerificationResult,
)


class RemoteVerificationError(RuntimeError):
    pass


class GitHubActionsVerifier:
    """Dispatch and collect a schema-validated result from an ephemeral runner."""

    def __init__(
        self,
        config: GitHubActionsConfig,
        *,
        token: str | None = None,
        client: httpx.Client | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.config = config
        repository_env = os.getenv("GITHUB_REPOSITORY", "")
        env_owner, env_repository = (None, None)
        if "/" in repository_env:
            env_owner, env_repository = repository_env.split("/", 1)
        self.owner = config.owner or os.getenv("GITHUB_REPOSITORY_OWNER") or env_owner
        self.repository = config.repository or env_repository
        self.token = (
            token
            or os.getenv("REPAIR_LOOP_GITHUB_TOKEN")
            or os.getenv("GH_TOKEN")
            or os.getenv("GITHUB_TOKEN")
        )
        self._sleep = sleep
        self._cancelled = threading.Event()
        self._client = client or httpx.Client(
            base_url=config.api_url,
            follow_redirects=True,
            timeout=30,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}" if self.token else "",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    def cancel(self) -> None:
        self._cancelled.set()

    def baseline(self, request: RepairRequest) -> VerificationResult:
        return self._dispatch(request, candidate_id="baseline", patch="")

    def verify(self, request: RepairRequest, candidate: CandidatePatch) -> VerificationResult:
        return self._dispatch(request, candidate_id=candidate.candidate_id, patch=candidate.diff)

    def _require_ready(self) -> None:
        if os.getenv("REPAIR_LOOP_REMOTE_EXECUTION") != "1":
            raise RemoteVerificationError(
                "remote execution is disabled; set REPAIR_LOOP_REMOTE_EXECUTION=1 "
                "inside the Codespace only"
            )
        if not self.owner or not self.repository:
            raise RemoteVerificationError("GitHub owner/repository is not configured")
        if not self.token:
            raise RemoteVerificationError(
                "REPAIR_LOOP_GITHUB_TOKEN, GH_TOKEN, or GITHUB_TOKEN is required"
            )

    def _request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        try:
            response = self._client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            messages = {
                401: "GitHub authentication failed",
                403: "GitHub token lacks Actions permission or quota",
                404: "GitHub repository or workflow was not found",
                429: "GitHub API rate limit exceeded",
            }
            message = messages.get(
                status,
                "GitHub service error" if status >= 500 else "GitHub API request failed",
            )
            raise RemoteVerificationError(f"{message} (HTTP {status})") from exc
        except httpx.HTTPError as exc:
            raise RemoteVerificationError(f"GitHub connection failed: {exc}") from exc

    def _encode_patch(self, patch: str) -> str:
        encoded = base64.b64encode(gzip.compress(patch.encode("utf-8"))).decode("ascii")
        if len(encoded.encode("ascii")) > self.config.max_payload_bytes:
            raise RemoteVerificationError("compressed patch exceeds dispatch payload limit")
        return encoded

    def _dispatch(
        self, request: RepairRequest, *, candidate_id: str, patch: str
    ) -> VerificationResult:
        self._require_ready()
        self._cancelled.clear()
        request_id = uuid.uuid4().hex
        workflow_path = (
            f"/repos/{self.owner}/{self.repository}/actions/workflows/{self.config.workflow}"
        )
        self._request(
            "POST",
            f"{workflow_path}/dispatches",
            json={
                "ref": self.config.ref,
                "inputs": {
                    "request_id": request_id,
                    "case_id": request.case_id,
                    "candidate_id": candidate_id,
                    "patch_b64": self._encode_patch(patch),
                },
            },
        )
        run = self._wait_for_run(workflow_path, request_id)
        run_id = int(run["id"])
        completed = self._wait_for_completion(run_id, run)
        if completed.get("conclusion") != "success":
            raise RemoteVerificationError(
                f"verification workflow ended with {completed.get('conclusion')!r}: "
                f"{completed.get('html_url', '')}"
            )
        return self._download_result(
            run_id=run_id,
            request_id=request_id,
            candidate_id=candidate_id,
            run_url=str(completed.get("html_url", "")),
        )

    def _deadline(self) -> float:
        return time.monotonic() + self.config.timeout_seconds

    def _check_wait(self, deadline: float) -> None:
        if self._cancelled.is_set():
            raise RemoteVerificationError("remote verification cancelled")
        if time.monotonic() >= deadline:
            raise RemoteVerificationError("remote verification timed out")
        self._sleep(self.config.poll_interval_seconds)

    def _wait_for_run(self, workflow_path: str, request_id: str) -> dict[str, Any]:
        deadline = self._deadline()
        expected_title = f"repair-loop:{request_id}"
        while True:
            payload = self._request(
                "GET",
                f"{workflow_path}/runs",
                params={"event": "workflow_dispatch", "branch": self.config.ref, "per_page": 50},
            ).json()
            for run in payload.get("workflow_runs", []):
                if run.get("display_title") == expected_title:
                    return dict(run)
            self._check_wait(deadline)

    def _wait_for_completion(self, run_id: int, initial: dict[str, Any]) -> dict[str, Any]:
        deadline = self._deadline()
        run = initial
        while run.get("status") != "completed":
            self._check_wait(deadline)
            run = self._request(
                "GET",
                f"/repos/{self.owner}/{self.repository}/actions/runs/{run_id}",
            ).json()
        return dict(run)

    def _download_result(
        self,
        *,
        run_id: int,
        request_id: str,
        candidate_id: str,
        run_url: str,
    ) -> VerificationResult:
        artifacts_url = f"/repos/{self.owner}/{self.repository}/actions/runs/{run_id}/artifacts"
        artifacts = self._request("GET", artifacts_url).json().get("artifacts", [])
        expected_name = f"verification-{request_id}"
        artifact = next((item for item in artifacts if item.get("name") == expected_name), None)
        if artifact is None:
            raise RemoteVerificationError("verification result artifact is missing")
        archive = self._request(
            "GET",
            f"/repos/{self.owner}/{self.repository}/actions/artifacts/{artifact['id']}/zip",
        ).content
        try:
            with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
                result_data = json.loads(bundle.read("result.json"))
            result = VerificationResult.model_validate(result_data)
        except (KeyError, ValueError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
            raise RemoteVerificationError("verification artifact failed schema validation") from exc
        if result.request_id != request_id or result.candidate_id != candidate_id:
            raise RemoteVerificationError("verification artifact correlation mismatch")
        return result.model_copy(update={"run_url": run_url})
