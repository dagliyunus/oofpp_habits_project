from config.db_config import get_connection


def sign_up(username, email, password):
    """
    Register a new user in the system. Checks whether the given username already exists.
    If not, inserts the new user into the User table.
    Parameters:
        username (str): Desired username.
        email (str): User's email address.
        password (str): User's password (should be hashed in production).
    Returns:
        Tuple[Optional[int], str]: A tuple containing the new user's ID (or None if failed),
                                   and a status message.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if username exists
    cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return None, "❌ Username already exists."

    # Inserting new user here
    cursor.execute(
        "INSERT INTO User (username, email, password) VALUES (?, ?, ?)",
        (username, email, password)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id, "✅ User registered successfully."


def log_in(username, password):
    """
    Authenticate a user based on username and password.
    Parameters:
        username (str): The user's username.
        password (str): The password to verify (plain text comparison — NOT secure).
    Returns:
        Tuple[Optional[int], str]: A tuple with the user's ID if authenticated, and a status message.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch user credentials from the database
    cursor.execute("SELECT user_id, password FROM User WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None, "❌ User not found."
    if row[1] != password:
        return None, "❌ Incorrect password."

    return row[0], "✅ Logged in successfully."