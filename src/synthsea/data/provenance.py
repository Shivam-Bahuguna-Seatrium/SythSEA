"""Append-only provenance references."""

from __future__ import annotations

from synthsea.config.schemas import ProvenanceRef


def source_provenance(source_id: str, source_version: str, transformation: str) -> ProvenanceRef:
    return ProvenanceRef(
        source_type="source_dataset",
        source_id=source_id,
        source_version=source_version,
        transformation=transformation,
    )


def derived_provenance(parent_refs: list[str], transformation: str) -> ProvenanceRef:
    return ProvenanceRef(
        source_type="derived",
        parent_refs=parent_refs,
        transformation=transformation,
    )
