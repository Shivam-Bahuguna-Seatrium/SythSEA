"""Local DuckDB catalog for runs and artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import duckdb

from synthsea.config.schemas import ArtifactRef, RunStatus


class Catalog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = duckdb.connect(str(path))
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                run_id VARCHAR PRIMARY KEY,
                status VARCHAR NOT NULL,
                config_id VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS artifacts (
                artifact_id VARCHAR PRIMARY KEY,
                run_id VARCHAR,
                path VARCHAR NOT NULL,
                kind VARCHAR NOT NULL,
                checksum VARCHAR NOT NULL,
                access_class VARCHAR NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    def register_run(self, run_id: str, status: RunStatus, config_id: str | None = None) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO runs (run_id, status, config_id) VALUES (?, ?, ?)",
            [run_id, status.value, config_id],
        )

    def register_artifact(self, run_id: str, artifact: ArtifactRef) -> None:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO artifacts
            (artifact_id, run_id, path, kind, checksum, access_class)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                artifact.artifact_id,
                run_id,
                artifact.path,
                artifact.kind,
                artifact.checksum,
                artifact.access_class.value,
            ],
        )

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT run_id, status, config_id, created_at FROM runs WHERE run_id = ?",
            [run_id],
        ).fetchone()
        if row is None:
            return None
        return dict(zip(("run_id", "status", "config_id", "created_at"), row, strict=True))

    def close(self) -> None:
        self.connection.close()
