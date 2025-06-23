from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, auth
from .users_utils import get_user_by_email, create_user

router = APIRouter()

@router.post("/register", response_model=schemas.Token)
def register(u: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    if get_user_by_email(db, u.email):
        raise HTTPException(400, "Email already registered")
    user = create_user(db, u)
    token = auth.create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = get_user_by_email(db, form.username)
    if not user or not auth.verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = auth.create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}
