# src/model_baseline.py
import os
import argparse
import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns


def load_features(ticker: str) -> pd.DataFrame:
    path = f"data/features/{ticker}_features.csv"
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    return df


def train_model(df: pd.DataFrame):
    # Define X, y (predicting next day's close or return)
    df = df.copy()
    df["Target"] = df["Close"].pct_change().shift(-1)
    df.dropna(inplace=True)

    X = df.drop(columns=["Target"])
    y = df["Target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    
    print("MAE:", mean_absolute_error(y_test, preds))
    print("RMSE:", np.sqrt(mean_squared_error(y_test, preds)))
    print("R2:", r2_score(y_test, preds))

    return model, X_test, y_test, preds


def plot_predictions(y_test, preds, ticker):
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=y_test.index, y=y_test.values, label="Actual")
    sns.lineplot(x=y_test.index, y=preds, label="Predicted")
    plt.title(f"Actual vs Predicted for {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Next Day Return")
    plt.legend()
    plt.tight_layout()
    os.makedirs("plots", exist_ok=True)
    plt.savefig(f"plots/{ticker}_predictions.png")
    plt.close()


def main(ticker):
    df = load_features(ticker)
    model, X_test, y_test, preds = train_model(df)
    joblib.dump(model, f"models/{ticker}_model.pkl")
    print(f"Model saved to models/{ticker}_model.pkl")
    plot_predictions(y_test, preds, ticker)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", type=str, required=True)
    args = parser.parse_args()
    os.makedirs("models", exist_ok=True)
    main(args.ticker)
