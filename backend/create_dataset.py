"""
create_dataset.py

Loads completed NHL games from the database and turns them into
a dataset used for machine learning.
"""

import pandas as pd
from database import get_connection


def load_games():
    """
    Pull completed games from the database.

    Returns:
        pd.DataFrame with game data (teams, scores, and target variable).
    """
    conn = get_connection()

    query = """
        SELECT
            id,
            season,
            game_date,
            home_team,
            away_team,
            home_score,
            away_score,
            home_win,
            winner
        FROM games
        WHERE game_state = 'OFF'
        ORDER BY game_date ASC
    """

    # Read SQL results straight into a DataFrame
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def main():
    """
    Quick check to make sure dataset looks right.
    """
    df = load_games()

    # Show a few rows to sanity check the data
    print("Preview of dataset:")
    print(df.head())
    print()

    # Total number of completed games
    print(f"Total completed games: {len(df)}")

    # What columns we have to work with
    print("Columns:", list(df.columns))


if __name__ == "__main__":
    # Run this file directly to inspect the dataset
    main()