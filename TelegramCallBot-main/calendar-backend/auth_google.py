import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")  # http://127.0.0.1:8000/auth/google/callback
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def build_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
    )

@router.get("/auth/google/start")
async def google_start(user_id: str): # Принимаем user_id
    flow = build_flow()
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    # Передаем user_id в state, чтобы получить его обратно в callback
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        state=user_id 
    )
    return RedirectResponse(auth_url)

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")
    user_id = request.query_params.get("state") # Получаем ID обратно
    
    flow = build_flow()
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    flow.fetch_token(code=code)
    creds = flow.credentials

    # ВАЖНО: Здесь нужно сохранить creds.refresh_token в базу данных
    # связав его с user_id. Без этого бот не сможет звонить сам.
    # save_token_to_db(user_id, creds.refresh_token) 
    
    return RedirectResponse("https://cv-ai-app-179g.vercel.app/connected")
