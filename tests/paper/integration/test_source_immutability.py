from pathlib import Path

from synthsea.paper.evidence import snapshot_checksums, verify_unchanged


def test_source_checksums_remain_unchanged(tmp_path: Path) -> None:
    source = tmp_path / "result.json"
    source.write_text('{"metric": 1}\n', encoding="utf-8")
    snapshot = snapshot_checksums([source])
    assert verify_unchanged(snapshot) is True
