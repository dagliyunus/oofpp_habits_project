import pytest
from datetime import datetime, timedelta
from tests.habit_test.habit_testable import HabitTestable


@pytest.fixture
def habit():
    """
    Fixture that provides a testable habit instance with a past deadline.
    """
    return HabitTestable(
        habit_id=1,
        user_id=1,
        name="Test Habit",
        frequency="daily",
        description="Test Habit",
        deadline_time=datetime.now() - timedelta(days=1)
    )


def test_add_checkoff(habit):
    """
    Test that add_checkoff() correctly adds a non-missed log entry.
    """
    habit.add_checkoff()
    assert len(habit.logs) == 1
    assert habit.logs[0]['missed'] is False


def test_calculate_streaks(habit):
    """
    Test that calculate_streaks() correctly returns a 3-day streak.
    """
    habit.logs = []
    habit.add_checkoff(datetime.now() - timedelta(days=2))
    habit.add_checkoff(datetime.now() - timedelta(days=1))
    habit.add_checkoff(datetime.now())
    assert habit.calculate_streaks() == 3


def test_was_missed(habit):
    """
    Test that was_missed() correctly detects and logs a missed habit.
    """
    missed = habit.was_missed()
    assert missed is True
    assert habit.logs[-1]['missed'] is True