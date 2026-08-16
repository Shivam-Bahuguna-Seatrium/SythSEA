"""Research report package writing."""

from __future__ import annotations

from pathlib import Path

from synthsea.data.storage import write_json
from synthsea.paper.builder import detect_document_tools
from synthsea.paper.package import write_paper_package
from synthsea.research.evidence import public_records
from synthsea.research.io import write_artifact
from synthsea.research.models import EvidenceRecord, ReadinessReport, ResearchDossier, SourceRecord
from synthsea.research.report import render_report


def write_research_package(
    output_root: Path,
    dossier: ResearchDossier,
    matrix: dict[str, object],
    evidence: list[EvidenceRecord],
    sources: list[SourceRecord],
    readiness: ReadinessReport,
) -> Path:
    package_root = output_root / dossier.dossier_id
    public_evidence, excluded = public_records(evidence)
    paper_root = write_paper_package(
        output_root,
        dossier.dossier_id,
        render_report(dossier, public_evidence),
        "",
        detect_document_tools(),
        excluded,
    )
    write_artifact(paper_root / "dossier.json", dossier.model_dump(mode="json"))
    write_artifact(
        paper_root / "literature.json",
        {"sources": [source.model_dump(mode="json") for source in sources]},
    )
    write_artifact(paper_root / "requirements-matrix.json", matrix)
    write_artifact(
        paper_root / "evidence.json",
        {"records": [record.model_dump(mode="json") for record in public_evidence]},
    )
    write_artifact(paper_root / "readiness.json", readiness.model_dump(mode="json"))
    write_json(
        paper_root / "release-manifest.json",
        {
            "package_id": dossier.dossier_id,
            "release_status": readiness.release_status,
            "excluded_artifacts": excluded,
            "source_access_class": "public",
        },
    )
    return package_root