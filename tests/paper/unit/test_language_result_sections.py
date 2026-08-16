from synthsea.paper.sections import language_result_section


def test_four_language_results_precede_aggregate() -> None:
    section = language_result_section(
        {"singlish": "1", "malay": "2", "tamil": "3", "singapore_mandarin": "4"},
        "aggregate",
    )
    assert section.content.index("singlish") < section.content.index("aggregate")
    assert section.content.index("singapore_mandarin") < section.content.index("aggregate")
