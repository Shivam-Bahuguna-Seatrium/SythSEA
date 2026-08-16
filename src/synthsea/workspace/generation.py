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
from synthsea.generation.adapters import GenerationAdapter
from synthsea.generation.runner import GenerationConfig, GenerationRunner


class GenerationWorkspaceService:
    """Run and record the candidate-data portion of the SynthSEA methodology."""

    def __init__(self, root: Path, adapter: GenerationAdapter) -> None:
        self.root = root / "generation"
        self.adapter = adapter

    def run(
        self,
        topic: str,
        language_profile_id: str,
        prompt_count: int,
        seed: int,
        model_version: str,
    ) -> GenerationRun:
        run_id = f"generation-{uuid4().hex[:12]}"
        prompts = [
            f"Create one culturally appropriate instruction-response example about {topic} for {language_profile_id}. "
            "Preserve factual uncertainty, avoid personal data, and do not claim research results."
            for _ in range(prompt_count)
        ]
        generated = GenerationRunner(self.adapter).run(
            prompts,
            GenerationConfig(run_id, language_profile_id, "tier_b_multi_agent", seed, model_version=model_version),
        )
        records = [record.model_dump(mode="json") for record in generated.records]
        stage_results = StageGraph(stages=_methodology_stages()).run(
            records, StageContext(run_id=run_id, metadata={"model": model_version, "topic": topic})
        )
        result = GenerationRun(
            run_id=run_id,
            model_version=model_version,
            topic=topic,
            language_profile_id=language_profile_id,
            record_count=len(records),
            failures=generated.failures,
            stages=[stage.stage_name for stage in stage_results],
            artifact_ref=f"generation:{self.root / f'{run_id}.json'}",
        )
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / f"{run_id}.json").write_text(
            json.dumps(
                {
                    "run": result.model_dump(mode="json"),
                    "records": records,
                    "stage_results": [stage.model_dump(mode="json") for stage in stage_results],
                    "next_steps": [
                        "Review and filter generated candidates before dataset intake.",
                        "Train only an approved dataset version with recorded provenance.",
                        "Run baseline, ablation, per-language evaluation, and evidence checks before paper claims.",
                    ],
                },
                indent=2,
            )
            + "\n"
        )
        return result


class GenerationRun:
    def __init__(self, **values: object) -> None:
        self.__dict__.update(values)

    def model_dump(self, mode: str = "python") -> dict[str, object]:
        return dict(self.__dict__)


def _methodology_stages() -> list:
    return [
        ResourceDiscoveryStage(), TopicContextStage(), LanguageProfileStage(),
        InstructionGenerationStage(), LanguageSpecialistStage(), CodeSwitchingStage(),
        CulturalValidationStage(), SemanticValidationStage(), DiversityDifficultyStage(),
        CriticStage(), JudgeStage(), RefinementStage(),
    ]