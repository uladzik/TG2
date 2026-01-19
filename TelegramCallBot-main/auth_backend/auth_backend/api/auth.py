from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse, JSONResponse
from google_auth_oauthlib.flow import Flow
import os
import json

app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = 'https://your-vercel-app.vercel.app/callback'

# Временное хранилище токенов (в продакшене - БД)
tokens_store = {}

@app.get('/auth/google/start')
def google_start(user_id: str):
    flow = Flow.from_client_config(
        {
            "installed": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    auth_url, state = flow.authorization_url(access_type='offline')
    # Сохраняем state с user_id
    tokens_store[state] = {'user_id': user_id}
    return RedirectResponse(auth_url)

@app.get('/callback')
def callback(code: str, state: str):
    flow = Flow.from_client_config(...)
    flow.redirect_uri = REDIRECT_URI
    flow.fetch_token(code=code)
    
    user_id = tokens_store.get(state, {}).get('user_id')
    token = flow.credentials.to_json()
    
    # Сохраняем токен (для боота)
    tokens_store[user_id] = token
    
    return JSONResponse({"status": "success", "user_id": user_id})

@app.get('/events/{user_id}')
def get_events(user_id: str):
    token = tokens_store.get(user_id)
    if not token:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    # Получаем события из Google Calendar
    return JSONResponse({"events": []})
