"""Model adapters with a deterministic CPU implementation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from synthsea.config.schemas import StrictModel


class GenerationRequest(StrictModel):
    prompt: str
    model_version: str
    seed: int
    language_profile_id: str


class GenerationResponse(StrictModel):
    text: str
    provider: str
    model_version: str
    seed: int
    input_tokens: int
    output_tokens: int
    estimated_cost: float


class GenerationAdapter(Protocol):
    """Model provider boundary used by the generation runner."""

    @property
    def provider(self) -> str:
        """Provider identifier persisted with generation metadata."""

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate one response and return reproducibility metadata."""


class DeterministicAdapter:
    provider = "local"

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        text = f"fixture:{request.language_profile_id}:{request.prompt}"
        return GenerationResponse(
            text=text,
            provider=self.provider,
            model_version=request.model_version,
            seed=request.seed,
            input_tokens=len(request.prompt.split()),
            output_tokens=len(text.split()),
            estimated_cost=0.0,
        )


@dataclass(frozen=True)
class OllamaAdapter:
    """Local Ollama `/api/generate` adapter for a developer workstation."""

    host: str = "http://127.0.0.1:11434"
    temperature: float = 0.2
    timeout_seconds: float = 180.0
    provider: str = "ollama"

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        payload = {
            "model": request.model_version,
            "prompt": request.prompt,
            "stream": False,
            "options": {"seed": request.seed, "temperature": self.temperature},
        }
        endpoint = f"{self.host.rstrip('/')}/api/generate"
        http_request = Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(http_request, timeout=self.timeout_seconds) as http_response:
                response_data = json.loads(http_response.read().decode("utf-8"))
        except HTTPError as error:
            raise RuntimeError(f"Ollama generation failed with HTTP {error.code}") from error
        except URLError as error:
            raise RuntimeError(
                f"Cannot reach Ollama at {self.host}. Start Ollama, then run `ollama serve`."
            ) from error
        if not isinstance(response_data, dict):
            raise RuntimeError("Ollama returned a non-object response")
        text = response_data.get("response")
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("Ollama response did not contain generated text")
        model_version = response_data.get("model", request.model_version)
        if not isinstance(model_version, str):
            model_version = request.model_version
        return GenerationResponse(
            text=text,
            provider=self.provider,
            model_version=model_version,
            seed=request.seed,
            input_tokens=_int_or_zero(response_data.get("prompt_eval_count")),
            output_tokens=_int_or_zero(response_data.get("eval_count")),
            estimated_cost=0.0,
        )


@dataclass(frozen=True)
class AdapterFailure:
    prompt: str
    reason: str


def _int_or_zero(value: object) -> int:
    return value if isinstance(value, int) and value >= 0 else 0
