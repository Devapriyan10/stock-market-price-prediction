import os
import pandas as pd
import yfinance as yf

TICKER_CSV = "data/company_list.csv"
OUTPUT_DIR = "data/historical_data"

def download_data(ticker, name):
    try:
        print(f"📥 Downloading: {name} ({ticker})")
        df = yf.Ticker(ticker).history(period="5y")
        if df.empty:
            print(f"⚠️ No data for {ticker}")
            return
        df.reset_index(inplace=True)  # ensure 'Date' column exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, f"{name.replace(' ', '_')}.csv")
        df.to_csv(output_path, index=False)
        print(f"✅ Saved to {output_path}")
    except Exception as e:
        print(f"❌ Failed for {ticker}: {e}")

def main():
    if not os.path.exists(TICKER_CSV):
        print(f"❌ Ticker list not found at: {TICKER_CSV}")
        return

    df = pd.read_csv(TICKER_CSV)

    for _, row in df.iterrows():
        company_name = row["Company Name"]
        ticker = row["Ticker Symbol"]
        download_data(ticker, company_name)

if __name__ == "__main__":
    main()
