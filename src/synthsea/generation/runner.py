"""CPU-first generation runner with explicit code-switch metadata."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from synthsea.agents.code_switching import CodeSwitchPolicy
from synthsea.config.schemas import AccessClass, ProvenanceRef
from synthsea.data.models import DataRecord
from synthsea.generation.adapters import GenerationAdapter, GenerationRequest


class GenerationConfig:
    def __init__(
        self,
        run_id: str,
        language_profile_id: str,
        condition_id: str,
        seed: int,
        code_switching: CodeSwitchPolicy | None = None,
        model_version: str = "fixture-0.1.0",
    ) -> None:
        self.run_id = run_id
        self.language_profile_id = language_profile_id
        self.condition_id = condition_id
        self.seed = seed
        self.code_switching = code_switching or CodeSwitchPolicy()
        self.model_version = model_version


@dataclass
class GenerationResult:
    records: list[DataRecord]
    failures: list[str] = field(default_factory=list)


class GenerationRunner:
    def __init__(self, adapter: GenerationAdapter) -> None:
        self.adapter = adapter

    def run(self, prompts: list[str], config: GenerationConfig) -> GenerationResult:
        records: list[DataRecord] = []
        failures: list[str] = []
        for index, prompt in enumerate(prompts):
            try:
                response = self.adapter.generate(
                    GenerationRequest(
                        prompt=prompt,
                        model_version=config.model_version,
                        seed=config.seed + index,
                        language_profile_id=config.language_profile_id,
                    )
                )
                switch = config.code_switching
                record_text = response.text
                records.append(
                    DataRecord(
                        record_id=f"{config.run_id}-{index:04d}",
                        dataset_id=None,
                        record_version="v1",
                        instruction=prompt,
                        response=record_text,
                        language_profile_id=config.language_profile_id,
                        task_category="fixture",
                        source_type="source_independent",
                        access_class=AccessClass.PUBLIC,
                        provenance_ref=ProvenanceRef(
                            source_type="source_independent",
                            source_id=config.run_id,
                            transformation="deterministic_generation",
                        ),
                        content_hash=hashlib.sha256(record_text.encode()).hexdigest(),
                        switch_condition=switch.condition,
                        switch_direction=switch.direction,
                        language_proportion=switch.target_proportion,
                        communicative_intent=switch.intent,
                    )
                )
            except (ValueError, RuntimeError) as error:
                failures.append(f"prompt {index}: {error}")
        return GenerationResult(records=records, failures=failures)
