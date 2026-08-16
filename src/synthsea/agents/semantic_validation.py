from synthsea.agents.base import DeterministicStage


class SemanticValidationStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="semantic_validation", version="v1")
