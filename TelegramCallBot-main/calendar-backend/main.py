from fastapi import FastAPI
from auth_google import router as google_router

app = FastAPI()

app.include_router(google_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
