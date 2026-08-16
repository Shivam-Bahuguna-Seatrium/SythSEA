from __future__ import annotations

import json
from unittest.mock import patch

from synthsea.generation.adapters import DeterministicAdapter, GenerationRequest, OllamaAdapter


def test_deterministic_adapter_records_generation_metadata() -> None:
    request = GenerationRequest(
        prompt="Translate hello",
        model_version="fixture-0.1.0",
        seed=13,
        language_profile_id="singlish",
    )
    response = DeterministicAdapter().generate(request)
    assert response.text.startswith("fixture:")
    assert response.model_version == "fixture-0.1.0"
    assert response.seed == 13
    assert response.provider == "local"


class _FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_ollama_adapter_posts_seed_and_records_local_metadata() -> None:
    request = GenerationRequest(
        prompt="Explain hello",
        model_version="qwen2.5:3b",
        seed=13,
        language_profile_id="singlish",
    )
    payload = {
        "model": "qwen2.5:3b",
        "response": "Hello lah.",
        "prompt_eval_count": 4,
        "eval_count": 2,
    }
    with patch(
        "synthsea.generation.adapters.urlopen", return_value=_FakeResponse(payload)
    ) as open_url:
        response = OllamaAdapter().generate(request)

    request_body = json.loads(open_url.call_args.args[0].data.decode("utf-8"))
    assert request_body["model"] == "qwen2.5:3b"
    assert request_body["stream"] is False
    assert request_body["options"]["seed"] == 13
    assert response.text == "Hello lah."
    assert response.provider == "ollama"
    assert response.input_tokens == 4
    assert response.output_tokens == 2
