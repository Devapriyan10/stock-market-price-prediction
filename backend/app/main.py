from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, stocks, portfolio  # import your routers

app = FastAPI()

# CORS middleware setup (for frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routes
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["Portfolio"])

# Optional root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Market Prediction System API"}
