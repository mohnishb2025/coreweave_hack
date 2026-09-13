"""W&B OpenAI-compatible inference with typed output and usage accounting."""

from __future__ import annotations

import json
import netrc
import os
import threading
from collections.abc import Sequence
from pathlib import Path
from typing import TypeVar

from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    OpenAI,
    RateLimitError,
)
from pydantic import BaseModel
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from .schemas import Usage

T = TypeVar("T", bound=BaseModel)


class InferenceError(RuntimeError):
    pass


RETRYABLE_ERRORS = (
    ConnectionError,
    TimeoutError,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
    InferenceError,
)

MODEL_PRICES_PER_MILLION: dict[str, tuple[float, float]] = {
    "zai-org/GLM-5.3-Flash": (0.15, 0.50),
    "ibm-granite/granite-4.2-8b": (0.10, 0.15),
    "Qwen/Qwen3.8-27B": (0.40, 3.00),
    "deepseek-ai/DeepSeek-V4-Pro-0813": (1.31, 3.96),
    "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B": (0.10, 0.25),
}


def resolve_api_key(explicit: str | None = None) -> str | None:
    """Resolve credentials without copying them into project files or traces."""
    if explicit:
        return explicit
    if value := os.getenv("WANDB_API_KEY"):
        return value
    candidates = [Path.home() / "_netrc", Path.home() / ".netrc"]
    for candidate in candidates:
        if not candidate.is_file():
            continue
        try:
            credentials = netrc.netrc(str(candidate)).authenticators("api.wandb.ai")
        except (OSError, netrc.NetrcParseError):
            continue
        if credentials:
            return credentials[2]
    return None


def resolve_project(explicit: str | None = None) -> str | None:
    """Resolve W&B's required ``entity/project`` inference routing value."""
    project = explicit or os.getenv("WANDB_PROJECT")
    if not project or "/" in project:
        return project
    entity = os.getenv("WANDB_ENTITY")
    return f"{entity}/{project}" if entity else project


class InferenceClient:
    """Small synchronous client suitable for deterministic threaded orchestration."""

    def __init__(
        self,
        *,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        project: str | None = None,
        temperature: float = 0.0,
        seed: int = 17,
        client: OpenAI | None = None,
    ) -> None:
        key = resolve_api_key(api_key)
        if client is None and not key:
            raise InferenceError("WANDB_API_KEY is required")
        headers: dict[str, str] = {}
        project_name = resolve_project(project)
        if project_name:
            headers["OpenAI-Project"] = project_name
        self._client = client or OpenAI(
            api_key=key,
            base_url=base_url
            or os.getenv("WANDB_INFERENCE_BASE_URL", "https://api.inference.wandb.ai/v1"),
            default_headers=headers,
        )
        self._model = model or os.getenv("REPAIR_LOOP_MODEL")
        self._temperature = temperature
        self._seed = seed
        self._resolved_model: str | None = None
        self._usage = Usage()
        self._lock = threading.Lock()

    @property
    def usage(self) -> Usage:
        with self._lock:
            return self._usage.model_copy(deep=True)

    @retry(
        retry=retry_if_exception_type(RETRYABLE_ERRORS),
        stop=stop_after_attempt(4),
        wait=wait_exponential_jitter(initial=1, max=10),
        reraise=True,
    )
    def list_models(self) -> list[str]:
        models = self._client.models.list()
        ids = sorted(item.id for item in models.data)
        if not ids:
            raise InferenceError("inference endpoint returned no models")
        return ids

    def resolve_model(self) -> str:
        if self._resolved_model:
            return self._resolved_model
        available = self.list_models()
        if self._model:
            if self._model not in available:
                raise InferenceError(
                    f"configured model {self._model!r} is unavailable; available: {available}"
                )
            self._resolved_model = self._model
        else:
            self._resolved_model = available[0]
        return self._resolved_model

    @retry(
        retry=retry_if_exception_type(RETRYABLE_ERRORS),
        stop=stop_after_attempt(4),
        wait=wait_exponential_jitter(initial=1, max=10),
        reraise=True,
    )
    def complete_json(
        self,
        *,
        system: str,
        user: str,
        schema: type[T],
        model: str | None = None,
    ) -> T:
        selected_model = model or self.resolve_model()
        response = self._client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=self._temperature,
            seed=self._seed,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "strict": True,
                    "schema": schema.model_json_schema(),
                },
            },
        )
        raw_usage = response.usage
        with self._lock:
            self._usage.model_calls += 1
            if raw_usage:
                input_tokens = int(raw_usage.prompt_tokens or 0)
                output_tokens = int(raw_usage.completion_tokens or 0)
                self._usage.input_tokens += input_tokens
                self._usage.output_tokens += output_tokens
                input_price, output_price = MODEL_PRICES_PER_MILLION.get(selected_model, (0.0, 0.0))
                self._usage.cost_usd += (
                    input_tokens * input_price + output_tokens * output_price
                ) / 1_000_000
        content = response.choices[0].message.content
        if not content:
            raise InferenceError("model returned an empty response")
        try:
            parsed = schema.model_validate(json.loads(content))
        except (json.JSONDecodeError, ValueError) as exc:
            raise InferenceError(f"invalid structured response: {exc}") from exc
        return parsed


def compact_context(parts: Sequence[str], *, max_chars: int = 80_000) -> str:
    """Bound prompts deterministically, preserving the most recent evidence."""
    text = "\n\n".join(part.strip() for part in parts if part.strip())
    if len(text) <= max_chars:
        return text
    return "[earlier context truncated]\n" + text[-max_chars:]
