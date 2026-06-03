"""
train_model.py

Trains a machine learning model to predict whether the home team wins.
This version uses a time-based train/test split, which is more realistic
for sports prediction.
"""

import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from create_dataset import load_games
from features import add_basic_features, add_rolling_features

MODEL_PATH = Path(__file__).parent.parent / "models" / "home_win_model.pkl"

def train_model():
    """
    Load games, create features, train the model, and print evaluation results.
    """
    df = load_games()

    # Make sure games are sorted by date before splitting
    df = df.sort_values("game_date")

    # Add feature columns
    df = add_basic_features(df)
    df = add_rolling_features(df)

    feature_columns = [
        "home_last5_win_rate",
        "away_last5_win_rate",
        "home_last5_goal_diff",
        "away_last5_goal_diff",
    ]

    X = df[feature_columns]
    y = df["home_win"]

    # Use the first 75% of games for training and the last 25% for testing
    split_index = int(len(df) * 0.75)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")

    predictions = model.predict(X_test)

    print("Model accuracy:", accuracy_score(y_test, predictions))
    print()
    print(classification_report(y_test, predictions))


if __name__ == "__main__":
    train_model()