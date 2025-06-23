from pydantic import BaseModel, EmailStr
from typing import List

# USER
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# COMPANY
class CompanyOut(BaseModel):
    ticker: str
    name: str
    class Config:
        orm_mode = True

# PREDICT
class PredictRequest(BaseModel):
    ticker: str
    year: int

class PredictResponse(BaseModel):
    ticker: str
    year: int
    predicted_price: float

# PORTFOLIO
class PortfolioOut(BaseModel):
    id: int
    ticker: str
    year: int
    predicted_price: float
    class Config:
        orm_mode = True
# STOCK HISTORY
class StockData(BaseModel):
    date: str
    price: float

class StockHistoryResponse(BaseModel):
    ticker: str
    history: List[StockData]
