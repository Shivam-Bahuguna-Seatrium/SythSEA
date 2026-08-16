"""Research-question, claim, and experiment requirement matrix assembly."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from synthsea.research.io import load_artifact, write_artifact
from synthsea.research.models import ExperimentRequirement, ResearchDossier
from synthsea.research.requirements import default_requirements


def build_matrix(
    dossier: ResearchDossier,
    requirements: list[ExperimentRequirement] | None = None,
) -> dict[str, Any]:
    selected = requirements or default_requirements()
    return {
        "matrix_id": f"{dossier.dossier_id}-readiness",
        "version": "v1",
        "dossier_id": dossier.dossier_id,
        "generated_at": dossier.created_at.isoformat(),
        "language_slices": ["singlish", "malay", "tamil", "singapore_mandarin"],
        "requirements": [requirement.model_dump(mode="json") for requirement in selected],
        "claims": [
            {
                "claim_id": "claim-primary-quality",
                "claim_text": (
                    "SynthSEA improves declared quality measures over the declared baseline."
                ),
                "claim_type": "numerical",
                "evidence_ids": [],
                "source_ids": [],
                "language_slices": ["singlish", "malay", "tamil", "singapore_mandarin"],
                "status": "missing",
            },
            {
                "claim_id": "claim-ablation",
                "claim_text": "Declared SynthSEA components contribute to the observed result.",
                "claim_type": "methodological",
                "evidence_ids": [],
                "source_ids": [],
                "language_slices": ["singlish", "malay", "tamil", "singapore_mandarin"],
                "status": "missing",
            },
            {
                "claim_id": "claim-language-slices",
                "claim_text": (
                    "Results and failure patterns differ across target language settings."
                ),
                "claim_type": "comparative",
                "evidence_ids": [],
                "source_ids": [],
                "language_slices": ["singlish", "malay", "tamil", "singapore_mandarin"],
                "status": "missing",
            },
        ],
    }


def write_matrix(path: Path, matrix: dict[str, Any]) -> None:
    write_artifact(path, matrix)


def load_matrix(path: Path) -> dict[str, Any]:
    return load_artifact(path)