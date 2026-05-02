import requests

BASE_URL = "https://api-web.nhle.com/v1"


def get_today_scores():
    url = f"{BASE_URL}/score/now"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def print_today_games():
    data = get_today_scores()

    games = data.get("games", [])

    if not games:
        print("No NHL games found today.")
        return

    for game in games:
        away = game["awayTeam"]["abbrev"]
        home = game["homeTeam"]["abbrev"]
        state = game.get("gameState", "Unknown")

        print(f"{away} at {home} - {state}")


if __name__ == "__main__":
    print_today_games()