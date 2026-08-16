"""Run-level token and cost accounting."""

from dataclasses import dataclass


@dataclass
class CostTracker:
    examples: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    requests: int = 0
    retries: int = 0
    cache_hits: int = 0
    estimated_cost: float = 0.0

    def record(self, input_tokens: int, output_tokens: int, cost: float = 0.0) -> None:
        self.examples += 1
        self.requests += 1
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.estimated_cost += cost

    def as_dict(self) -> dict[str, int | float]:
        return {
            "examples": self.examples,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "requests": self.requests,
            "retries": self.retries,
            "cache_hits": self.cache_hits,
            "estimated_cost": self.estimated_cost,
        }