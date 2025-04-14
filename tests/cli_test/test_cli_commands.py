import pytest
from click.testing import CliRunner
from cli.commands import cli

@pytest.fixture
def runner():
    """
    Provides a Click CLI runner for simulating command-line execution.
    """
    return CliRunner()

def test_create_command(runner):
    """
    Test the 'create' CLI command to add a new habit.
    """
    result = runner.invoke(cli, ["create", "--user-id", "1"], input="Water plants\ndaily\nHelps my flowers\n2025-04-14 20:00\n")
    assert result.exit_code == 0
    assert "✅ Habit" in result.output

def test_delete_command(runner):
    """
    Test the 'delete' CLI command to remove a habit.
    """
    result = runner.invoke(cli, ["delete"], input="1\n")
    assert result.exit_code == 0
    assert "🗑️ Habit" in result.output or "❌ Habit not found" in result.output

def test_list_command(runner):
    """
    Test the 'list' CLI command to display all habits for a user.
    """
    result = runner.invoke(cli, ["list", "--user-id", "1"])
    assert result.exit_code == 0
    assert "📋 Habits for user 1:" in result.output or "No habits found" in result.output

def test_checkoff_command(runner):
    """
    Test the 'checkoff' CLI command to mark a habit as completed.
    """
    result = runner.invoke(cli, ["checkoff", "--user-id", "1"], input="1\n")
    assert result.exit_code == 0
    assert "✅ Habit" in result.output or "❌ Habit not found" in result.output