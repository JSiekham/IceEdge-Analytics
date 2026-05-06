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


def main():
    """
    Quick test file for checking feature creation.
    """
    from create_dataset import load_games

    df = load_games()
    df = add_basic_features(df)

    print(df.head())
    print()
    print("Columns:", list(df.columns))


if __name__ == "__main__":
    main()