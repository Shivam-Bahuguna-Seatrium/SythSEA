from synthsea.agents.base import DeterministicStage


class ResourceDiscoveryStage(DeterministicStage):
    def __init__(self) -> None:
        super().__init__(name="resource_discovery", version="v1")
