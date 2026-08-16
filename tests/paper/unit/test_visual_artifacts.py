from synthsea.paper.figures import result_figure
from synthsea.paper.tables import result_table


def test_visuals_keep_evidence_provenance() -> None:
    table = result_table("table-1", "artifact-1", "tables/results.tex", ["singlish"])
    figure = result_figure("figure-1", "artifact-1", "figures/results.pdf", ["singlish"])
    assert table.source_refs == ["artifact-1"]
    assert figure.validation_status == "verified"
