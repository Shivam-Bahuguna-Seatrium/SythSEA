from synthsea.paper.reproducibility import build_appendix


def test_complete_reproducibility_metadata_is_verified() -> None:
    required_fields = (
        "prompts",
        "models",
        "seeds",
        "configs",
        "datasets",
        "commands",
        "environment",
        "checksums",
    )
    fields = {field: ["fixture"] for field in required_fields}
    assert build_appendix(fields).validation_status == "verified"
