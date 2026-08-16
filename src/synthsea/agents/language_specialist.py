from synthsea.agents.base import DeterministicStage


class LanguageSpecialistStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="language_specialist", version="v1")
