"""Publication-package assembly."""

from pathlib import Path
from typing import Any

from synthsea.data.storage import write_json


def write_publication_package(path: Path, package: dict[str, Any]) -> None:
    required = {"methods", "results", "limitations", "provenance", "manifest"}
    missing = required.difference(package)
    if missing:
        raise ValueError(f"publication package missing: {', '.join(sorted(missing))}")
    write_json(path, package)
