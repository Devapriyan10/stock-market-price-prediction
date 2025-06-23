import yfinance as yf
import pandas as pd
import joblib
from prophet import Prophet
import os, csv

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# Load tickers
with open(os.path.join(os.getcwd(), "data/companies.csv")) as f:
    reader = csv.DictReader(f)
    tickers = [r["ticker"] for r in reader]

for ticker in tickers:
    try:
        # Download
        df = yf.download(f"{ticker}.NS", period="5y", interval="1d")

        # Skip if empty
        if df.empty:
            print(f"Skipping {ticker}: Downloaded data is empty")
            continue

        # Handle MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            # Confirm 'Close' exists in the first level
            if "Close" not in df.columns.get_level_values(0):
                print(f"Skipping {ticker}: 'Close' not in columns")
                continue
            # Extract just the Close series
            df = df["Close"].reset_index()
            df.columns = ["ds", "y"]
        else:
            if "Close" not in df.columns:
                print(f"Skipping {ticker}: 'Close' not found")
                continue
            df = df.reset_index()[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"})

        # Ensure numeric y
        df["y"] = pd.to_numeric(df["y"], errors="coerce")

        # Debug output (optional)
        print(f"\nTicker: {ticker}")
        print(df.head())
        print(df.dtypes)

        # Skip if no valid y
        if df["y"].dropna().empty:
            print(f"Skipping {ticker}: 'y' column is all NaNs")
            continue

        # Train & save
        m = Prophet()
        m.fit(df)
        joblib.dump(m, os.path.join(MODEL_DIR, f"{ticker}.pkl"))
        print(f"✅ Saved model for {ticker}")

    except Exception as e:
        print(f"❌ Error processing {ticker}: {e}")
