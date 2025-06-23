from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    portfolios = relationship("Portfolio", back_populates="owner")

class Company(Base):
    __tablename__ = "companies"
    ticker = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ticker = Column(String, ForeignKey("companies.ticker"))
    year = Column(Integer, nullable=False)
    predicted_price = Column(Float, nullable=False)
    owner = relationship("User", back_populates="portfolios")
    company = relationship("Company")
