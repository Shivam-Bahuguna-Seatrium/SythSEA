"""Evidence-aware manuscript content assembly."""

from __future__ import annotations

from synthsea.paper.renderer import render_manuscript
from synthsea.paper.sections import PaperSection, assemble_sections, language_result_section
from synthsea.research.models import EvidenceRecord, ResearchDossier

REPORT_SECTIONS = (
    "research_questions",
    "research_gap",
    "experimental_protocol",
    "baselines",
    "ablations",
    "statistical_analysis",
    "human_evaluation",
    "error_analysis",
    "cultural_and_ethical_considerations",
    "data_and_code_availability",
    "acknowledgements",
    "appendices",
)


def build_report_sections(
    dossier: ResearchDossier,
    evidence: list[EvidenceRecord],
) -> list[PaperSection]:
    available = {record.language_slice for record in evidence}
    result_values = {
        language_slice: (
            "Verified evidence available."
            if language_slice in available
            else "[MISSING EVIDENCE]"
        )
        for language_slice in ("singlish", "malay", "tamil", "singapore_mandarin")
    }
    sections = assemble_sections(
        {
            "title": (
                "SynthSEA: Multi-Agent Synthetic Instruction Generation for Resource-Uneven "
                "Southeast Asian Languages"
            ),
            "abstract": "[MISSING EVIDENCE]",
            "keywords": "SynthSEA; multilingual NLP; synthetic instruction data; Singapore",
            "introduction": "[MISSING EVIDENCE]",
            "related_work": "[MISSING EVIDENCE]",
            "methodology": "[MISSING EVIDENCE]",
            "architecture": "[MISSING EVIDENCE]",
            "dataset_design": "[MISSING EVIDENCE]",
            "experiments": "[MISSING EVIDENCE]",
            "results": language_result_section(result_values).content,
            "discussion": "[MISSING EVIDENCE]",
            "limitations": "[MISSING EVIDENCE]",
            "ethics": "[MISSING EVIDENCE]",
            "reproducibility": "[MISSING EVIDENCE]",
            "conclusion": "[MISSING EVIDENCE]",
            "references": "[MISSING EVIDENCE]",
        }
    )
    additional = [
        PaperSection("research_questions", dossier.novelty_summary),
        PaperSection("research_gap", "[MISSING EVIDENCE]"),
        PaperSection("experimental_protocol", "[MISSING EVIDENCE]"),
        PaperSection("baselines", "[MISSING EVIDENCE]"),
        PaperSection("ablations", "[MISSING EVIDENCE]"),
        PaperSection("statistical_analysis", "[MISSING EVIDENCE]"),
        PaperSection("human_evaluation", "[MISSING EVIDENCE]"),
        PaperSection("error_analysis", "[MISSING EVIDENCE]"),
        PaperSection("cultural_and_ethical_considerations", "[MISSING EVIDENCE]"),
        PaperSection("data_and_code_availability", "[MISSING EVIDENCE]"),
        PaperSection("acknowledgements", "[MISSING EVIDENCE]"),
        PaperSection("appendices", "[MISSING EVIDENCE]"),
    ]
    return sections + additional


def render_report(dossier: ResearchDossier, evidence: list[EvidenceRecord]) -> str:
    return render_manuscript(build_report_sections(dossier, evidence))