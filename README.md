# SMPS — Stock Market Prediction System

Full-stack stock-price prediction web app:
- **Backend**: FastAPI, yfinance, Prophet, SQLite, Docker
- **Frontend**: React, Vite, TailwindCSS, Chart.js
- **Features**:  
  • User registration/login (JWT)  
  • Browse 250 Indian companies  
  • 5-year history chart  
  • Year-ahead prediction via Prophet  
  • Save predictions to personal portfolio  

## Setup

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
python -m app.ml.train          # trains & persists models
uvicorn app.main:app --reload
