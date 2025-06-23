from fastapi import APIRouter, HTTPException
from typing import List
import csv
import os
import pandas as pd
from app import schemas
from app.ml.predictor import predict_price

router = APIRouter()

@router.get("/", response_model=List[schemas.CompanyOut])
def list_companies():
    companies = []
    with open("data/companies.csv") as f:
        reader = csv.DictReader(f)
        for r in reader:
            companies.append({"ticker": r["ticker"], "name": r["name"]})
    return companies

@router.post("/predict", response_model=schemas.PredictResponse)
def predict_stock(req: schemas.PredictRequest):
    price = predict_price(req.ticker, req.year)
    return {"ticker": req.ticker, "year": req.year, "predicted_price": price}

@router.get("/history/{ticker}", response_model=schemas.StockHistoryResponse)
def stock_history(ticker: str):
    filepath = f"backend/data/history/{ticker}.csv"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Stock history not found")
    with open(filepath) as f:
        reader = csv.DictReader(f)
        history = [{"date": row["date"], "price": float(row["price"])} for row in reader]
    return {"ticker": ticker, "history": history}
    df = pd.read_csv(file_path)
    if 'Date' not in df.columns or 'Close' not in df.columns:
        raise HTTPException(status_code=500, detail="Invalid file format")

    history = [
        {"date": row["Date"], "price": row["Close"]}
        for _, row in df.iterrows()
    ]
    return {"ticker": ticker, "history": history}
