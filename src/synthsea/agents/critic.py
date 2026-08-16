from synthsea.agents.base import DeterministicStage


class CriticStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="critic", version="v1")
