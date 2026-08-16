"""Read existing Feature 003 readiness artifacts for the workbench."""

from __future__ import annotations

import json
from pathlib import Path

from synthsea.api.schemas.workbench import ReadinessItemResponse


def readiness(root: Path) -> tuple[str, list[ReadinessItemResponse]]:
    path = root / "research-packages" / "synthsea-regicon-2026" / "readiness.json"
    if not path.is_file():
        return "blocked", [
            ReadinessItemResponse(
                item_id="readiness-missing",
                category="evidence",
                severity="blocking",
                status="missing",
                message="Generate a research readiness report before release.",
            )
        ]
    report = json.loads(path.read_text())
    blockers = report.get("blocking_issues", []) if isinstance(report, dict) else []
    return str(report.get("release_status", "blocked")), [
        ReadinessItemResponse(
            item_id=f"blocker-{index}",
            category="readiness",
            severity="blocking",
            status="blocked",
            message=str(blocker),
            resolution_action="Register verified evidence or resolve the stated requirement.",
        )
        for index, blocker in enumerate(blockers)
    ]