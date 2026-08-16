"""Exploratory local Ollama chat with auditable local storage."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen
from uuid import uuid4

from synthsea.api.schemas.workbench import (
    ChatConversationRequest,
    ChatConversationResponse,
    ChatMessageResponse,
    LocalModelResponse,
)
from synthsea.generation.adapters import GenerationRequest, OllamaAdapter


def validate_promotion(access_class: str, provenance_ref: str) -> None:
    """Require explicit governance before exploratory chat can become an artifact."""

    if access_class not in {"public", "restricted", "private"}:
        raise ValueError("promotion requires an explicit access class")
    if not provenance_ref.strip():
        raise ValueError("promotion requires an explicit provenance reference")


class LocalChatService:
    def __init__(self, root: Path, ollama_host: str) -> None:
        self.workspace_root = root
        self.root = root / "conversations"
        self.ollama_host = ollama_host.rstrip("/")

    def models(self) -> list[LocalModelResponse]:
        models = self._ollama_models()
        models.extend(self._fine_tuned_models())
        return models

    def _ollama_models(self) -> list[LocalModelResponse]:
        try:
            with urlopen(f"{self.ollama_host}/api/tags", timeout=3) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except URLError:
            return [
                LocalModelResponse(
                    model_version="local-service",
                    available=False,
                    unavailable_reason="Start Ollama, then run `ollama serve`.",
                )
            ]
        raw_models = payload.get("models", []) if isinstance(payload, dict) else []
        return [
            LocalModelResponse(model_version=str(model.get("name", "unknown")), available=True)
            for model in raw_models
            if isinstance(model, dict)
        ]

    def _fine_tuned_models(self) -> list[LocalModelResponse]:
        models: list[LocalModelResponse] = []
        for job_path in (self.workspace_root / "jobs").glob("*.json"):
            try:
                job = json.loads(job_path.read_text())
            except json.JSONDecodeError:
                continue
            if not isinstance(job, dict) or job.get("status") != "succeeded":
                continue
            adapter_path = next(
                (
                    ref.removeprefix("adapter:")
                    for ref in job.get("artifact_refs", [])
                    if isinstance(ref, str) and ref.startswith("adapter:")
                ),
                "",
            )
            if not adapter_path:
                continue
            ready = platform.system() == "Darwin" and shutil.which("mlx_lm.generate") is not None
            models.append(
                LocalModelResponse(
                    model_version=str(job.get("model_version", job_path.stem)),
                    available=ready,
                    engine="mlx_lm",
                    unavailable_reason="Fine-tuned chat requires macOS and mlx-lm."
                    if not ready
                    else "",
                )
            )
        return models

    def create(self, request: ChatConversationRequest) -> ChatConversationResponse:
        model = next(
            (model for model in self.models() if model.model_version == request.model_version), None
        )
        if model is None or not model.available:
            return ChatConversationResponse(
                conversation_id=f"chat-{uuid4().hex[:12]}",
                model_version=request.model_version,
                status="unavailable",
            )
        conversation_id = f"chat-{uuid4().hex[:12]}"
        self._write(
            conversation_id,
            {
                "model_version": request.model_version,
                "access_class": request.access_class.value,
                "temperature": request.temperature,
                "seed": request.seed,
                "engine": model.engine,
                "messages": [],
            },
        )
        return ChatConversationResponse(
            conversation_id=conversation_id,
            model_version=request.model_version,
            status="active",
        )

    def send(self, conversation_id: str, content: str) -> ChatMessageResponse:
        conversation = self._read(conversation_id)
        if conversation.get("engine") == "mlx_lm":
            return self._send_fine_tuned(conversation_id, conversation, content)
        adapter = OllamaAdapter(
            host=self.ollama_host,
            temperature=_float_value(conversation["temperature"]),
        )
        response = adapter.generate(
            GenerationRequest(
                prompt=content,
                model_version=str(conversation["model_version"]),
                seed=_int_value(conversation["seed"]),
                language_profile_id="singlish",
            )
        )
        message_id = f"message-{uuid4().hex[:12]}"
        messages = conversation["messages"]
        if not isinstance(messages, list):
            raise ValueError("conversation messages are malformed")
        messages.extend(
            [
                {"role": "user", "content": content, "exploratory": True},
                {
                    "id": message_id,
                    "role": "assistant",
                    "content": response.text,
                    "exploratory": True,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                },
            ]
        )
        self._write(conversation_id, conversation)
        return ChatMessageResponse(
            message_id=message_id,
            role="assistant",
            content=response.text,
            model_version=response.model_version,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
        )

    def _send_fine_tuned(
        self, conversation_id: str, conversation: dict[str, object], content: str
    ) -> ChatMessageResponse:
        model = self._fine_tuned_model(str(conversation["model_version"]))
        if model is None:
            raise ValueError("fine-tuned model is unavailable")
        result = subprocess.run(
            [
                "mlx_lm.generate",
                "--model",
                model["base_model"],
                "--adapter-path",
                model["adapter_path"],
                "--prompt",
                content,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "mlx_lm.generate failed")
        message_id = f"message-{uuid4().hex[:12]}"
        messages = conversation["messages"]
        if not isinstance(messages, list):
            raise ValueError("conversation messages are malformed")
        messages.extend(
            [
                {"role": "user", "content": content, "exploratory": True},
                {"id": message_id, "role": "assistant", "content": result.stdout.strip(), "exploratory": True},
            ]
        )
        self._write(conversation_id, conversation)
        return ChatMessageResponse(
            message_id=message_id,
            role="assistant",
            content=result.stdout.strip(),
            model_version=str(conversation["model_version"]),
        )

    def _fine_tuned_model(self, model_version: str) -> dict[str, str] | None:
        for job_path in (self.workspace_root / "jobs").glob("*.json"):
            try:
                job = json.loads(job_path.read_text())
            except json.JSONDecodeError:
                continue
            if not isinstance(job, dict) or job.get("status") != "succeeded" or job.get("model_version") != model_version:
                continue
            adapter_path = next(
                (ref.removeprefix("adapter:") for ref in job.get("artifact_refs", []) if isinstance(ref, str) and ref.startswith("adapter:")),
                "",
            )
            if adapter_path:
                return {"base_model": str(job.get("base_model", "")), "adapter_path": adapter_path}
        return None

    def _path(self, conversation_id: str) -> Path:
        return self.root / f"{conversation_id}.json"

    def _read(self, conversation_id: str) -> dict[str, object]:
        path = self._path(conversation_id)
        if not path.is_file():
            raise ValueError(f"conversation not found: {conversation_id}")
        value = json.loads(path.read_text())
        if not isinstance(value, dict):
            raise ValueError("conversation is malformed")
        return value

    def _write(self, conversation_id: str, value: dict[str, object]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self._path(conversation_id).write_text(json.dumps(value, indent=2) + "\n")


def _float_value(value: object) -> float:
    if isinstance(value, int | float):
        return float(value)
    raise ValueError("conversation temperature is malformed")


def _int_value(value: object) -> int:
    if isinstance(value, int):
        return value
    raise ValueError("conversation seed is malformed")