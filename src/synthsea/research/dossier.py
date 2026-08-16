"""Research dossier assembly."""

from __future__ import annotations

from pathlib import Path

from synthsea.data.storage import write_json
from synthsea.paper.models import VenueStatus
from synthsea.research.io import write_artifact
from synthsea.research.models import (
    DossierStatus,
    ResearchDossier,
    ResearchQuestion,
    SourceRecord,
    SourceStatus,
)
from synthsea.research.sources import find_duplicate_sources, write_literature_matrix
from synthsea.research.venue_research import venue_status


def default_research_questions() -> list[ResearchQuestion]:
    return [
        ResearchQuestion(
            question_id="rq-001",
            question=(
                "Does coordinated language-aware synthetic instruction generation improve "
                "quality over declared baselines?"
            ),
            hypotheses=[
                "The full pipeline will improve at least one predeclared quality measure "
                "without unacceptable safety or cultural regressions."
            ],
            language_slices=["singlish", "malay", "tamil", "singapore_mandarin"],
            claim_ids=["claim-primary-quality"],
        ),
        ResearchQuestion(
            question_id="rq-002",
            question="Which components of SynthSEA account for observed quality differences?",
            hypotheses=[
                "Removing language-aware, cultural, or verification components will change "
                "predeclared outcomes."
            ],
            language_slices=["singlish", "malay", "tamil", "singapore_mandarin"],
            claim_ids=["claim-ablation"],
        ),
        ResearchQuestion(
            question_id="rq-003",
            question=(
                "How do quality, safety, and cultural judgments vary across the four target "
                "settings?"
            ),
            hypotheses=[
                "Performance and failure patterns will differ by language setting and must "
                "not be hidden by aggregate scores."
            ],
            language_slices=["singlish", "malay", "tamil", "singapore_mandarin"],
            claim_ids=["claim-language-slices"],
        ),
    ]


def build_dossier(
    sources: list[SourceRecord],
    target_venue: str = "RegiCON 2026",
    dossier_id: str = "synthsea-regicon-2026",
) -> tuple[ResearchDossier, list[ResearchQuestion]]:
    questions = default_research_questions()
    status, venue_issues = venue_status(sources, target_venue)
    unresolved = list(venue_issues)
    unresolved.extend(
        f"duplicate_source:{source_id}" for source_id in find_duplicate_sources(sources)
    )
    unresolved.extend(
        "unverified_literature_source"
        for source in sources
        if source.verification_status is not SourceStatus.VERIFIED
    )
    dossier = ResearchDossier(
        dossier_id=dossier_id,
        version="v1",
        title="SynthSEA research-to-publication dossier",
        target_venue=target_venue,
        source_refs=[source.source_id for source in sources],
        research_question_ids=[question.question_id for question in questions],
        novelty_summary=(
            "Novelty remains a research hypothesis until verified literature comparison and "
            "the declared experiments are complete."
        ),
        unresolved_items=sorted(set(unresolved)),
        status=DossierStatus.BLOCKED if unresolved else DossierStatus.REVIEWED,
    )
    if status is VenueStatus.CONFLICTED:
        dossier = dossier.model_copy(update={"status": DossierStatus.BLOCKED})
    return dossier, questions


def write_dossier_package(
    output_root: Path,
    dossier: ResearchDossier,
    questions: list[ResearchQuestion],
    sources: list[SourceRecord],
) -> Path:
    output_root.mkdir(parents=True, exist_ok=True)
    dossier_path = output_root / f"{dossier.dossier_id}.json"
    write_artifact(
        dossier_path,
        {
            "dossier": dossier.model_dump(mode="json"),
            "research_questions": [question.model_dump(mode="json") for question in questions],
        },
    )
    write_literature_matrix(output_root / f"{dossier.dossier_id}-literature.json", sources)
    write_json(
        output_root / f"{dossier.dossier_id}-novelty.json",
        {"summary": dossier.novelty_summary, "unresolved_items": dossier.unresolved_items},
    )
    return dossier_path