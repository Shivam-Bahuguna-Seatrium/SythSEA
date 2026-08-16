from synthsea.agents.base import DeterministicStage


class InstructionGenerationStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="instruction_generation", version="v1")
