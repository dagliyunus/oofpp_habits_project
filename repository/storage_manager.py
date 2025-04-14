import sqlite3

from config.db_config import get_connection
from datetime import datetime


def save_habit(habit):
    """
    Insert a new habit into the Habit table.
    Parameters:
        habit (Habit): A Habit object containing all required fields.
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Insert the habit data into the Habit table
    cursor.execute("""
        INSERT INTO Habit (user_id, name, frequency, description, deadline_time, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        habit.user_id,
        habit.name,
        habit.frequency,
        habit.description,
        habit.deadline_time,
        habit.created_at
    ))
    conn.commit()
    conn.close()


def delete_habit(habit_id):
    """
    Delete a habit by its unique habit ID.
    Parameters:
        habit_id (int): The ID of the habit to be deleted.
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Delete the habit row based on habit_id
    cursor.execute("DELETE FROM Habit WHERE habit_id = ?", (habit_id,))
    conn.commit()
    conn.close()


def load_all_habits(user_id):
    """
    Load all habits associated with a specific user.
    Parameters:
        user_id (int): The ID of the user whose habits will be retrieved.
    Returns:
        List[Dict]: A list of habit records as dictionaries.
    """
    conn = get_connection()
    # This allows access to row data as dictionaries
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Fetch all habits for the given user
    cursor.execute("SELECT * FROM Habit WHERE user_id = ?", (user_id,))
    habits = cursor.fetchall()
    conn.close()
    return [dict(row) for row in habits]


def save_checkoff(habit_id, user_id):
    """
    Log a check-off for a habit in the Habit_Logs table.
    Parameters:
        habit_id (int): The ID of the habit being checked off.
        user_id (int): The ID of the user completing the check-off.
    Note:
        The 'missed' field is defaulted to 0, meaning not missed.
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Insert a new check-off log with current timestamp
    cursor.execute("""
        INSERT INTO Habit_Logs (habit_id, user_id, completed_at, missed)
        VALUES (?, ?, ?, 0)
    """, (habit_id, user_id, datetime.now()))
    conn.commit()
    conn.close()

def load_checkoffs_for_habit(habit_id):
    """
    Load all check-off logs for a specific habit, ordered by completion time.
    Parameters:
        habit_id (int): The ID of the habit whose logs are to be loaded.
    Returns:
        List[Dict]: A list of log records as dictionaries, ordered by most recent first.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Select all logs related to the given habit
    cursor.execute("""
        SELECT * FROM Habit_Logs
        WHERE habit_id = ?
        ORDER BY completed_at DESC
    """, (habit_id,))
    logs = cursor.fetchall()
    conn.close()
    return [dict(row) for row in logs]

def check_if_missed(habit_id, deadline_time):
    """
    Check if a habit was missed by comparing the last check-off time with the deadline.
    Parameters:
        habit_id (int): The ID of the habit to check.
    deadline_time (datetime): The expected completion deadline.
    Returns:
        bool: True if the habit was missed (no check-offs or too late), False otherwise.
        :param habit_id:
        :param deadline_time:
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Fetch the most recent check-off timestamp
    cursor.execute("""
        SELECT completed_at FROM Habit_Logs
        WHERE habit_id = ?
        ORDER BY completed_at DESC
        LIMIT 1
    """, (habit_id,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        # No check-offs recorded → missed
        return True

    last_check_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")

    # Missed if the last check-off was *after* the deadline
    return last_check_time > deadline_time