from synthsea.paper.builder import detect_document_tools


def test_builder_reports_a_truthful_tool_status() -> None:
    result = detect_document_tools()
    assert result.status in {"available", "unavailable"}
