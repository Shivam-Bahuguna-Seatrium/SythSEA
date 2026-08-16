from synthsea.agents.base import DeterministicStage


class TopicContextStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="topic_context", version="v1")
