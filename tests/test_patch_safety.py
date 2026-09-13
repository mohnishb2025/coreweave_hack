import pytest

from repair_loop.patch_safety import UnsafePatch, validate_unified_diff
from repair_loop.schemas import PatchPolicy

VALID = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ -1 +1 @@
-old
+new
"""


def test_accepts_small_source_patch() -> None:
    assert validate_unified_diff(VALID) == ["src/app.py"]


def test_accepts_unified_diff_without_diff_git_header() -> None:
    diff = """--- a/clamp.py
+++ b/clamp.py
@@ -1,4 +1,4 @@
 def clamp(value, low, high):
     if value >= high:
-        return high - 1
+        return high
     return max(low, value)
"""
    assert validate_unified_diff(diff) == ["clamp.py"]


@pytest.mark.parametrize(
    "diff",
    [
        VALID.replace("src/app.py", "tests/test_app.py"),
        VALID.replace("src/app.py", "../escape.py"),
        VALID.replace("src/app.py", "C:\\secret.py"),
        VALID + "GIT binary patch\n",
    ],
)
def test_rejects_unsafe_paths_and_binary_patches(diff: str) -> None:
    with pytest.raises(UnsafePatch):
        validate_unified_diff(diff)


def test_enforces_changed_line_limit() -> None:
    with pytest.raises(UnsafePatch):
        validate_unified_diff(VALID, PatchPolicy(max_changed_lines=1))
