"""Command-line presentation shell for Repair Loop Build."""

from __future__ import annotations

import asyncio
import importlib
import inspect
import json
from pathlib import Path
from typing import Any

import typer
import yaml
from click import ClickException

from .evaluation import build_leaderboard, evaluate_records, weave_url

app = typer.Typer(
    name="repair-loop",
    help="Run, resume, and evaluate sandboxed code-repair loops.",
    no_args_is_help=True,
)
console = typer.echo
DEFAULT_RUNS = Path(".repair-loop/runs")


def _jsonable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if hasattr(value, "dict"):
        return value.dict()
    if hasattr(value, "__dict__"):
        return vars(value)
    return value


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise typer.BadParameter(f"Cannot read {path}: {exc}") from exc


def _invoke(callable_: Any, **kwargs: Any) -> Any:
    signature = inspect.signature(callable_)
    accepted = {
        name: value
        for name, value in kwargs.items()
        if name in signature.parameters
        or any(p.kind == p.VAR_KEYWORD for p in signature.parameters.values())
    }
    result = callable_(**accepted)
    return asyncio.run(result) if inspect.isawaitable(result) else result


def _orchestrator_class() -> type[Any]:
    candidates = (
        ("repair_loop.orchestrator", "RepairOrchestrator"),
        ("repair_loop.orchestrator", "RepairLoop"),
        ("repair_loop", "RepairOrchestrator"),
        ("repair_loop", "RepairLoop"),
    )
    for module_name, class_name in candidates:
        try:
            module = importlib.import_module(module_name)
            value = getattr(module, class_name)
            if isinstance(value, type):
                return value
        except (ImportError, AttributeError):
            continue
    raise RuntimeError(
        "RepairOrchestrator is unavailable. Install the core repair-loop package first."
    )


def _orchestrator(**kwargs: Any) -> Any:
    cls = _orchestrator_class()
    if "config" in inspect.signature(cls).parameters and "config" not in kwargs:
        try:
            schemas = importlib.import_module("repair_loop.schemas")
            config_path = Path(kwargs.pop("config_path", "configs/default.yaml"))
            config = schemas.LoopConfig.from_yaml(config_path)
            updates: dict[str, Any] = {}
            if kwargs.get("variant"):
                variants_path = Path("configs/loops.yaml")
                variants = yaml.safe_load(variants_path.read_text(encoding="utf-8")).get(
                    "variants", {}
                )
                variant_name = str(kwargs["variant"])
                if variant_name not in variants:
                    raise ValueError(
                        f"unknown loop variant {variant_name!r}; choose from {sorted(variants)}"
                    )
                updates.update(variants[variant_name])
                updates["variant"] = variant_name
            if kwargs.get("model"):
                updates["model"] = kwargs["model"]
                updates["role_models"] = {}
            if kwargs.get("project"):
                project = str(kwargs["project"])
                entity = kwargs.get("entity")
                updates["project"] = (
                    project if "/" in project or not entity else f"{entity}/{project}"
                )
            if kwargs.get("max_attempts"):
                updates["max_iterations"] = kwargs["max_attempts"]
            if kwargs.get("runs_dir"):
                updates["checkpoint_dir"] = Path(kwargs["runs_dir"])
            if kwargs.get("token_budget"):
                updates["budgets"] = config.budgets.model_copy(
                    update={"max_input_tokens": kwargs["token_budget"]}
                )
            if kwargs.get("cost_budget") is not None:
                current = updates.get("budgets", config.budgets)
                updates["budgets"] = current.model_copy(
                    update={"max_cost_usd": kwargs["cost_budget"]}
                )
            kwargs["config"] = config.model_copy(update=updates)
        except (ImportError, AttributeError, OSError, ValueError) as exc:
            raise RuntimeError(f"Cannot construct loop configuration: {exc}") from exc
    return _invoke(cls, **kwargs)


