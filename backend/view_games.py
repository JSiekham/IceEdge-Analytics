from database import get_connection


def view_games():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, game_date, away_team, away_score, home_team, home_score, game_state
        FROM games
        ORDER BY game_date DESC
    """)

    games = cursor.fetchall()
    conn.close()

    if not games:
        print("No games found in database.")
        return

    for game in games:
        game_id, date, away, away_score, home, home_score, state = game
        print(f"{date} | {away} {away_score} @ {home} {home_score} | {state} | ID: {game_id}")


if __name__ == "__main__":
    view_games()