import os
import pandas as pd

PORTFOLIO_DIR = "data/user_portfolios"

def save_to_portfolio(username, result):
    os.makedirs(PORTFOLIO_DIR, exist_ok=True)
    user_file = os.path.join(PORTFOLIO_DIR, f"{username}.csv")
    df = pd.DataFrame([result])
    if os.path.exists(user_file):
        existing = pd.read_csv(user_file)
        df = pd.concat([existing, df], ignore_index=True)
    df.to_csv(user_file, index=False)
