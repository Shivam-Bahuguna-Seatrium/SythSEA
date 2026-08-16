"""Local Ollama chat endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from synthsea.api.dependencies import workbench_config, workspace_root
from synthsea.api.schemas.workbench import (
    ChatConversationRequest,
    ChatConversationResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    LocalModelResponse,
)
from synthsea.workspace.chat import LocalChatService

router = APIRouter(prefix="/api/chat", tags=["chat"])


def chat_service() -> LocalChatService:
    config = workbench_config()
    return LocalChatService(workspace_root(), str(config["chat"]["ollama_host"]))


@router.get("/models", response_model=list[LocalModelResponse])
def list_models(
    service: LocalChatService = Depends(chat_service),  # noqa: B008
) -> list[LocalModelResponse]:
    return service.models()


@router.post("/conversations", response_model=ChatConversationResponse, status_code=201)
def create_conversation(
    request: ChatConversationRequest,
    service: LocalChatService = Depends(chat_service),  # noqa: B008
) -> ChatConversationResponse:
    return service.create(request)


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=ChatMessageResponse,
    status_code=201,
)
def send_message(
    conversation_id: str,
    request: ChatMessageRequest,
    service: LocalChatService = Depends(chat_service),  # noqa: B008
) -> ChatMessageResponse:
    try:
        return service.send(conversation_id, request.content)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error