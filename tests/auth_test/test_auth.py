import os
import sqlite3
import pytest
from services.auth import sign_up, log_in
from config import db_config

TEST_DB_PATH = "test_users.db"


@pytest.fixture(autouse=True)
def setup_and_teardown_user_db(monkeypatch):
    """
     Fixture that overrides the DB_PATH to use a test database.
     Automatically sets up and tears down the User table for each test.
     """
    # Override DB path for testing
    monkeypatch.setattr(db_config, "DB_PATH", TEST_DB_PATH)

    # Set up test schema
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT,
            password TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

    # Run the test
    yield

    # Clean up test db
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


def test_successful_signup_and_login():
    """
    Test a complete flow: signing up and then logging in with correct credentials.
    """
    user_id, msg = sign_up("testuser", "test@example.com", "secret")
    assert user_id is not None
    assert "successfully" in msg.lower()

    login_id, login_msg = log_in("testuser", "secret")
    assert login_id == user_id
    assert "successfully" in login_msg.lower()


def test_signup_with_duplicate_username():
    """
    Test that signing up with an already-taken username fails gracefully.
    """
    sign_up("dupuser", "a@example.com", "123")
    user_id, msg = sign_up("dupuser", "b@example.com", "456")
    assert user_id is None
    assert "already exists" in msg.lower()


def test_login_with_incorrect_password():
    """
    Test that logging in with the wrong password returns an error.
    """
    sign_up("wrongpass", "wrong@example.com", "abc123")
    user_id, msg = log_in("wrongpass", "wrongpassword")
    assert user_id is None
    assert "incorrect password" in msg.lower()