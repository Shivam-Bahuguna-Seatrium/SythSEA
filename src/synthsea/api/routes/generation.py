"""Local multi-agent generation endpoints."""

from fastapi import APIRouter, BackgroundTasks

from synthsea.api.dependencies import workbench_config, workspace_root
from synthsea.api.schemas.workbench import GenerationRunRequest, GenerationRunResponse
from synthsea.generation.adapters import OllamaAdapter
from synthsea.workspace.generation import GenerationWorkspaceService

router = APIRouter(prefix="/api/generation", tags=["generation"])


@router.post("/runs", response_model=GenerationRunResponse, status_code=201)
def create_generation_run(
    request: GenerationRunRequest, background_tasks: BackgroundTasks
) -> GenerationRunResponse:
    config = workbench_config()
    service = GenerationWorkspaceService(
        workspace_root(), OllamaAdapter(host=str(config["chat"]["ollama_host"]))
    )
    generated = service.start(
        topic=request.topic,
        language_profile_id=request.language_profile_id,
        prompt_count=request.prompt_count,
        seed=request.seed,
        model_version=request.model_version,
    )
    background_tasks.add_task(
        service.run, request.topic, request.language_profile_id, request.prompt_count,
        request.seed, request.model_version, generated.run_id,
    )
    return GenerationRunResponse(**generated.model_dump())


@router.get("/runs", response_model=list[GenerationRunResponse])
def list_generation_runs() -> list[GenerationRunResponse]:
    config = workbench_config()
    service = GenerationWorkspaceService(
        workspace_root(), OllamaAdapter(host=str(config["chat"]["ollama_host"]))
    )
    return [GenerationRunResponse(**run.model_dump()) for run in service.list()]


@router.get("/runs/{run_id}", response_model=GenerationRunResponse)
def get_generation_run(run_id: str) -> GenerationRunResponse:
    config = workbench_config()
    service = GenerationWorkspaceService(
        workspace_root(), OllamaAdapter(host=str(config["chat"]["ollama_host"]))
    )
    return GenerationRunResponse(**service.get(run_id).model_dump())


@router.post("/runs/{run_id}/evaluate", response_model=GenerationRunResponse)
def evaluate_generation_run(run_id: str) -> GenerationRunResponse:
    config = workbench_config()
    service = GenerationWorkspaceService(
        workspace_root(), OllamaAdapter(host=str(config["chat"]["ollama_host"]))
    )
    return GenerationRunResponse(**service.evaluate(run_id).model_dump())