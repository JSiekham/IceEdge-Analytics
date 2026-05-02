import requests

from database import create_tables, get_connection

BASE_URL = "https://api-web.nhle.com/v1"


def get_today_scores():
    url = f"{BASE_URL}/score/now"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def save_games_to_db(data):
    create_tables()

    conn = get_connection()
    cursor = conn.cursor()

    for game in data.get("games", []):
        game_id = game["id"]
        season = game.get("season")
        game_date = game.get("gameDate")
        game_type = game.get("gameType")
        home_team = game["homeTeam"]["abbrev"]
        away_team = game["awayTeam"]["abbrev"]
        home_score = game["homeTeam"].get("score")
        away_score = game["awayTeam"].get("score")
        game_state = game.get("gameState")

        cursor.execute("""
            INSERT OR REPLACE INTO games (
                id, season, game_date, game_type,
                home_team, away_team,
                home_score, away_score, game_state
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game_id, season, game_date, game_type,
            home_team, away_team, home_score, away_score, game_state
        ))

    conn.commit()
    conn.close()


def main():
    data = get_today_scores()
    save_games_to_db(data)
    print("Today's games saved to database.")


if __name__ == "__main__":
    main()