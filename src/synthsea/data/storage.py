"""Portable JSON and Parquet artifact storage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pyarrow as pa
import pyarrow.parquet as pq


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True, default=str)
        handle.write("\n")


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_parquet(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), path)


def read_parquet(path: Path) -> list[dict[str, Any]]:
    return cast(list[dict[str, Any]], pq.read_table(path).to_pylist())
