from click.testing import CliRunner
from main import cli_main

def test_signup_and_login_flow():
    """
    Test launching the CLI and choosing the 'Exit' option from the main menu.
    """
    runner = CliRunner()
    result = runner.invoke(
        cli_main,
        ["start"],
        # Simulates user choosing "Exit"
        input="3\n"
    )
    assert result.exit_code == 0
    assert " Welcome to Habit Tracker" in result.output