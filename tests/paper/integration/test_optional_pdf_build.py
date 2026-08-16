from synthsea.paper.builder import detect_document_tools


def test_pdf_build_is_optional_and_truthful() -> None:
    result = detect_document_tools()
    assert result.status != "success" or result.output_path is not None
