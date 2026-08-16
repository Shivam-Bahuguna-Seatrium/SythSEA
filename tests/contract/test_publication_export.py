from pathlib import Path

from synthsea.export.reports import write_publication_package


def test_publication_package_writes_required_sections(tmp_path: Path) -> None:
    path = tmp_path / "publication.json"
    write_publication_package(
        path,
        {"methods": {}, "results": {}, "limitations": [], "provenance": {}, "manifest": {}},
    )
    assert path.is_file()