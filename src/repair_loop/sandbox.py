"""Isolated Docker verification and its command-line entry point."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from .patch_safety import validate_unified_diff
from .schemas import CandidatePatch, PatchPolicy, SandboxConfig, VerificationResult


class DockerVerifier:
    def __init__(self, config: SandboxConfig, policy: PatchPolicy | None = None) -> None:
        self.config = config
        self.policy = policy or PatchPolicy()

    def baseline(self, repository: Path) -> VerificationResult:
        """Reproduce the public failure before spending inference tokens."""
        started = time.monotonic()
        try:
            completed = subprocess.run(
                self.docker_command(repository),
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return VerificationResult(
                candidate_id="baseline",
                passed=False,
                public_passed=False,
                hidden_passed=False,
                exit_code=124,
                stdout=(exc.stdout or "")[-50_000:],
                stderr=((exc.stderr or "") + "\nbaseline verification timed out")[-50_000:],
                duration_seconds=time.monotonic() - started,
            )
        return VerificationResult(
            candidate_id="baseline",
            passed=completed.returncode == 0,
            public_passed=completed.returncode == 0,
            hidden_passed=False,
            exit_code=completed.returncode,
            stdout=completed.stdout[-50_000:],
            stderr=completed.stderr[-50_000:],
            duration_seconds=time.monotonic() - started,
        )

    def docker_command(
        self,
        repository: Path,
        *,
        command: list[str] | None = None,
        hidden_tests: Path | None = None,
    ) -> list[str]:
        docker_args = [
            "docker",
            "run",
            "--rm",
            "--network",
            "none",
            "--cpus",
            str(self.config.cpus),
            "--memory",
            self.config.memory,
            "--pids-limit",
            str(self.config.pids_limit),
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--user",
            "65534:65534",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=256m",
            "--mount",
            f"type=bind,src={repository.resolve()},dst=/workspace,readonly",
            "--env",
            "PYTHONPATH=/workspace",
        ]
        if hidden_tests is not None:
            docker_args.extend(
                [
                    "--mount",
                    f"type=bind,src={hidden_tests.resolve()},dst=/hidden_tests,readonly",
                ]
            )
        return [
            *docker_args,
            "--workdir",
            "/workspace",
            self.config.image,
            *(command or self.config.command),
        ]

    def verify(
        self,
        repository: Path,
        candidate: CandidatePatch,
        *,
        hidden_tests: Path | None = None,
    ) -> VerificationResult:
        validate_unified_diff(candidate.diff, self.policy)
        started = time.monotonic()
        with tempfile.TemporaryDirectory(prefix="repair-loop-") as temporary:
            checkout = Path(temporary) / "repo"
            shutil.copytree(
                repository,
                checkout,
                ignore=shutil.ignore_patterns(".git", ".repair-loop", ".venv", "__pycache__"),
            )
            patch_path = Path(temporary) / "candidate.diff"
            patch_path.write_text(candidate.diff, encoding="utf-8")
            checked = subprocess.run(
                ["git", "apply", "--check", str(patch_path)],
                cwd=checkout,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            if checked.returncode != 0:
                return VerificationResult(
                    candidate_id=candidate.candidate_id,
                    passed=False,
                    exit_code=checked.returncode,
                    stderr=f"git apply --check failed:\n{checked.stderr}",
                    duration_seconds=time.monotonic() - started,
                )
            subprocess.run(
                ["git", "apply", str(patch_path)],
                cwd=checkout,
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )
            try:
                public = subprocess.run(
                    self.docker_command(checkout),
                    capture_output=True,
                    text=True,
                    timeout=self.config.timeout_seconds,
                    check=False,
                )
                hidden = None
                if public.returncode == 0 and hidden_tests is not None:
                    hidden = subprocess.run(
                        self.docker_command(
                            checkout,
                            command=self.config.hidden_command,
                            hidden_tests=hidden_tests,
                        ),
                        capture_output=True,
                        text=True,
                        timeout=self.config.timeout_seconds,
                        check=False,
                    )
                passed = public.returncode == 0 and (hidden is None or hidden.returncode == 0)
                output = public.stdout
                errors = public.stderr
                if hidden is not None:
                    hidden_summary = (
                        "passed"
                        if hidden.returncode == 0
                        else "failed (details withheld from repair agents)"
                    )
                    output += f"\n--- hidden regression tests: {hidden_summary} ---\n"
                return VerificationResult(
                    candidate_id=candidate.candidate_id,
                    passed=passed,
                    public_passed=public.returncode == 0,
                    hidden_passed=hidden is None or hidden.returncode == 0,
                    exit_code=0 if passed else (hidden.returncode if hidden else public.returncode),
                    stdout=output[-50_000:],
                    stderr=errors[-50_000:],
                    duration_seconds=time.monotonic() - started,
                )
            except subprocess.TimeoutExpired as exc:
                return VerificationResult(
                    candidate_id=candidate.candidate_id,
                    passed=False,
                    exit_code=124,
                    stdout=(exc.stdout or "")[-50_000:],
                    stderr=((exc.stderr or "") + "\nverification timed out")[-50_000:],
                    duration_seconds=time.monotonic() - started,
                )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a command in the repair-loop sandbox")
    parser.add_argument("repository", type=Path)
    parser.add_argument("--image", default="repair-loop-runner:latest")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command or ["python", "-m", "pytest", "-q"]
    if command and command[0] == "--":
        command = command[1:]
    config = SandboxConfig(image=args.image, timeout_seconds=args.timeout, command=command)
    verifier = DockerVerifier(config)
    try:
        result = subprocess.run(
            verifier.docker_command(args.repository),
            timeout=args.timeout,
            check=False,
        )
        return result.returncode
    except subprocess.TimeoutExpired:
        return 124


if __name__ == "__main__":
    raise SystemExit(main())
