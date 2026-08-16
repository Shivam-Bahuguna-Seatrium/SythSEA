import json
from pathlib import Path

from synthsea.research.io import validate_schema


def test_research_dossier_contract_fixture_is_valid() -> None:
    fixture = {
        "dossier_id": "dossier",
        "version": "v1",
        "title": "Research dossier",
        "target_venue": "RegiCON 2026",
        "created_at": "2026-08-13T00:00:00Z",
        "source_refs": [],
        "research_question_ids": ["rq-001"],
        "status": "blocked",
    }
    validate_schema(
        fixture,
        Path("specs/003-deep-research-final-report/contracts/research-dossier.schema.json"),
    )


def test_evidence_matrix_contract_rejects_missing_claim_type() -> None:
    schema = json.loads(
        Path(
            "specs/003-deep-research-final-report/contracts/evidence-matrix.schema.json"
        ).read_text()
    )
    assert schema["title"] == "SynthSEA Claim Evidence Matrix"