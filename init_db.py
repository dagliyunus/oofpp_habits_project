# init_db.py
from config.db_config import get_connection

def initialize_schema():
    """
    Initialize the SQLite database using the schema SQL file.
    Parameters:
    file_path (str): Path to the SQL schema file. Defaults to 'db/habits.sql'.

    This function reads the SQL schema from the specified file
    and executes it against the connected database.
    """
    with open("db/habits.sql", "r") as f:
        schema = f.read()
    conn = get_connection()
    cursor = conn.cursor()
    # Executing here full schema script (CREATE TABLE, etc.)
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("✅ Database initialized: habits.db")

if __name__ == "__main__":
    initialize_schema()