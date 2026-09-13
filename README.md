# Repair Loop Build

A bounded, observable code-repair system that asks an inference model for a
patch, validates it in a disposable sandbox, and feeds failures back into the
next attempt. Weave captures the decision trail and evaluation metrics while
the Codespace run store makes every loop resumable.

## Quick start

Create a private GitHub Codespace from this repository. No local Docker, WSL,
installer, or Windows configuration is required:

```bash
uv sync --extra dev --extra demo
uv run pytest
uv run repair-loop models
uv run repair-loop cases
uv run repair-loop repair CASE_ID --model MODEL_ID --variant full_team
uv run marimo run --host 0.0.0.0 --port 2718 notebooks/repair_lab.py
```

Set `WANDB_ENTITY=mohnishb` and `WANDB_PROJECT=repair-loop` to print the
corresponding Weave workspace URL. `wandb login` credentials or
`WANDB_API_KEY` authenticate inference and trace uploads. Remote dispatch is
off by default and requires `REPAIR_LOOP_REMOTE_EXECUTION=1` in the Codespace.

## Commands

- `repair-loop models` and `repair-loop cases` discover available definitions.
- `repair-loop repair CASE --model MODEL` runs one bounded loop.
- `repair-loop benchmark cases.json -m MODEL_A -m MODEL_B` writes a leaderboard.
- `repair-loop resume RUN_ID` continues from a persisted checkpoint.

## Documentation

- [Setup](docs/setup.md)
- [Private Codespaces setup](docs/codespaces.md)
- [Architecture](docs/architecture.md)
- [Threat model](docs/threat-model.md)
- [Evaluation methodology](docs/methodology.md)
- [Demo guide](docs/demo.md)
- [Limitations](docs/limitations.md)

No API keys are included. Treat generated patches and benchmark fixtures as
untrusted input.

The reinforcement mechanism is verifier-guided Reflexion: failed patches,
public test evidence, critic lessons, and QA feedback are persisted and fed
back into a fresh diagnosis and plan. Model weights are not trained.
