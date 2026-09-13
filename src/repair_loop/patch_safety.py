"""Strict validation for model-produced unified diffs."""

from __future__ import annotations

import re
from pathlib import PurePosixPath

from .schemas import PatchPolicy


class UnsafePatch(ValueError):
    pass


_DIFF_HEADER = re.compile(r"^diff --git (?:\"?a/(\S+)\"?) (?:\"?b/(\S+)\"?)$")
_PATH_HEADER = re.compile(r"^(?:---|\+\+\+) (.+?)(?:\t.*)?$")


def _normalize(raw: str) -> PurePosixPath | None:
    raw = raw.strip().strip('"').replace("\\", "/")
    if raw == "/dev/null":
        return None
    if raw.startswith(("a/", "b/")):
        raw = raw[2:]
    if not raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise UnsafePatch(f"absolute or empty path is forbidden: {raw!r}")
    path = PurePosixPath(raw)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise UnsafePatch(f"unsafe path component in {raw!r}")
    return path


def _assert_allowed(path: PurePosixPath | None, policy: PatchPolicy) -> None:
    if path is None:
        return
    folded = tuple(part.casefold() for part in path.parts)
    forbidden = {root.casefold() for root in policy.forbidden_roots}
    if folded and folded[0] in forbidden:
        raise UnsafePatch(f"editing {path} is forbidden")


def validate_unified_diff(diff: str, policy: PatchPolicy | None = None) -> list[str]:
    """Return modified paths or raise before the patch reaches disk."""
    policy = policy or PatchPolicy()
    if not diff.strip():
        raise UnsafePatch("patch is empty")
    if len(diff.encode("utf-8")) > policy.max_bytes:
        raise UnsafePatch("patch exceeds byte limit")
    if "\x00" in diff or "GIT binary patch" in diff or "Binary files " in diff:
        raise UnsafePatch("binary patches are forbidden")

    files: set[str] = set()
    changed_lines = 0
    diff_headers = 0
    has_hunk = False

    for line in diff.splitlines():
        if line.startswith("diff --git "):
            match = _DIFF_HEADER.match(line)
            if not match:
                raise UnsafePatch(f"malformed diff header: {line}")
            old_path, new_path = (_normalize(value) for value in match.groups())
            _assert_allowed(old_path, policy)
            _assert_allowed(new_path, policy)
            if old_path != new_path:
                raise UnsafePatch("renames are forbidden")
            assert new_path is not None
            files.add(new_path.as_posix())
            diff_headers += 1
        elif line.startswith(("--- ", "+++ ")):
            match = _PATH_HEADER.match(line)
            if not match:
                raise UnsafePatch(f"malformed path header: {line}")
            path = _normalize(match.group(1))
            _assert_allowed(path, policy)
            if line.startswith("+++ ") and path is not None:
                files.add(path.as_posix())
        elif line.startswith("@@ "):
            has_hunk = True
        elif line.startswith(("+", "-")):
            changed_lines += 1
        elif line.startswith(("new file mode 120000", "old mode 120000")):
            raise UnsafePatch("symbolic links are forbidden")

    if not files or not has_hunk:
        raise UnsafePatch("patch must contain file headers and at least one hunk")
    if len(files) > policy.max_files:
        raise UnsafePatch("patch exceeds file limit")
    if changed_lines > policy.max_changed_lines:
        raise UnsafePatch("patch exceeds changed-line limit")
    return sorted(files)
