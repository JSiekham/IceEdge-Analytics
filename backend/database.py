"""
database.py

Handles creating and connecting to the SQLite database.
This is where all NHL game data gets stored for the project.
"""

import sqlite3
from pathlib import Path

# This sets the path to the database file inside the /data folder
DB_PATH = Path(__file__).parent.parent / "data" / "iceedge.db"


def get_connection():
    """
    Creates a connection to the SQLite database.

    Also makes sure the /data folder exists before trying to connect.
    """
    # Create the data folder if it doesn't exist yet
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Return a connection to the database file
    return sqlite3.connect(DB_PATH)


def create_tables():
    """
    Creates the main 'games' table if it doesn't already exist.

    This table stores all game-level data pulled from the NHL API.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # This is the main table for storing game results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            season INTEGER,
            game_date TEXT,
            game_type INTEGER,
            home_team TEXT,
            away_team TEXT,
            home_score INTEGER,
            away_score INTEGER,
            game_state TEXT,
            home_win INTEGER,
            winner TEXT
        )
    """)

    # Save changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Run this file directly to create the database and tables
    create_tables()
    print("Database and tables created successfully.")