"""Tests for cli."""
from typer.testing import CliRunner

from misc.cli import app

runner = CliRunner()


def test_app() -> None:
    """Tests for cli."""
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert not result.output
