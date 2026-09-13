"""Entrypoint executed only on a disposable GitHub-hosted runner."""

from __future__ import annotations

import argparse
import base64
import gzip
import json
import re
from pathlib import Path

from .patch_safety import UnsafePatch, validate_unified_diff
from .sandbox import DockerVerifier
from .schemas import (
    CandidatePatch,
    PatchPolicy,
    SandboxConfig,
    VerificationResult,
)

SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")


def _decode_patch(value: str, *, max_bytes: int) -> str:
    try:
        payload = gzip.decompress(base64.b64decode(value, validate=True))
    except (ValueError, OSError) as exc:
        raise ValueError("patch payload is not valid gzip/base64") from exc
    if len(payload) > max_bytes:
        raise ValueError("decoded patch exceeds byte limit")
    return payload.decode("utf-8")


def run_remote_verification(
    *,
    root: Path,
    request_id: str,
    case_id: str,
    candidate_id: str,
    patch_b64: str,
) -> VerificationResult:
    if not all(SAFE_ID.fullmatch(value) for value in (request_id, case_id, candidate_id)):
        raise ValueError("request, case, or candidate ID is unsafe")
    case_root = (root / "benchmarks" / "cases" / case_id).resolve()
    cases_root = (root / "benchmarks" / "cases").resolve()
    if case_root.parent != cases_root:
        raise ValueError("case path escapes benchmark root")
    manifest = json.loads((case_root / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("id") != case_id:
        raise ValueError("case manifest identity mismatch")
    repository = case_root / manifest["repository"]
    hidden_tests = case_root / manifest["hidden_tests"]
    policy = PatchPolicy(max_bytes=40_000)
    verifier = DockerVerifier(SandboxConfig(), policy)
    if candidate_id == "baseline":
        result = verifier.baseline(repository)
    else:
        patch = _decode_patch(patch_b64, max_bytes=policy.max_bytes)
        changed = validate_unified_diff(patch, policy)
        allowed = {str(path).replace("\\", "/") for path in manifest["allowed_source_paths"]}
        disallowed = set(changed) - allowed
        if disallowed:
            raise UnsafePatch(
                "patch edits paths outside benchmark allowlist: " + ", ".join(sorted(disallowed))
            )
        candidate = CandidatePatch(
            candidate_id=candidate_id,
            rationale="remote verification payload",
            diff=patch,
        )
        result = verifier.verify(repository, candidate, hidden_tests=hidden_tests)
    return result.model_copy(update={"request_id": request_id})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--patch-file", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = run_remote_verification(
            root=args.root,
            request_id=args.request_id,
            case_id=args.case_id,
            candidate_id=args.candidate_id,
            patch_b64=args.patch_file.read_text(encoding="ascii").strip(),
        )
    except Exception as exc:
        result = VerificationResult(
            candidate_id=args.candidate_id,
            request_id=args.request_id,
            passed=False,
            exit_code=2,
            stderr=f"{type(exc).__name__}: {exc}",
        )
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
