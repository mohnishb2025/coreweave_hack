"""Weave initialization kept separate from offline-safe evaluation code."""

from __future__ import annotations

import os
from typing import Any

import weave


def initialize_weave(project: str | None) -> Any | None:
    """Initialize tracing when a project is configured, with an explicit opt-out."""
    if not project or os.getenv("REPAIR_LOOP_DISABLE_WEAVE") == "1":
        return None
    return weave.init(project)
