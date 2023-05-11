import hypothesis as hy
import pytest
from hypothesis.strategies import integers
from typer.testing import CliRunner

from cedh_proxy.cli import app

runner = CliRunner()


@pytest.mark.xfail(reason="Not implemented yet.")
@hy.given(integers(min_value=1))
@pytest.mark.parametrize("flag", ["--ddb", "--cedh-decklist-database"])
def test_select_decks_cedh_decklist_database(limit, flag):
    result = runner.invoke(
        app,
        [
            "select-decks",
            flag,
            "--csv",
            "--limit",
            str(limit),
        ],
    )
    assert result.exit_code == 0
    assert result.stdout.count("\n") == limit + 1
