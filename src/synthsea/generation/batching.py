"""Bounded batching primitives for generation."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

T = TypeVar("T")


def batches(items: Iterable[T], batch_size: int) -> Iterable[list[T]]:
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    batch: list[T] = []
    for item in items:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
