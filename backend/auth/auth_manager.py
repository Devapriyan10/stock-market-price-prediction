import sqlite3
import hashlib
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = "backend/auth/users.db"
app = FastAPI()

# ========================
# Database Utility
# ========================
def create_user_table():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Call table creation at import
create_user_table()

# ========================
# Utility Functions
# ========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, hash_password(password)))
        conn.commit()
        return True, "Registered successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                   (username, hash_password(password)))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# ========================
# Pydantic Models
# ========================
class User(BaseModel):
    username: str
    password: str

# ========================
# API Endpoints
# ========================
@app.get("/")
def read_root():
    return {"message": "Welcome to SMPS API"}

@app.post("/register")
def register(user: User):
    success, msg = register_user(user.username, user.password)
    if success:
        return {"success": True, "message": msg}
    raise HTTPException(status_code=400, detail=msg)

@app.post("/login")
def login(user: User):
    if login_user(user.username, user.password):
        return {"success": True, "message": "Login successful."}
    raise HTTPException(status_code=401, detail="Invalid credentials.")
