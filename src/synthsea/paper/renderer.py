"""Deterministic manuscript source rendering."""

from synthsea.paper.sections import PaperSection


def render_manuscript(sections: list[PaperSection], bibliography: str = "") -> str:
    blocks = [f"\\section{{{section.section_type}}}\n{section.content}" for section in sections]
    if bibliography:
        blocks.append("\\bibliography{references}")
    return "\n\n".join(blocks) + "\n"
