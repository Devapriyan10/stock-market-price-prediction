import os
import json
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

DATA_FILE = "app/data/companies.json"
MODEL_DIR = "app/models"

def load_companies():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def train_model_for_company(ticker):
    print(f"[+] Training model for: {ticker}")
    try:
        df = yf.download(ticker, period="5y", interval="1d", progress=False)

        if df.empty or 'Close' not in df.columns:
            print(f"[-] No data for {ticker}")
            return

        df = df[['Close']].dropna().reset_index()
        df['Day'] = (df.index + 1)

        X = df[['Day']]
        y = df['Close']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        model = LinearRegression()
        model.fit(X_train, y_train)

        os.makedirs(MODEL_DIR, exist_ok=True)
        model_file = os.path.join(MODEL_DIR, f"{ticker}.pkl")
        joblib.dump(model, model_file)

        print(f"[✓] Model saved: {model_file}")

    except Exception as e:
        print(f"[!] Error training {ticker}: {e}")

def main():
    companies = load_companies()
    for company in companies:
        train_model_for_company(company["ticker"])

if __name__ == "__main__":
    main()
