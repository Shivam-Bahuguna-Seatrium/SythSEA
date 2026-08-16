"""Governed local generation runs for the research workbench."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from synthsea.agents.base import StageContext, StageGraph
from synthsea.agents.code_switching import CodeSwitchingStage
from synthsea.agents.critic import CriticStage
from synthsea.agents.cultural_validation import CulturalValidationStage
from synthsea.agents.diversity_difficulty import DiversityDifficultyStage
from synthsea.agents.instruction_generation import InstructionGenerationStage
from synthsea.agents.judge import JudgeStage
from synthsea.agents.language_profile import LanguageProfileStage
from synthsea.agents.language_specialist import LanguageSpecialistStage
from synthsea.agents.refinement import RefinementStage
from synthsea.agents.resource_discovery import ResourceDiscoveryStage
from synthsea.agents.semantic_validation import SemanticValidationStage
from synthsea.agents.topic_context import TopicContextStage
from synthsea.config.schemas import StrictModel
from synthsea.generation.adapters import GenerationAdapter, GenerationRequest


class GenerationWorkspaceService:
    """Run and record the candidate-data portion of the SynthSEA methodology."""

    def __init__(self, root: Path, adapter: GenerationAdapter) -> None:
        self.root = root / "generation"
        self.adapter = adapter

    def start(
        self,
        topic: str,
        language_profile_id: str,
        prompt_count: int,
        seed: int,
        model_version: str,
    ) -> GenerationRun:
        run_id = f"generation-{uuid4().hex[:12]}"
        result = GenerationRun(
            run_id=run_id, dataset_version=f"generated:{run_id}:v1", model_version=model_version,
            topic=topic, language_profile_id=language_profile_id, record_count=0,
            requested_count=prompt_count, status="queued", evaluation_status="not_started",
            failures=[], stages=[stage.name for stage in _methodology_stages()], records=[],
            dataset_path=str(self.root / f"{run_id}-data"),
            artifact_ref=f"generation:{self.root / f'{run_id}.json'}",
        )
        self._save(result, [])
        return result

    def run(
        self,
        topic: str,
        language_profile_id: str,
        prompt_count: int,
        seed: int,
        model_version: str,
        run_id: str | None = None,
    ) -> GenerationRun:
        result = self.get(run_id) if run_id else self.start(
            topic, language_profile_id, prompt_count, seed, model_version
        )
        result = result.model_copy(update={"status": "running"})
        self._save(result, [])
        prompts = [
            f"Create one culturally appropriate instruction-response example about {topic} "
            f"for {language_profile_id}. "
            "Preserve factual uncertainty, avoid personal data, and do not claim research results."
            for _ in range(prompt_count)
        ]
        records: list[dict[str, object]] = []
        failures: list[str] = []
        for index, prompt in enumerate(prompts):
            try:
                response = self.adapter.generate(
                    GenerationRequest(
                        prompt=prompt,
                        model_version=model_version,
                        seed=seed + index,
                        language_profile_id=language_profile_id,
                    )
                )
                records.append(
                    {
                        "instruction": prompt,
                        "response": response.text,
                        "seed": seed + index,
                        "model_version": response.model_version,
                    }
                )
            except (ValueError, RuntimeError) as error:
                failures.append(f"prompt {index + 1}: {error}")
            result = result.model_copy(
                update={"record_count": len(records), "failures": failures, "records": records[-5:]}
            )
            self._save(result, records)
        stage_results = StageGraph(stages=_methodology_stages()).run(
            records,
            StageContext(run_id=result.run_id, metadata={"model": model_version, "topic": topic}),
        )
        result = result.model_copy(
            update={
                "status": "completed" if records else "failed",
                "stages": [stage.stage_name for stage in stage_results],
            }
        )
        self._save(result, records, stage_results)
        return result

    def list(self) -> list[GenerationRun]:
        if not self.root.is_dir():
            return []
        runs: list[GenerationRun] = []
        for path in self.root.glob("*.json"):
            try:
                value = json.loads(path.read_text())
                runs.append(GenerationRun.model_validate(value["run"]))
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
        return sorted(runs, key=lambda run: run.run_id, reverse=True)

    def get(self, run_id: str) -> GenerationRun:
        path = self.root / f"{run_id}.json"
        if not path.is_file():
            raise ValueError(f"generation run not found: {run_id}")
        return GenerationRun.model_validate(json.loads(path.read_text())["run"])

    def evaluate(self, run_id: str) -> GenerationRun:
        path = self.root / f"{run_id}.json"
        if not path.is_file():
            raise ValueError(f"generation run not found: {run_id}")
        value = json.loads(path.read_text())
        result = GenerationRun.model_validate(value["run"])
        if result.status != "completed":
            raise ValueError("generation batch must complete before agent evaluation")
        result = result.model_copy(
            update={"evaluation_status": "agent_reviewed_pending_experiment_evaluation"}
        )
        stage_results = value.get("stage_results", [])
        self._save(result, value.get("records", []), stage_results)
        return result

    def _save(
        self,
        result: GenerationRun,
        records: list[dict[str, object]],
        stage_results: list[object] | None = None,
    ) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        data_root = Path(result.dataset_path)
        data_root.mkdir(parents=True, exist_ok=True)
        (data_root / "train.jsonl").write_text(
            "".join(
                json.dumps(
                    {
                        "messages": [
                            {"role": "user", "content": str(record["instruction"])},
                            {"role": "assistant", "content": str(record["response"])},
                        ]
                    }
                )
                + "\n"
                for record in records
            )
        )
        (self.root / f"{result.run_id}.json").write_text(
            json.dumps(
                {
                    "run": result.model_dump(mode="json"),
                    "records": records,
                    "stage_results": [
                        stage if isinstance(stage, dict) else stage.model_dump(mode="json")
                        for stage in stage_results or []
                    ],
                    "next_steps": [
                        "Review and filter generated candidates before dataset intake.",
                        "Train only an approved dataset version with recorded provenance.",
                        "Run baseline, ablation, per-language evaluation, and evidence checks "
                        "before paper claims.",
                    ],
                },
                indent=2,
            )
            + "\n"
        )


class GenerationRun(StrictModel):
    run_id: str
    dataset_version: str
    model_version: str
    topic: str
    language_profile_id: str
    record_count: int
    requested_count: int
    status: str
    evaluation_status: str
    failures: list[str]
    stages: list[str]
    records: list[dict[str, object]]
    dataset_path: str
    artifact_ref: str


def _methodology_stages() -> list:
    return [
        ResourceDiscoveryStage(), TopicContextStage(), LanguageProfileStage(),
        InstructionGenerationStage(), LanguageSpecialistStage(), CodeSwitchingStage(),
        CulturalValidationStage(), SemanticValidationStage(), DiversityDifficultyStage(),
        CriticStage(), JudgeStage(), RefinementStage(),
    ]