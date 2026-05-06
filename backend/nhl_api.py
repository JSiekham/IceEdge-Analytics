"""
nhl_api.py

Handles pulling NHL data from the API and saving it into the database.
This is basically the data ingestion part of the project.
"""

import requests

from database import create_tables, get_connection

# Base URL for NHL API
BASE_URL = "https://api-web.nhle.com/v1"

# List of teams we want to pull data for (can expand later)
TEAMS = [
    "VAN", "EDM", "TOR", "BOS", "COL",
    "VGK", "NYR", "LAK", "DAL", "CAR"
]


def get_today_scores():
    """
    Fetch today's games from the NHL API.
    """
    url = f"{BASE_URL}/score/now"

    # Make API request
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Return just the list of games
    return response.json()["games"]


def get_team_schedule(team_abbrev, season):
    """
    Fetch the full season schedule for a specific team.

    Args:
        team_abbrev (str): Team abbreviation (e.g. VAN, TOR)
        season (int): NHL season (e.g. 20252026)

    Returns:
        list: List of game dictionaries
    """
    url = f"{BASE_URL}/club-schedule-season/{team_abbrev}/{season}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.json()["games"]


def save_games_to_db(games):
    """
    Save a list of games into the database.

    Only completed games are stored, since those are what we need for ML.
    """
    # Make sure tables exist before inserting
    create_tables()

    conn = get_connection()
    cursor = conn.cursor()

    for game in games:
        # Skip games that haven't finished yet
        if game.get("gameState") != "OFF":
            continue

        game_id = game["id"]
        season = game.get("season")
        game_date = game.get("gameDate")
        game_type = game.get("gameType")

        home_team = game["homeTeam"]["abbrev"]
        away_team = game["awayTeam"]["abbrev"]

        home_score = game["homeTeam"].get("score")
        away_score = game["awayTeam"].get("score")

        game_state = game.get("gameState")

        # Skip anything missing scores (just in case)
        if home_score is None or away_score is None:
            continue

        # Create target variables for ML
        home_win = 1 if home_score > away_score else 0
        winner = home_team if home_win == 1 else away_team

        # Insert or update game in database
        cursor.execute("""
            INSERT OR REPLACE INTO games (
                id, season, game_date, game_type,
                home_team, away_team,
                home_score, away_score, game_state,
                home_win, winner
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game_id, season, game_date, game_type,
            home_team, away_team,
            home_score, away_score, game_state,
            home_win, winner
        ))

    conn.commit()
    conn.close()


def main():
    """
    Main ingestion loop.

    Pulls schedule data for multiple teams and saves it to the database.
    """
    season = 20252026
    total_games = 0

    for team in TEAMS:
        print(f"Fetching {team}...")

        games = get_team_schedule(team, season)

        # Save games for this team
        save_games_to_db(games)

        total_games += len(games)

    print(f"Saved {total_games} games to database.")


if __name__ == "__main__":
    # Run this file directly to populate the database
    main()