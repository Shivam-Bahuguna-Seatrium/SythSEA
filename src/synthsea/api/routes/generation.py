"""Local multi-agent generation endpoints."""

from fastapi import APIRouter

from synthsea.api.dependencies import workbench_config, workspace_root
from synthsea.api.schemas.workbench import GenerationRunRequest, GenerationRunResponse
from synthsea.generation.adapters import OllamaAdapter
from synthsea.workspace.generation import GenerationWorkspaceService

router = APIRouter(prefix="/api/generation", tags=["generation"])


@router.post("/runs", response_model=GenerationRunResponse, status_code=201)
def create_generation_run(request: GenerationRunRequest) -> GenerationRunResponse:
    config = workbench_config()
    generated = GenerationWorkspaceService(
        workspace_root(), OllamaAdapter(host=str(config["chat"]["ollama_host"]))
    ).run(
        topic=request.topic,
        language_profile_id=request.language_profile_id,
        prompt_count=request.prompt_count,
        seed=request.seed,
        model_version=request.model_version,
    )
    return GenerationRunResponse(**generated.model_dump())