def _print_result(result: Any, *, entity: str | None, project: str | None) -> None:
    console(json.dumps(_jsonable(result), indent=2, default=str))
    url = weave_url(entity, project)
    if url:
        console(f"Weave: {url}")
    else:
        console("Weave: local-only (set WANDB_ENTITY and WANDB_PROJECT for a URL)")


def _files(directory: Path, patterns: tuple[str, ...]) -> list[Path]:
    if not directory.exists():
        return []
    return sorted({path for pattern in patterns for path in directory.glob(pattern)})


def _case_manifest(case: str | Path) -> tuple[dict[str, Any], Path]:
    supplied = Path(case)
    candidates = (
        supplied / "manifest.json",
        supplied,
        Path("benchmarks/cases") / str(case) / "manifest.json",
    )
    for candidate in candidates:
        if candidate.is_file():
            payload = _load_json(candidate)
            if not isinstance(payload, dict):
                raise typer.BadParameter(f"Case manifest must be an object: {candidate}")
            return payload, candidate.parent
    raise typer.BadParameter(f"Unknown case: {case}")


def _repair_request(case: str | Path) -> Any:
    payload, root = _case_manifest(case)
    try:
        request_type = importlib.import_module("repair_loop.schemas").RepairRequest
    except (ImportError, AttributeError):
        return payload
    expected = payload.get("expected_failure", {})
    task = payload.get("task") or expected.get("reason") or f"Repair case {payload.get('id')}"
    repository = (root / payload.get("repository", "repo")).resolve()
    hidden_tests_value = payload.get("hidden_tests")
    hidden_tests = (root / hidden_tests_value).resolve() if hidden_tests_value else None
    return request_type(
        case_id=str(payload.get("id", root.name)),
        task=task,
        repository=repository,
        hidden_tests=hidden_tests,
        allowed_source_paths=payload.get("allowed_source_paths", []),
        failure_output=json.dumps(expected, indent=2),
        context=json.dumps(
            {
                "allowed_source_paths": payload.get("allowed_source_paths", []),
                "test_commands": payload.get("test_commands", {}),
            },
            indent=2,
        ),
    )


@app.command("models")
def models(
    directory: Path = typer.Option(Path("configs"), "--directory", "-d"),
) -> None:
    """List configured model profiles."""
    files = _files(directory, ("*.yaml", "*.yml", "*.json"))
    if not files:
        console(f"No model profiles found in {directory}")
        return
    for path in files:
        try:
            payload = (
                _load_json(path)
                if path.suffix == ".json"
                else yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            )
        except (OSError, ValueError, yaml.YAMLError):
            continue
        profiles = payload.get("profiles", {}) if isinstance(payload, dict) else {}
        if profiles:
            for profile_name, assignments in profiles.items():
                formatted = ", ".join(
                    f"{role}={model}" for role, model in sorted(assignments.items())
                )
                console(f"{profile_name}: {formatted}")
        elif isinstance(payload, dict) and "model" in payload:
            console(f"{path.stem}: {payload['model'] or 'role-routed'}")


@app.command("cases")
def cases(
    directory: Path = typer.Option(Path("benchmarks/cases"), "--directory", "-d"),
) -> None:
    """List benchmark cases."""
    files = _files(directory, ("*/manifest.json", "*.yaml", "*.yml", "*.json"))
    if not files:
        console(f"No cases found in {directory}")
        return
    for path in files:
        console(path.parent.name if path.name == "manifest.json" else path.stem)


