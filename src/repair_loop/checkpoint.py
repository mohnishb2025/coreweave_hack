"""Atomic checkpoint persistence for resumable repair runs."""

from __future__ import annotations

import os
from pathlib import Path

from .schemas import LoopState


class CheckpointStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def save(self, state: LoopState) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        target = self.root / f"{state.run_id}.json"
        temporary = target.with_suffix(".tmp")
        temporary.write_text(state.model_dump_json(indent=2), encoding="utf-8")
        os.replace(temporary, target)
        return target

    def load(self, run_id: str) -> LoopState:
        path = self.root / f"{run_id}.json"
        return LoopState.model_validate_json(path.read_text(encoding="utf-8"))
