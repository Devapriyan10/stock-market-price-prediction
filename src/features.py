# src/features.py
import os
import argparse
import glob

import pandas as pd
import numpy as np
from ta import add_all_ta_features
from ta.utils import dropna


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input: df with columns ['Open','High','Low','Close','Volume']
    Output: df with new columns for:
      - Technical indicators (RSI, MACD, Bollinger Bands…)
      - Rolling stats (mean, std)
      - Lagged returns
    """
    # 1. Clean any residual NaNs
    df = dropna(df)

    # 2. Add all built-in technical indicators
    df = add_all_ta_features(
        df,
        open="Open",
        high="High",
        low="Low",
        close="Close",
        volume="Volume",
        fillna=True
    )

    # 3. Compute returns and rolling statistics
    df["Return"] = df["Close"].pct_change()
    df["RollMean_5"] = df["Return"].rolling(window=5).mean().fillna(0)
    df["RollStd_5"] = df["Return"].rolling(window=5).std().fillna(0)

    # 4. Create lag features
    for lag in [1, 2, 5, 10]:
        df[f"Return_lag_{lag}"] = df["Return"].shift(lag).fillna(0)

    # 5. Drop any rows with NaNs introduced by shifts
    df = df.dropna()

    return df


def find_cleaned_file(ticker: str) -> str:
    """Find the cleaned CSV for a ticker, handling different naming conventions."""
    # Preferred exact match
    exact = f"data/processed/{ticker}_clean.csv"
    if os.path.exists(exact):
        return exact
    # Fallback to any file starting with ticker_
    pattern = f"data/processed/{ticker}_*.csv"
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No processed file found for ticker {ticker}")
    # Choose most recent file by modified time
    files.sort(key=os.path.getmtime)
    return files[-1]


def load_cleaned(ticker: str) -> pd.DataFrame:
    """Load cleaned price data from CSV, auto-detecting filename."""
    path = find_cleaned_file(ticker)
    print(f"Loading cleaned data from {path}")
    df = pd.read_csv(path, index_col=0, parse_dates=True)

    # Convert OHLCV to float (fixes string error)
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df



def save_features(df: pd.DataFrame, ticker: str):
    """Save engineered features to disk."""
    os.makedirs("data/features", exist_ok=True)
    path = f"data/features/{ticker}_features.csv"
    df.to_csv(path)
    print(f"Features saved to {path}")


def main(tickers):
    for ticker in tickers:
        print(f"Processing features for {ticker}...")
        df_clean = load_cleaned(ticker)
        df_feat = create_features(df_clean)
        save_features(df_feat, ticker)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate technical and statistical features from cleaned price data."
    )
    parser.add_argument(
        "--tickers", nargs="+", required=True,
        help="Ticker symbols to process, e.g. AAPL MSFT GOOGL"
    )
    args = parser.parse_args()
    main(args.tickers)
