import requests

from database import create_tables, get_connection

BASE_URL = "https://api-web.nhle.com/v1"

TEAMS = [
    "VAN", "EDM", "TOR", "BOS", "COL",
    "VGK", "NYR", "LAK", "DAL", "CAR"
]

def get_today_scores():
    url = f"{BASE_URL}/score/now"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["games"]

def get_team_schedule(team_abbrev, season):
    url = f"{BASE_URL}/club-schedule-season/{team_abbrev}/{season}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["games"]

def save_games_to_db(games):
    create_tables()

    conn = get_connection()
    cursor = conn.cursor()

    for game in games:
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

        if home_score is None or away_score is None:
            continue

        home_win = 1 if home_score > away_score else 0
        winner = home_team if home_win == 1 else away_team

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
    season = 20252026

    total_games = 0

    for team in TEAMS:
        print(f"Fetching {team}...")
        games = get_team_schedule(team, season)
        save_games_to_db(games)
        total_games += len(games)

    print(f"Saved {total_games} games to database.")

if __name__ == "__main__":
    main()