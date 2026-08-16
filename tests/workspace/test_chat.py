import pytest

from synthsea.workspace.chat import LocalChatService, validate_promotion


def test_unavailable_local_service_reports_recovery_action(tmp_path) -> None:
    models = LocalChatService(tmp_path, "http://127.0.0.1:1").models()

    assert models[0].available is False
    assert "ollama serve" in models[0].unavailable_reason


def test_chat_promotion_requires_explicit_provenance_and_access_decision() -> None:
    with pytest.raises(ValueError, match="provenance"):
        validate_promotion("private", "")


def test_completed_fine_tune_is_listed_as_a_local_chat_model(tmp_path) -> None:
    adapter = tmp_path / "jobs" / "mlx-123" / "adapter"
    adapter.mkdir(parents=True)
    (tmp_path / "jobs" / "mlx-123.json").write_text(
        '{"job_id":"mlx-123","status":"succeeded","model_version":"qwen3-8b-synthsea",'
        '"base_model":"mlx-community/Qwen3-8B-4bit","artifact_refs":'
        '["adapter:' + str(adapter).replace("\\", "/") + '"]}'
    )

    models = LocalChatService(tmp_path, "http://127.0.0.1:1").models()

    assert any(model.model_version == "qwen3-8b-synthsea" for model in models)