# ml_models/train_all_models.py
import os
from train_model import train_model

DATA_DIR = "data/historical_data"

def train_all():
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".csv"):
            company = filename.replace(".csv", "")
            try:
                train_model(company)
            except Exception as e:
                print(f"⚠️ Failed to train for {company}: {e}")

if __name__ == "__main__":
    train_all()
