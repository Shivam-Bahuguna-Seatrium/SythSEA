from typer.testing import CliRunner

from synthsea.cli import app


def test_research_dossier_cli_writes_blocked_dossier(tmp_path) -> None:
    output = tmp_path / "dossier.json"
    result = CliRunner().invoke(
        app,
        ["research", "dossier", "--sources", str(tmp_path / "sources"), "--output", str(output)],
    )

    assert result.exit_code == 0
    assert output.is_file()
    assert "dossier.json" in result.stdout