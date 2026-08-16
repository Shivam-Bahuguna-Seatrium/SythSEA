"""JSON Schema validation for external artifact contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def validate_contract(value: dict[str, Any], schema_path: Path) -> None:
    with schema_path.open(encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator(schema).validate(value)
