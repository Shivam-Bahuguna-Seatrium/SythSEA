from synthsea.agents.base import DeterministicStage


class RefinementStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="refinement", version="v1")
