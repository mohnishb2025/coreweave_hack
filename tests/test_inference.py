import json
from types import SimpleNamespace

import pytest

from repair_loop.inference import InferenceClient, InferenceError, compact_context
from repair_loop.schemas import QAResult


class FakeOpenAI:
    def __init__(self) -> None:
        self.models = SimpleNamespace(
            list=lambda: SimpleNamespace(
                data=[SimpleNamespace(id="z-model"), SimpleNamespace(id="a-model")]
            )
        )
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))
        self.kwargs = None

    def _create(self, **kwargs: object) -> SimpleNamespace:
        self.kwargs = kwargs
        payload = QAResult(approved=True, summary="passed").model_dump()
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))],
            usage=SimpleNamespace(prompt_tokens=11, completion_tokens=7),
        )


def test_dynamic_model_selection_schema_and_usage() -> None:
    fake = FakeOpenAI()
    client = InferenceClient(client=fake)
    result = client.complete_json(system="system", user="user", schema=QAResult)
    assert result.approved
    assert fake.kwargs["model"] == "a-model"
    assert fake.kwargs["response_format"]["json_schema"]["strict"] is True
    assert client.usage.model_dump() == {
        "model_calls": 1,
        "input_tokens": 11,
        "output_tokens": 7,
        "cost_usd": 0.0,
    }


def test_rejects_unavailable_configured_model() -> None:
    client = InferenceClient(client=FakeOpenAI(), model="missing")
    with pytest.raises(InferenceError):
        client.resolve_model()


def test_context_is_bounded_from_the_end() -> None:
    assert compact_context(["abcdef"], max_chars=3).endswith("def")
