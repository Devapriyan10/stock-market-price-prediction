import joblib, os
import pandas as pd
from datetime import datetime

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

def predict_price(ticker: str, year: int) -> float:
    path = os.path.join(MODEL_DIR, f"{ticker}.pkl")
    m = joblib.load(path)
    years_ahead = year - datetime.now().year
    future = m.make_future_dataframe(periods=years_ahead * 365, freq='D')
    fc = m.predict(future)
    target = fc[fc.ds.dt.year == year]
    if target.empty:
        raise ValueError("No data for that year")
    return round(float(target.yhat.values[-1]), 2)
