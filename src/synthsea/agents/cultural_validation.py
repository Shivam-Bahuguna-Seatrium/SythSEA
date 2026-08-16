from synthsea.agents.base import DeterministicStage


class CulturalValidationStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="cultural_validation", version="v1")
