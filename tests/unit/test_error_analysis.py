from synthsea.evaluation.errors import categorize


def test_error_finding_retains_record_reference() -> None:
    assert categorize("r1", "cultural", "review required").record_id == "r1"
