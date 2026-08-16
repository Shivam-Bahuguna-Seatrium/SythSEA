from typer.testing import CliRunner

from synthsea.cli import app


def test_version_command_is_cpu_safe() -> None:
    result = CliRunner().invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "0.1.0"
