"""Default and validated experiment requirements."""

from __future__ import annotations

from synthsea.research.models import ExperimentRequirement, RequirementStatus


def default_requirements() -> list[ExperimentRequirement]:
    requirements: list[ExperimentRequirement] = []
    conditions = ("baseline", "synthsea_full", "ablation_language", "ablation_cultural")
    for language_slice in ("singlish", "malay", "tamil", "singapore_mandarin"):
        for condition_id in conditions:
            requirements.append(
                ExperimentRequirement(
                    requirement_id=f"req-{language_slice}-{condition_id}",
                    question_id=(
                        "rq-001"
                        if condition_id in {"baseline", "synthsea_full"}
                        else "rq-002"
                    ),
                    claim_ids=["claim-primary-quality"],
                    condition_id=condition_id,
                    dataset_versions=[f"{language_slice}:approved-v1"],
                    language_slices=[language_slice],
                    metrics=["quality_pass_rate", "safety_pass_rate", "cultural_review_pass_rate"],
                    sample_size=None,
                    statistical_method=(
                        "researcher-approved uncertainty or significance method required"
                    ),
                    human_evaluation="required for cultural and quality claims",
                    command=(
                        f"synthsea experiment run --language {language_slice} "
                        f"--condition {condition_id}"
                    ),
                    expected_artifacts=[f"experiments/results/{language_slice}/{condition_id}.json"],
                    status=RequirementStatus.MISSING,
                )
            )
    return requirements