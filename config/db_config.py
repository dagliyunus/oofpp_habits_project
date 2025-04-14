# config/db_config.py
import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
# Get the path to the SQLite database from environment, or use default
DB_PATH = os.getenv("DB_PATH", "./db/habits.db")

def get_connection():
    """
    Establish a connection to the SQLite database.
    Returns:
        sqlite3.Connection: A connection object to the specified SQLite database,
        with type detection enabled for better datetime parsing and column name support.
    """
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)