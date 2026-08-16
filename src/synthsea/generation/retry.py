"""Bounded retry helper."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry(operation: Callable[[], T], attempts: int = 3) -> T:
    if attempts < 1:
        raise ValueError("attempts must be positive")
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            return operation()
        except Exception as error:  # noqa: BLE001
            last_error = error
    assert last_error is not None
    raise last_error