@app.command("repair")
def repair(
    case: str = typer.Argument(..., help="Case ID or case definition path."),
    model: str = typer.Option(..., "--model", "-m"),
    variant: str = typer.Option("full_team", "--variant", "-v"),
    max_attempts: int | None = typer.Option(None, min=1, max=50),
    token_budget: int = typer.Option(32_000, min=1),
    cost_budget: float = typer.Option(5.0, min=0.01),
    runs_dir: Path = typer.Option(DEFAULT_RUNS),
    entity: str | None = typer.Option(None, envvar="WANDB_ENTITY"),
    project: str | None = typer.Option(None, envvar="WANDB_PROJECT"),
) -> None:
    """Run one bounded repair loop."""
    try:
        orchestrator = _orchestrator(
            model=model,
            variant=variant,
            runs_dir=runs_dir,
            entity=entity,
            project=project,
            max_attempts=max_attempts,
            token_budget=token_budget,
            cost_budget=cost_budget,
        )
        method = getattr(orchestrator, "repair", None) or orchestrator.run
        request = _repair_request(case)
        result = _invoke(
            method,
            request=request,
            case=request,
            case_id=case,
            model=model,
            max_attempts=max_attempts,
            token_budget=token_budget,
            cost_budget=cost_budget,
        )
    except (RuntimeError, AttributeError, TypeError) as exc:
        raise ClickException(str(exc)) from exc
    _print_result(result, entity=entity, project=project)


@app.command("benchmark")
def benchmark(
    cases_file: Path = typer.Argument(..., exists=True, readable=True),
    models: list[str] = typer.Option(..., "--model", "-m"),
    variants: list[str] = typer.Option(["full_team"], "--variant", "-v"),
    output: Path = typer.Option(Path(".repair-loop/leaderboard.json")),
    max_attempts: int | None = typer.Option(None, min=1, max=50),
    entity: str | None = typer.Option(None, envvar="WANDB_ENTITY"),
    project: str | None = typer.Option(None, envvar="WANDB_PROJECT"),
) -> None:
    """Run a benchmark matrix and write an offline leaderboard."""
    payload = _load_json(cases_file)
    cases_payload = payload.get("cases", payload) if isinstance(payload, dict) else payload
    if not isinstance(cases_payload, list):
        raise typer.BadParameter("cases file must contain a JSON list or {'cases': [...]}")
    records: list[Any] = []
    try:
        for variant in variants:
            for model in models:
                for case in cases_payload:
                    case_id = case.get("id", case) if isinstance(case, dict) else case
                    request = (
                        _repair_request(case_id)
                        if not isinstance(case, dict) or "repository" not in case
                        else case
                    )
                    orchestrator = _orchestrator(
                        model=model,
                        variant=variant,
                        entity=entity,
                        project=project,
                        max_attempts=max_attempts,
                    )
                    method = getattr(orchestrator, "repair", None) or orchestrator.run
                    result = _invoke(
                        method,
                        request=request,
                        case=request,
                        case_id=case_id,
                        model=model,
                        max_attempts=max_attempts,
                    )
                    records.append(
                        {
                            "case_id": case_id,
                            "model": model,
                            "variant": variant,
                            "output": _jsonable(result),
                        }
                    )
    except (RuntimeError, AttributeError, TypeError) as exc:
        raise ClickException(str(exc)) from exc
    board = build_leaderboard(evaluate_records(records))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(board, indent=2), encoding="utf-8")
    _print_result(board, entity=entity, project=project)
    console(f"Leaderboard: {output}")


@app.command("resume")
def resume(
    run_id: str = typer.Argument(...),
    runs_dir: Path = typer.Option(DEFAULT_RUNS),
    max_attempts: int | None = typer.Option(None, min=1, max=50),
    entity: str | None = typer.Option(None, envvar="WANDB_ENTITY"),
    project: str | None = typer.Option(None, envvar="WANDB_PROJECT"),
) -> None:
    """Resume a persisted run from its latest checkpoint."""
    try:
        orchestrator = _orchestrator(runs_dir=runs_dir, entity=entity, project=project)
        method = orchestrator.resume
        result = _invoke(method, run_id=run_id, max_attempts=max_attempts)
    except (RuntimeError, AttributeError, TypeError) as exc:
        raise ClickException(str(exc)) from exc
    _print_result(result, entity=entity, project=project)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
