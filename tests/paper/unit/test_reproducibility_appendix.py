from synthsea.paper.reproducibility import build_appendix


def test_reproducibility_appendix_requires_all_fields() -> None:
    appendix = build_appendix({"prompts": ["p"], "models": ["m"]})
    assert appendix.validation_status == "blocked"
