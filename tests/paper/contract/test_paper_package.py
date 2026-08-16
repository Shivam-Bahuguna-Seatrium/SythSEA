from synthsea.paper.builder import BuildResult
from synthsea.paper.package import write_paper_package


def test_paper_package_records_excluded_artifacts(tmp_path) -> None:
    root = write_paper_package(
        tmp_path,
        "package-1",
        "manuscript",
        "bibliography",
        BuildResult("unavailable", None, "missing tools"),
        ["restricted-1"],
    )
    assert (root / "manifest.json").is_file()
    assert (root / "manuscript.tex").read_text() == "manuscript"
