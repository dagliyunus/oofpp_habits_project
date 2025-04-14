import json
from datetime import datetime
from config.db_config import get_connection


def load_fixtures():
    """
    Load initial fixture data into the database from a JSON file.
    This function inserts users, habits, and habit logs from the given fixture file.
    It checks for duplication by verifying whether the user already exists.
    Parameters:
    file_path (str): Path to the fixture JSON file. Defaults to 'db/fixtures.json'.
    Raises:
    FileNotFoundError: If the JSON fixture file is missing.
    KeyError: If required keys like 'user', 'habits', or 'habit_logs' are missing.
    """
    # Load fixture data
    with open("db/fixtures.json", "r") as f:
        data = json.load(f)

    conn = get_connection()
    cursor = conn.cursor()

    # Here checking if user already exists
    cursor.execute("SELECT COUNT(*) FROM User WHERE user_id = ?", (data["user"]["user_id"],))
    if cursor.fetchone()[0] > 0:
        print("ℹ️ Fixtures already loaded. Skipping.")
        conn.close()
        return

    print("📦 Loading fixtures...")

    # Inserting user
    user = data["user"]
    cursor.execute("""
        INSERT INTO User (user_id, username, email, password)
        VALUES (?, ?, ?, ?)
    """, (
        user["user_id"],
        user["username"],
        user["email"],
        user["password"]
    ))

    # Inserting habits
    for habit in data["habits"]:
        cursor.execute("""
            INSERT INTO Habit (habit_id, user_id, name, frequency, description, deadline_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            habit["habit_id"],
            habit["user_id"],
            habit["name"],
            habit["frequency"],
            habit["description"],
            habit["deadline_time"],
            datetime.now()
        ))

    # Inserting logs
    for log in data["habit_logs"]:
        cursor.execute("""
            INSERT INTO Habit_Logs (habit_id, user_id, completed_at, note, missed)
            VALUES (?, ?, ?, ?, ?)
        """, (
            log["habit_id"],
            log["user_id"],
            log["completed_at"],
            log.get("note", ""),
            log.get("missed", 0)
        ))

    conn.commit()
    conn.close()
    print("✅ Fixtures loaded successfully!")