"""Interactive Repair Loop lab.

Run in a Codespace with: ``uv run marimo run notebooks/repair_lab.py``
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="full")


@app.cell
def _():
    import json
    import os
    from pathlib import Path

    import altair as alt
    import marimo as mo
    import pandas as pd
    import yaml
    from repair_loop.cli import _repair_request
    from repair_loop.orchestrator import RepairLoop
    from repair_loop.schemas import LoopConfig

    return LoopConfig, Path, RepairLoop, alt, json, mo, os, pd, yaml


@app.cell
def _(mo):
    mo.md(r"""
    # Repair Loop Build

    This UI runs the orchestrator in a private Codespace. Generated patches are
    sent as data to disposable GitHub Actions runners and are never executed in
    the Codespace or on your Windows machine.
    """)
    return


@app.cell
def _(mo, os):
    github_repository = os.getenv("GITHUB_REPOSITORY", "")
    remote_enabled = os.getenv("REPAIR_LOOP_REMOTE_EXECUTION") == "1"
    github_authenticated = bool(
        os.getenv("REPAIR_LOOP_GITHUB_TOKEN")
        or os.getenv("GH_TOKEN")
        or os.getenv("GITHUB_TOKEN")
    )
    wandb_authenticated = bool(os.getenv("WANDB_API_KEY"))
    readiness = mo.hstack(
        [
            mo.stat(
                label="Codespace repository",
                value=github_repository or "not detected",
            ),
            mo.stat(
                label="Remote execution",
                value="enabled" if remote_enabled else "disabled",
            ),
            mo.stat(
                label="GitHub authentication",
                value="ready" if github_authenticated else "missing",
            ),
            mo.stat(
                label="W&B authentication",
                value="ready" if wandb_authenticated else "missing",
            ),
        ],
        widths="equal",
    )
    readiness
    return


@app.cell
def _(Path, yaml):
    def case_ids(directory):
        root = Path(directory)
        values = sorted(path.parent.name for path in root.glob("*/manifest.json"))
        return values or ["not-configured"]

    def model_ids(path):
        config = Path(path)
        if not config.is_file():
            return ["not-configured"]
        payload = yaml.safe_load(config.read_text(encoding="utf-8")) or {}
        values = sorted(
            {
                model
                for profile in payload.get("profiles", {}).values()
                for model in profile.values()
            }
        )
        return values or ["not-configured"]

    available_cases = case_ids("benchmarks/cases")
    available_models = model_ids("configs/models.yaml")
    return available_cases, available_models


@app.cell
def _(available_cases, available_models, mo):
    case = mo.ui.dropdown(available_cases, value=available_cases[0], label="Case")
    model = mo.ui.dropdown(available_models, value=available_models[0], label="Model")
    loop_variant = mo.ui.dropdown(
        ["single_pass", "retry_only", "diagnose_fix", "full_team"],
        value="full_team",
        label="Loop variant",
    )
    attempts = mo.ui.slider(1, 12, value=3, label="Max attempts")
    tokens = mo.ui.slider(1_000, 128_000, step=1_000, value=32_000, label="Token budget")
    cost = mo.ui.slider(0.0, 25.0, step=0.25, value=5.0, label="Cost budget (USD)")
    run = mo.ui.run_button(label="Run repair")
    return attempts, case, cost, loop_variant, model, run, tokens


@app.cell
def _(attempts, case, cost, loop_variant, mo, model, run, tokens):
    mo.vstack(
        [
            mo.hstack([case, model, loop_variant], widths="equal"),
            mo.hstack([attempts, tokens, cost], widths="equal"),
            run,
        ]
    )
    return


@app.cell
def _(Path, json, run_output):
    _ = run_output  # Reload persisted checkpoints after an execution.

    def load_runs():
        rows = []
        for path in Path(".repair-loop/runs").glob("**/*.json"):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(payload, dict):
                saved_request = payload.get("request") or {}
                usage = payload.get("usage") or {}
                verifications = payload.get("verifications") or []
                rows.append(
                    {
                        "run": payload.get("run_id", path.stem),
                        "case": saved_request.get("case_id", "unknown"),
                        "model": payload.get("model", "unknown"),
                        "status": payload.get("phase", "unknown"),
                        "attempts": payload.get("iteration", 0),
                        "cost_usd": usage.get("cost_usd", 0),
                        "latency_seconds": payload.get(
                            "latency_seconds", payload.get("duration_seconds", 0)
                        ),
                        "success": payload.get("phase") == "done",
                        "run_url": (
                            verifications[-1].get("run_url") if verifications else None
                        ),
                    }
                )
        return rows

    history = load_runs()
    return (history,)


@app.cell
def _(
    LoopConfig,
    Path,
    RepairLoop,
    attempts,
    case,
    cost,
    loop_variant,
    mo,
    model,
    os,
    run,
    tokens,
    yaml,
):
    request = None
    status = "Ready"
    run_output = ""
    if run.value:
        request = {
            "case": case.value,
            "model": model.value,
            "loop": loop_variant.value,
            "max_attempts": attempts.value,
            "token_budget": tokens.value,
            "cost_budget": cost.value,
        }
        config = LoopConfig.from_yaml("configs/default.yaml")
        variants = yaml.safe_load(
            Path("configs/loops.yaml").read_text(encoding="utf-8")
        )["variants"]
        repository_slug = os.getenv("GITHUB_REPOSITORY", "")
        if "/" in repository_slug:
            owner, repository_name = repository_slug.split("/", 1)
            github_config = config.github_actions.model_copy(
                update={"owner": owner, "repository": repository_name}
            )
        else:
            github_config = config.github_actions
        budget = config.budgets.model_copy(
            update={
                "max_input_tokens": tokens.value,
                "max_cost_usd": cost.value,
            }
        )
        config = config.model_copy(
            update={
                **variants[loop_variant.value],
                "variant": loop_variant.value,
                "model": model.value,
                "role_models": {},
                "max_iterations": attempts.value,
                "budgets": budget,
                "checkpoint_dir": Path(".repair-loop/runs"),
                "github_actions": github_config,
            }
        )
        try:
            with mo.status.spinner(title="Remote repair loop running"):
                result = RepairLoop(config).run(_repair_request(case.value))
            status = "Completed" if result.success else "Failed"
            run_output = result.model_dump_json(indent=2)
        except Exception as exc:
            status = "Error"
            run_output = f"{type(exc).__name__}: {exc}"
    return request, run_output, status


@app.cell
def _(history, mo, request, run_output, status):
    summary = [
        mo.stat(label="Status", value=status),
        mo.stat(label="Saved runs", value=str(len(history))),
        mo.stat(label="Selected", value=request["case"] if request else "—"),
    ]
    output = mo.md(f"```\n{run_output}\n```") if run_output else mo.md("_No run output yet._")
    mo.vstack(
        [
            mo.hstack(summary, widths="equal"),
            output,
            mo.md("## Results"),
            mo.ui.table(history),
        ]
    )
    return


@app.cell
def _(alt, history, mo, pd):
    if not history:
        chart = mo.md("_Charts appear after JSON run artifacts are saved in `.repair-loop/runs`._")
    else:
        frame = pd.DataFrame(history)
        attempts_chart = (
            alt.Chart(frame)
            .mark_bar()
            .encode(
                x=alt.X("model:N", title="Model"),
                y=alt.Y("mean(attempts):Q", title="Mean attempts"),
                color=alt.Color("success:N", title="Success"),
                tooltip=["model", "case", "attempts", "cost_usd", "status"],
            )
            .properties(title="Repair efficiency", height=280)
        )
        cost_chart = (
            alt.Chart(frame)
            .mark_circle(size=100)
            .encode(
                x=alt.X("attempts:Q"),
                y=alt.Y("cost_usd:Q"),
                color="model:N",
                tooltip=["run", "case", "model", "latency_seconds"],
            )
            .properties(title="Attempts versus cost", height=280)
        )
        chart = mo.ui.altair_chart(attempts_chart | cost_chart)
    return


if __name__ == "__main__":
    app.run()
