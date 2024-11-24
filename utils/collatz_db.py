import os
import sqlite3
from utils.orbit_info import OrbitInfo  # Ensure the OrbitInfo class is defined in orbit_info.py

def initialize_db_and_create_table():
    # Ensure the 'db' folder exists
    db_folder = "db"
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    # SQLite database file path
    db_path = os.path.join(db_folder, "orbit_info.db")

    # Connect to SQLite database (it will be created if it doesn't exist)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create a table for OrbitInfo
    create_table_query = """
    CREATE TABLE IF NOT EXISTS OrbitInfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_drop INTEGER NOT NULL,
        first_orbit TEXT NOT NULL,
        total_orbit TEXT NOT NULL,
        stop_mod INTEGER NOT NULL,
        stop_index INTEGER NOT NULL,
        n INTEGER NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

    print(f"Database initialized and table created (if not already present) at: {db_path}")
