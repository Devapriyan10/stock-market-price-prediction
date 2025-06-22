from fastapi import FastAPI, Form
from backend.auth.auth_manager import login_user, register_user
from backend.utils.predictor import predict_and_recommend

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to SMPS API"}
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if login_user(username, password):
        return {"success": True}
    return {"success": False, "error": "Invalid credentials"}

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    success, msg = register_user(username, password)
    return {"success": success, "message": msg}

@app.post("/predict")
def predict(company: str = Form(...), year: int = Form(...)):
    result = predict_and_recommend(company, year)
    return result
