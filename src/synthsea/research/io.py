"""Serialization and JSON Schema validation for research artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from synthsea.config.loader import load_yaml
from synthsea.data.storage import read_json, write_json


def load_artifact(path: Path) -> dict[str, Any]:
    if path.suffix.lower() in {".yaml", ".yml"}:
        return load_yaml(path)
    value = read_json(path)
    if not isinstance(value, dict):
        raise ValueError(f"research artifact must be an object: {path}")
    return value


def write_artifact(path: Path, value: Any) -> None:
    write_json(path, value)


def validate_schema(value: dict[str, Any], schema_path: Path) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(value), key=lambda error: list(error.path)
    )
    if errors:
        details = "; ".join(error.message for error in errors)
        raise ValueError(f"schema validation failed: {details}")