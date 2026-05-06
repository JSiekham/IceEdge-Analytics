"""
features.py

Creates ML features from the raw game results.
This is where basic scores are turned into useful hockey stats.
"""

import pandas as pd


def add_basic_features(df):
    """
    Add simple game-level features.

    These are not predictions yet — they are extra columns that help
    the ML model understand each game better.
    """
    df = df.copy()

    # Goal difference from the home team's point of view
    df["home_goal_diff"] = df["home_score"] - df["away_score"]

    # Total goals in the game
    df["total_goals"] = df["home_score"] + df["away_score"]

    return df

def add_rolling_features(df):
    """
    Create rolling stats for each team based on their last 5 games.
    """
    df = df.copy()

    # Sort by date so everything is in chronological order
    df = df.sort_values("game_date")

    # Store rolling stats here
    home_last5_win_rate = []
    away_last5_win_rate = []

    home_last5_goal_diff = []
    away_last5_goal_diff = []

    # Track each team's history
    team_history = {}

    for _, row in df.iterrows():
        home = row["home_team"]
        away = row["away_team"]

        # Initialize if team not seen yet
        if home not in team_history:
            team_history[home] = []

        if away not in team_history:
            team_history[away] = []

        # Get last 5 games for each team
        home_last5 = team_history[home][-5:]
        away_last5 = team_history[away][-5:]

        # --- HOME TEAM FEATURES ---
        if len(home_last5) > 0:
            wins = sum(g["win"] for g in home_last5)
            goal_diff = sum(g["goal_diff"] for g in home_last5)

            home_last5_win_rate.append(wins / len(home_last5))
            home_last5_goal_diff.append(goal_diff / len(home_last5))
        else:
            home_last5_win_rate.append(0)
            home_last5_goal_diff.append(0)

        # --- AWAY TEAM FEATURES ---
        if len(away_last5) > 0:
            wins = sum(g["win"] for g in away_last5)
            goal_diff = sum(g["goal_diff"] for g in away_last5)

            away_last5_win_rate.append(wins / len(away_last5))
            away_last5_goal_diff.append(goal_diff / len(away_last5))
        else:
            away_last5_win_rate.append(0)
            away_last5_goal_diff.append(0)

        # --- UPDATE HISTORY AFTER USING IT ---
        home_win = row["home_win"]

        # Store results from each team's perspective
        team_history[home].append({
            "win": home_win,
            "goal_diff": row["home_score"] - row["away_score"]
        })

        team_history[away].append({
            "win": 1 - home_win,
            "goal_diff": row["away_score"] - row["home_score"]
        })

    # Add new columns to dataframe
    df["home_last5_win_rate"] = home_last5_win_rate
    df["away_last5_win_rate"] = away_last5_win_rate
    df["home_last5_goal_diff"] = home_last5_goal_diff
    df["away_last5_goal_diff"] = away_last5_goal_diff

    return df


def main():
    from create_dataset import load_games

    df = load_games()

    df = add_basic_features(df)
    df = add_rolling_features(df)

    print(df.tail(20))
    print()
    print("Columns:", list(df.columns))


if __name__ == "__main__":
    main()