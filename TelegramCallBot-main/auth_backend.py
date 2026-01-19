from fastapi import FastAPI
from google.oauth2 import flow
import os

app = FastAPI()

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

@app.get('/auth/google/start')
def google_start(user_id: str):
    # Редирект на Google consent
    return {"auth_url": "..."}

@app.get('/auth/google/callback')
def google_callback(code: str, user_id: str):
    # Сохраняем токен, отправляем в бот
    return {"status": "success"}
