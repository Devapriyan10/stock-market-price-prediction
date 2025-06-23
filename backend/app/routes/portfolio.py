from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app import schemas, models, auth
from .users_utils import get_user_by_email
from app.ml.predictor import predict_price

router = APIRouter()

@router.post("/", response_model=schemas.PortfolioOut)
def add_to_portfolio(
    req: schemas.PredictRequest,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    price = predict_price(req.ticker, req.year)
    entry = models.Portfolio(
        user_id=current_user.id,
        ticker=req.ticker,
        year=req.year,
        predicted_price=price
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/", response_model=List[schemas.PortfolioOut])
def list_portfolio(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    return db.query(models.Portfolio).filter(models.Portfolio.user_id == current_user.id).all()
