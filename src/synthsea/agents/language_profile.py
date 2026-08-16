from synthsea.agents.base import DeterministicStage


class LanguageProfileStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="language_profile", version="v1")
