from synthsea.agents.base import DeterministicStage


class JudgeStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="judge", version="v1")
