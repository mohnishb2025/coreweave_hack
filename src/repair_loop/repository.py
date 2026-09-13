"""Safe, bounded repository context collection for model handoffs."""

from __future__ import annotations

from pathlib import Path

TEXT_SUFFIXES = {
    ".cfg",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".repair-loop",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "dist",
}


def repository_snapshot(
    repository: Path,
    *,
    max_chars: int = 70_000,
    max_file_chars: int = 12_000,
) -> str:
    """Return a deterministic source-and-test snapshot without binary or secret files."""
    root = repository.resolve()
    files = sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.casefold() in TEXT_SUFFIXES
        and not any(part in EXCLUDED_PARTS or part.startswith(".env") for part in path.parts)
    )
    sections: list[str] = []
    used = 0
    for path in files:
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if len(text) > max_file_chars:
            text = text[:max_file_chars] + "\n[truncated]"
        section = f"--- {relative} ---\n{text}"
        if used + len(section) > max_chars:
            sections.append("[repository snapshot truncated]")
            break
        sections.append(section)
        used += len(section)
    return "\n\n".join(sections)
