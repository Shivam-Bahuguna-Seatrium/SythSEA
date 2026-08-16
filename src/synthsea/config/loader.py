"""YAML configuration loading with simple environment overrides."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Raised when a configuration file is missing or malformed."""


def load_yaml(path: Path, required_keys: tuple[str, ...] = ()) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigurationError(f"Configuration file does not exist: {path}")
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ConfigurationError(f"Configuration must be a mapping: {path}")
    missing = [key for key in required_keys if key not in data]
    if missing:
        raise ConfigurationError(f"Missing required keys in {path}: {', '.join(missing)}")
    return data


def apply_environment_overrides(data: dict[str, Any], prefix: str = "SYNTHSEA__") -> dict[str, Any]:
    result = dict(data)
    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue
        path = key[len(prefix) :].lower().split("__")
        target = result
        for part in path[:-1]:
            current = target.setdefault(part, {})
            if not isinstance(current, dict):
                raise ConfigurationError(f"Cannot override nested value: {key}")
            target = current
        target[path[-1]] = value
    return result
