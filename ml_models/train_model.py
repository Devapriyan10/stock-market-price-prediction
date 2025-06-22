# ml_models/train_model.py
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import joblib

DATA_DIR = "data/historical_data"
MODEL_DIR = "ml_models"

def train_model(company_name):
    csv_path = os.path.join(DATA_DIR, f"{company_name}.csv")
    df = pd.read_csv(csv_path)

    # Extract year from date
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    yearly_avg = df.groupby("Year")["Close"].mean().reset_index()

    # Prepare training data
    X = yearly_avg[["Year"]]
    y = yearly_avg[["Close"]]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, f"{company_name}_model.pkl")
    joblib.dump(model, model_path)
    print(f"✅ Model saved to {model_path}")

if __name__ == "__main__":
    train_model("TCS")
