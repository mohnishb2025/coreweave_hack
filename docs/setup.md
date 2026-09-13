# Setup

## Requirements

- A private GitHub repository with Actions enabled
- A GitHub Codespace created from that repository
- W&B and GitHub credentials stored as Codespaces secrets

The devcontainer installs Python 3.12, `uv`, project dependencies, marimo, and
GitHub CLI inside the Codespace. Candidate verification is dispatched to
GitHub-hosted runners. Docker is used only inside those disposable remote
runners; it is not installed or invoked on Windows.

Follow [Private Codespaces setup](codespaces.md) for secret names and notebook
startup. Never put credentials in model profiles, notebooks, workflow inputs,
run artifacts, screenshots, or chat.

## Verify

```bash
uv sync --extra dev --extra demo
uv run pytest
uv run ruff check .
uv run repair-loop --help
uv run marimo check --strict notebooks/repair_lab.py
```
