import os
from dotenv import load_dotenv 
from supabase import create_client, Client
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel 

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

class Credentials(BaseModel):
    email: str
    password: str 

@app.get("/")
def root():
    return {"message": "Server running and connected to Supabase"}

@app.post("/auth/signup")
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

    return response

@app.get("/public/info")
def get_info():
    return {"message": "Welcome stranger! This info is public"}


@app.get("/protected/profile")
def get_profile(authorization = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="access token required")

    token = authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=404, detail="Access token required")

    return {"token_received": token}