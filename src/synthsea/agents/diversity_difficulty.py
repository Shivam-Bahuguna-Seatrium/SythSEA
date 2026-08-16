from synthsea.agents.base import DeterministicStage


class DiversityDifficultyStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="diversity_difficulty", version="v1")
