from synthsea.evaluation.leakage import find_prompt_overlap
from tests.unit.test_evaluation import record


def test_leakage_finds_prompt_overlap() -> None:
    assert len(find_prompt_overlap([record("a"), record("b")])) == 1
