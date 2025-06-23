from fastapi import APIRouter, Request, HTTPException, Query
from datetime import datetime
import yfinance as yf
import logging

router = APIRouter()

@router.get("/predict")
async def predict_price(
    request: Request,
    ticker: str = Query(..., description="Ticker symbol like RELIANCE.NS"),
    year: int = Query(..., description="Year to predict for, e.g. 2026")
):
    models = request.app.state.models

    if ticker not in models:
        raise HTTPException(status_code=404, detail=f"Model for '{ticker}' not found")

    model = models[ticker]

    try:
        # Calculate number of trading days into the future
        years_from_now = year - datetime.now().year
        if years_from_now < 0:
            raise HTTPException(status_code=400, detail="Cannot predict for past years")

        future_day = years_from_now * 252  # Approx. trading days per year

        # Predict future price using the ML model
        predicted_price = float(model.predict([[future_day]])[0])

        # Fetch current price using Yahoo Finance
        data = yf.download(ticker, period="1d", progress=False)
        if data.empty:
            raise HTTPException(status_code=404, detail=f"Failed to fetch current price for '{ticker}'")
        current_price = float(data["Close"].iloc[-1])

        return {
            "ticker": ticker,
            "year": year,
            "predictedPrice": round(predicted_price, 2),
            "currentPrice": round(current_price, 2),
            "confidence": 90,  # Placeholder
            "createdAt": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise  # Re-raise known HTTP exceptions
    except Exception as e:
        logging.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
