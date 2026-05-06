"""
train_model.py

Trains a basic machine learning model to predict whether the home team wins.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from create_dataset import load_games
from features import add_basic_features, add_rolling_features


def train_model():
    """
    Load games, create features, train a model, and print results.
    """
    df = load_games()

    # Add our feature columns
    df = add_basic_features(df)
    df = add_rolling_features(df)

    # These are the columns the model will learn from
    feature_columns = [
        "home_last5_win_rate",
        "away_last5_win_rate",
        "home_last5_goal_diff",
        "away_last5_goal_diff",
    ]

    X = df[feature_columns]
    y = df["home_win"]

    # Split data into training and testing sets
    # random_state makes the results repeatable
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    # Random Forest is a good starter model because it handles small datasets well
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predict on games the model has not seen during training
    predictions = model.predict(X_test)

    print("Model accuracy:", accuracy_score(y_test, predictions))
    print()
    print(classification_report(y_test, predictions))


if __name__ == "__main__":
    train_model()