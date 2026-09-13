# Private Codespaces setup

The product runs without Docker Desktop, WSL, installers, or Windows feature
changes. The browser connects to a private GitHub Codespace; disposable GitHub
Actions runners perform all candidate execution.

## Repository secrets

Add these under **Settings → Secrets and variables → Codespaces**:

- `WANDB_API_KEY`: a newly rotated W&B key.
- `WANDB_ENTITY`: `mohnishb`.
- `WANDB_PROJECT`: `repair-loop`.
- `REPAIR_LOOP_REMOTE_EXECUTION`: `1`.

The Codespace normally provides repository-scoped GitHub authentication. If it
does not permit workflow dispatch and artifact reads, add
`REPAIR_LOOP_GITHUB_TOKEN` as a fine-grained token limited to this repository
with Actions read/write permission. Never place token values in files,
notebooks, chat, workflow inputs, or action logs.

## Start the app

Rebuild the Codespace after adding secrets, then run:

```bash
uv sync --extra dev --extra demo
uv run marimo run --host 0.0.0.0 --port 2718 notebooks/repair_lab.py
```

Open forwarded port 2718. The readiness cards must show the repository, remote
execution, GitHub authentication, and W&B authentication before **Run repair**
is selected.

## Request flow

The notebook imports `repair_loop` directly. W&B inference and orchestration
run in the Codespace, but generated patches are only compressed and dispatched
as GitHub Actions inputs. A unique workflow run builds the test image on a
GitHub-hosted runner, executes public and hidden tests in a network-disabled
container, uploads `result.json`, and is then discarded. The notebook polls
GitHub, validates the result schema and correlation ID, and feeds public
evidence plus hidden pass/fail status into the next Reflexion iteration.

## Publishing later

Before changing repository visibility to public:

1. Run secret scanning.
2. Review the complete Git history and Actions logs.
3. Confirm `.env`, checkpoints, artifacts, and credentials were never committed.
4. Rotate development credentials.
5. Remove private benchmark material if applicable.
