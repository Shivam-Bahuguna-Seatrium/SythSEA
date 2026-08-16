"""Server-side access checks for workspace projections."""

from __future__ import annotations

from synthsea.config.schemas import AccessClass


def can_include_in_public_export(access_class: AccessClass) -> bool:
    return access_class is AccessClass.PUBLIC


def require_public_exportable(access_class: AccessClass) -> None:
    if not can_include_in_public_export(access_class):
        raise ValueError(f"{access_class.value} artifacts cannot be included in a public export")