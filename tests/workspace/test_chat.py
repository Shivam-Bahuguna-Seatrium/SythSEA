import pytest

from synthsea.workspace.chat import LocalChatService, validate_promotion


def test_unavailable_local_service_reports_recovery_action(tmp_path) -> None:
    models = LocalChatService(tmp_path, "http://127.0.0.1:1").models()

    assert models[0].available is False
    assert "ollama serve" in models[0].unavailable_reason


def test_chat_promotion_requires_explicit_provenance_and_access_decision() -> None:
    with pytest.raises(ValueError, match="provenance"):
        validate_promotion("private", "")