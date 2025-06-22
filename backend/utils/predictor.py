# predictor.py
import joblib
import pandas as pd
import os

MODEL_DIR = "ml_models"
DATA_DIR = "data/historical_data"

def load_model(company_name):
    model_path = os.path.join(MODEL_DIR, f"{company_name.replace(' ', '_')}_model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found for {company_name}")
    return joblib.load(model_path)

def get_current_price(company_name):
    csv_path = os.path.join(DATA_DIR, f"{company_name.replace(' ', '_')}.csv")
    df = pd.read_csv(csv_path)
    return df["Close"].iloc[-1]  # last known closing price

def predict_future_price(company_name, target_year):
    model = load_model(company_name)
    prediction = model.predict([[target_year]])[0][0]
    return round(prediction, 2)

def get_recommendation(current_price, predicted_price):
    change = (predicted_price - current_price) / current_price
    if change > 0.15:
        return "Strong Buy"
    elif change > 0.05:
        return "Buy"
    elif change > -0.05:
        return "Hold"
    else:
        return "Sell"

def predict_and_recommend(company_name, target_year):
    current_price = get_current_price(company_name)
    predicted_price = predict_future_price(company_name, target_year)
    recommendation = get_recommendation(current_price, predicted_price)

    return {
        "company": company_name,
        "target_year": target_year,
        "current_price": round(current_price, 2),
        "predicted_price": predicted_price,
        "recommendation": recommendation
    }

# Example usage:
if __name__ == "__main__":
    result = predict_and_recommend("TCS", 2026)
    print(result)
