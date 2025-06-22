# fetch_data.py
import yfinance as yf
import pandas as pd
import os

DATA_DIR = "data/historical_data"

def fetch_stock_data(ticker, company_name, start="2019-01-01", end="2024-01-01"):
    try:
        df = yf.download(ticker, start=start, end=end)
        if not df.empty:
            os.makedirs(DATA_DIR, exist_ok=True)
            filename = f"{company_name.replace(' ', '_')}.csv"
            path = os.path.join(DATA_DIR, filename)
            df.to_csv(path)
            print(f"[✔] Data saved for {company_name} at {path}")
        else:
            print(f"[!] No data found for {company_name} ({ticker})")
    except Exception as e:
        print(f"[✘] Failed to fetch data for {company_name}: {e}")

def fetch_all():
    df = pd.read_csv("data/company_list.csv")
    for _, row in df.iterrows():
        fetch_stock_data(row["Ticker Symbol"], row["Company Name"])

if __name__ == "__main__":
    fetch_all()
