"""Optional LaTeX/BibTeX tool detection."""

from __future__ import annotations

import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class BuildResult:
    status: str
    output_path: str | None
    message: str


def detect_document_tools() -> BuildResult:
    latex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if latex and bibtex:
        return BuildResult("available", None, "pdflatex and bibtex available")
    return BuildResult("unavailable", None, "required document tools are unavailable")
