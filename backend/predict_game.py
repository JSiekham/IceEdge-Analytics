"""
predict_game.py

Loads the trained model and makes a simple prediction for a matchup.
"""

import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "models" / "home_win_model.pkl"


def load_model():
    """
    Load the saved prediction model from the models folder.
    """
    return joblib.load(MODEL_PATH)


def predict_home_win(home_last5_win_rate, away_last5_win_rate, home_last5_goal_diff, away_last5_goal_diff):
    """
    Predict whether the home team will win using recent team form stats.
    """
    model = load_model()

    game_features = pd.DataFrame([{
        "home_last5_win_rate": home_last5_win_rate,
        "away_last5_win_rate": away_last5_win_rate,
        "home_last5_goal_diff": home_last5_goal_diff,
        "away_last5_goal_diff": away_last5_goal_diff,
    }])

    prediction = model.predict(game_features)[0]
    probability = model.predict_proba(game_features)[0]

    return prediction, probability


def main():
    """
    Quick test prediction.
    """
    prediction, probability = predict_home_win(
        home_last5_win_rate=0.60,
        away_last5_win_rate=0.40,
        home_last5_goal_diff=1.2,
        away_last5_goal_diff=-0.4,
    )

    if prediction == 1:
        print("Prediction: Home team wins")
    else:
        print("Prediction: Away team wins")

    print(f"Home win probability: {probability[1]:.2%}")
    print(f"Away win probability: {probability[0]:.2%}")


if __name__ == "__main__":
    main()