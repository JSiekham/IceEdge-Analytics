"""
view_games.py

Simple script to read and display games from the database.
Mainly used to quickly check that data is being saved correctly.
"""

from database import get_connection


def view_games():
    """
    Fetch and print games from the database in a readable format.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Pull game data, newest games first
    cursor.execute("""
        SELECT id, game_date, away_team, away_score, home_team, home_score, game_state, winner
        FROM games
        ORDER BY game_date DESC
    """)

    games = cursor.fetchall()
    conn.close()

    # If nothing is in the table yet
    if not games:
        print("No games found in database.")
        return

    # Loop through results and print them nicely
    for game in games:
        game_id, date, away, away_score, home, home_score, state, winner = game

        print(
            f"{date} | {away} {away_score} @ {home} {home_score} | "
            f"{state} | Winner: {winner} | ID: {game_id}"
        )


if __name__ == "__main__":
    # Run this file to quickly inspect what’s in the database
    view_games()