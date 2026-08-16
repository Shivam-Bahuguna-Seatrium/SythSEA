from pathlib import Path

from synthsea.paper.events import PaperRunEvent, append_event


def test_paper_event_records_run_metadata(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    append_event(
        path,
        PaperRunEvent(
            package_id="package-1",
            source_manifest="manifest-1",
            venue_profile="venue-1",
            stage="validate",
            message="ok",
        ),
    )
    assert "package-1" in path.read_text(encoding="utf-8")
