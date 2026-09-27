from fastapi import FastAPI
from app.api import words
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:{settings.FRONTEND_PORT}"],
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(words.router)

@app.get("/")
async def root():
    return {
        "message": "Wordbook API is running"
    }