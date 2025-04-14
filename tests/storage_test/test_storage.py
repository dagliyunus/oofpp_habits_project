import sqlite3
import os
import pytest
from datetime import datetime

from repository.storage_manager import (
    save_habit,
    delete_habit,
    load_all_habits,
    save_checkoff,
    load_checkoffs_for_habit,
)
from config import db_config
from models.habits import Habit

TEST_DB_PATH = "test_habits.db"


@pytest.fixture(autouse=True)
def setup_and_teardown_db(monkeypatch):
    """
   Pytest fixture that automatically runs before and after each test.

   - Overrides the application's DB path to a test-specific SQLite DB
   - Creates the necessary Habit and Habit_Logs tables
   - Deletes the test DB after the test is finished to ensure isolation
   """
    # Redirect the real DB_PATH to use a temporary file for testing
    monkeypatch.setattr(db_config, "DB_PATH", TEST_DB_PATH)

    # Create test DB schema
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Habit (
        habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        frequency TEXT NOT NULL,
        description TEXT,
        deadline_time DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS Habit_Logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        note TEXT,
        missed BOOLEAN DEFAULT 0
    );
    """)

    conn.commit()
    conn.close()

    # Test runs here
    yield

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def test_save_and_load_habit():
    """
    Test that a habit can be saved to and retrieved from the database.
    """
    habit = Habit(
        habit_id=None,
        user_id=1,
        name="Test Habit",
        frequency="daily",
        description="test desc",
        deadline_time=datetime.now(),
        created_at=datetime.now()
    )
    save_habit(habit)

    habits = load_all_habits(user_id=1)
    assert any(h["name"] == "Test Habit" for h in habits)


def test_delete_habit():
    """
   Test that a habit can be deleted by its ID.
   """
    habit = Habit(
        habit_id=None,
        user_id=1,
        name="Delete Me",
        frequency="weekly",
        description="for deletion",
        deadline_time=datetime.now(),
        created_at=datetime.now()
    )
    save_habit(habit)
    # Retrieve the saved habit's ID
    habits = load_all_habits(user_id=1)
    habit_id = habits[0]["habit_id"]
    # Delete and verify it's gone
    delete_habit(habit_id)
    habits = load_all_habits(user_id=1)
    assert not any(h["habit_id"] == habit_id for h in habits)


def test_save_and_load_checkoff():
    """
    Test saving and retrieving a check-off for a habit.
    """
    # Step 1: Create and save a habit
    habit = Habit(
        habit_id=None,
        user_id=1,
        name="With Checkoff",
        frequency="daily",
        description="check this",
        deadline_time=datetime.now(),
        created_at=datetime.now()
    )
    save_habit(habit)
    # Step 2: Retrieve its habit_id
    habits = load_all_habits(user_id=1)
    habit_id = habits[0]["habit_id"]
    # Step 3: Save a checkoff
    save_checkoff(habit_id=habit_id, user_id=1)
    # Step 4: Load logs and validate
    logs = load_checkoffs_for_habit(habit_id)
    assert len(logs) == 1
    assert logs[0]["missed"] == 0