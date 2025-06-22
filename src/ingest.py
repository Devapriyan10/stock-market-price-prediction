# src/ingest.py
import os
import argparse
import logging
from datetime import datetime

import pandas as pd
import yfinance as yf
from dotenv import load_dotenv

#–– Load environment variables ––#
load_dotenv()  # reads .env into os.environ
ALPHA_VANTAGE_KEY = os.getenv("ALPHAVANTAGE_API_KEY")  # if you switch to Alpha Vantage later

#–– Logging setup ––#
LOG_FMT = "%(asctime)s %(levelname)s — %(message)s"
logging.basicConfig(
    filename="logs/ingest.log",
    level=logging.INFO,
    format=LOG_FMT
)
logger = logging.getLogger()


def fetch_yahoo(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download OHLCV via yfinance."""
    df = yf.download(ticker, start=start, end=end, progress=False)
    df.index = df.index.tz_localize(None)  # drop timezone info
    return df


def save_raw(df: pd.DataFrame, ticker: str):
    """Save raw DataFrame to CSV in data/raw/ with date stamp."""
    os.makedirs("data/raw", exist_ok=True)
    fname = f"data/raw/{ticker}_{datetime.today().date()}.csv"
    df.to_csv(fname)
    logger.info(f"Saved raw data to {fname}")


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and harmonize price DataFrame:
      1. Ensure business-day frequency
      2. Forward/backward fill small gaps
      3. Drop remaining NaNs in critical columns
    """
    # 1. Sort by date
    df = df.sort_index()

    # 2. Reindex to business-day frequency
    df = df.asfreq("B")  # introduces NaNs for missing days
    df.ffill(inplace=True)  # carry last valid observation forward
    df.bfill(inplace=True)  # back-fill leading NaNs if any

    # 3. Drop rows still containing NaNs in 'Close'
    df.dropna(subset=["Close"], inplace=True)
    return df


def save_clean(df: pd.DataFrame, ticker: str):
    """Save cleaned DataFrame to CSV in data/processed/."""
    os.makedirs("data/processed", exist_ok=True)
    fname = f"data/processed/{ticker}_clean.csv"
    df.to_csv(fname)
    logger.info(f"Saved cleaned data to {fname}")


def main(tickers, start, end):
    for ticker in tickers:
        try:
            # 1. Fetch raw data
            raw_df = fetch_yahoo(ticker, start, end)
            save_raw(raw_df, ticker)

            # 2. Clean and save processed data
            cleaned = clean_df(raw_df)
            save_clean(cleaned, ticker)

        except Exception as e:
            logger.error(f"Error processing {ticker}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest and clean stock price data.")
    parser.add_argument(
        "--tickers", nargs="+", required=True,
        help="List of ticker symbols to fetch (e.g. AAPL MSFT)."
    )
    parser.add_argument(
        "--start", type=str, default="2010-01-01",
        help="Start date in YYYY-MM-DD format."
    )
    parser.add_argument(
        "--end", type=str,
        default=datetime.today().strftime("%Y-%m-%d"),
        help="End date in YYYY-MM-DD format (default: today)."
    )
    args = parser.parse_args()

    main(args.tickers, args.start, args.end)
