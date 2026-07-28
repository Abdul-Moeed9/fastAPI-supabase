import os
from dotenv import load_dotenv 
from supabase import create_client, Client
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel 

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
bearer_scheme = HTTPBearer()

class Credentials(BaseModel):
    email: str
    password: str 

@app.get("/")
def root():
    return {"message": "Server running and connected to Supabase"}

@app.post("/auth/signup", status_code=201)
def signup(credentials: Credentials):
    if credentials.email == "" or credentials.password == "":
        raise HTTPException(status_code=400, detail="email or password field is empty")

    try:
        response = supabase.auth.sign_up(
            {
            "email": credentials.email,
            "password": credentials.password
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 

    return {"user": response.user}

@app.post("/auth/login")
def login(credentials: Credentials):
    if credentials.email == "" or credentials.password == "":
        raise HTTPException(status_code=400, detail="missing email or password")

    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token
    }

@app.get("/public/info")
def get_info():
    return {"message": "Welcome stranger! This info is public"}

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Access token required")

    try:
        user_response = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not user_response or not user_response.user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user_response.user

@app.get("/protected/profile")
def get_profile(user = Depends(verify_token)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

@app.get("/protected/dashboard")
def get_dashboard(user = Depends(verify_token)):
    return {"message": f"Welcome to your dashboard, {user.email}"}

@app.post("/auth/logout", status_code=204)
def logout(user = Depends(verify_token)):
    supabase.auth.sign_out()
    return