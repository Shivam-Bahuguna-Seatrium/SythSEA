"""Dependency providers for the local workbench API."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from synthsea.config.loader import load_yaml
from synthsea.workspace.jobs import WorkspaceJobStore


@lru_cache
def workbench_config() -> dict[str, Any]:
    config_path = Path(os.getenv("SYNTHSEA_WORKBENCH_CONFIG", "configs/workbench.yaml"))
    return load_yaml(config_path)


def workspace_root() -> Path:
    configured = os.getenv("SYNTHSEA_WORKSPACE_ROOT")
    if configured:
        return Path(configured)
    return Path(str(workbench_config()["storage"]["workspace_root"]))


def job_store() -> WorkspaceJobStore:
    return WorkspaceJobStore(workspace_root())