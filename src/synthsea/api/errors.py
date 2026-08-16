"""Consistent problem responses for the workbench API."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class WorkbenchError(ValueError):
    """Expected workbench failure presented as a user-facing API problem."""


def add_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(WorkbenchError)
    async def workbench_error_handler(_: Request, error: WorkbenchError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(error)})