from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import yfinance as yf
import os
import json
import joblib

from app.routes.predict import router as predict_router  # Your predict.py router

# --------------------------------------
# Initialize the FastAPI app
# --------------------------------------
app = FastAPI(title="Stock Price Prediction API")

# Enable CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# --------------------------------------
# Load all trained models from /models/
# --------------------------------------
models_dir = os.path.join(os.path.dirname(__file__), "models")
models = {}

for filename in os.listdir(models_dir):
    if filename.endswith(".pkl"):
        ticker = filename.replace(".pkl", "")
        model_path = os.path.join(models_dir, filename)
        models[ticker] = joblib.load(model_path)

# Save to app state
app.state.models = models


# --------------------------------------
# Include route handlers
# --------------------------------------
app.include_router(predict_router, prefix="/api")

# --------------------------------------
# Pydantic schema for response
# --------------------------------------
class PredictionResponse(BaseModel):
    ticker: str
    year: int
    predicted_price: float


# --------------------------------------
# API: Get Companies List
# --------------------------------------
@app.get("/api/companies")
def get_companies():
    data_path = os.path.join(os.path.dirname(__file__), "data", "companies.json")
    try:
        with open(data_path, "r") as f:
            companies = json.load(f)
        return companies
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="companies.json not found")


# --------------------------------------
# API: Get Historical Stock Data
# --------------------------------------
@app.get("/api/historical")
def get_historical(ticker: str):
    try:
        df = yf.Ticker(ticker).history(period="5y")["Close"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch historical data: {str(e)}")

    records = [
        {"date": idx.strftime("%Y-%m-%d"), "close": float(val)}
        for idx, val in df.items()
    ]
    return records


# --------------------------------------
# API: Legacy Simple Prediction (optional fallback)
# --------------------------------------
@app.get("/api/predict-simple", response_model=PredictionResponse)
def predict_price(ticker: str, year: int):
    models = app.state.models
    if ticker not in models:
        raise HTTPException(status_code=404, detail=f"No model found for ticker '{ticker}'")

    model = models[ticker]

    try:
        # Adjust this feature engineering as per training
        future_days = (year - 2024) * 252
        pred = model.predict([[future_days]])[0]
    except Exception:
        raise HTTPException(status_code=500, detail="Model prediction failed")

    return PredictionResponse(
        ticker=ticker,
        year=year,
        predicted_price=round(float(pred), 2)
    )
