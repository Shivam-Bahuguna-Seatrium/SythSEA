"""Paper package output assembly."""

from __future__ import annotations

from pathlib import Path

from synthsea.config.schemas import AccessClass
from synthsea.data.storage import write_json
from synthsea.paper.builder import BuildResult


def write_paper_package(
    output_root: Path,
    package_id: str,
    manuscript: str,
    bibliography: str,
    build: BuildResult,
    excluded_artifacts: list[str],
) -> Path:
    package_root = output_root / package_id
    package_root.mkdir(parents=True, exist_ok=True)
    (package_root / "manuscript.tex").write_text(manuscript, encoding="utf-8")
    (package_root / "references.bib").write_text(bibliography, encoding="utf-8")
    write_json(
        package_root / "manifest.json",
        {
            "package_id": package_id,
            "access_class": AccessClass.PUBLIC.value,
            "excluded_artifacts": excluded_artifacts,
            "build_status": build.status,
            "build_message": build.message,
        },
    )
    return package_root
