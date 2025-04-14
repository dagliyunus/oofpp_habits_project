import pytest
from datetime import datetime, timedelta
from analytics.analytics_module import (
    get_longest_streak,
    get_most_missed_habits,
    get_habits_by_period
)

@pytest.fixture
def sample_logs():
    """
    Fixture that provides a sample set of habit log entries
    for use in analytics tests.
    """
    logs = [
        {
            "habit_id": 1,
            "completed_at": (datetime.now() - timedelta(days=2)).isoformat(),
            "missed": False,
            "frequency": "daily"
        },
        {
            "habit_id": 1,
            "completed_at": (datetime.now() - timedelta(days=1)).isoformat(),
            "missed": False,
            "frequency": "daily"
        },
        {
            "habit_id": 1,
            "completed_at": datetime.now().isoformat(),
            "missed": False,
            "frequency": "daily"
        },
        {
            "habit_id": 2,
            "completed_at": datetime.now().isoformat(),
            "missed": True,
            "frequency": "daily"
        },
        {
            "habit_id": 2,
            "completed_at": datetime.now().isoformat(),
            "missed": True,
            "frequency": "daily"
        },
        {
            "habit_id": 3,
            "completed_at": datetime.now().isoformat(),
            "missed": False,
            "frequency": "weekly"
        }
    ]
    return logs


def test_get_longest_streak(sample_logs):
    """
    Test that the function correctly returns the habit with the longest streak.
    """
    longest = get_longest_streak(sample_logs)
    # habit_id=1 has 3-day streak
    assert longest == (1, 3)


def test_get_most_missed_habits(sample_logs):
    """
    Test that the function returns habits sorted by most missed first.
    """
    missed = get_most_missed_habits(sample_logs)
    # habit_id=2 missed twice
    assert missed[0] == (2, 2)


def test_get_habits_by_period(sample_logs):
    """
    Test that habits are correctly filtered by their frequency period.
    """
    daily = get_habits_by_period(sample_logs, "daily")
    weekly = get_habits_by_period(sample_logs, "weekly")
    assert all(h["frequency"] == "daily" for h in daily)
    assert all(h["frequency"] == "weekly" for h in weekly)