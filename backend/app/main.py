import logging
import os
from pythonjsonlogger.json import JsonFormatter
from datetime import datetime, timezone


class UTCJsonFormatter(JsonFormatter):
    def formatTime(self, record, datefmt=None):
        return (
            datetime.fromtimestamp(record.created, timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
        )


formatter = UTCJsonFormatter(
    "%(asctime)s %(levelname)s %(message)s",
    rename_fields={
        "asctime": "timestamp",
        "levelname": "level"
    },
    static_fields={
        "service.name": os.getenv("SERVICE_NAME", "wordbook-backend"),
        "service.version": os.getenv("SERVICE_VERSION", "1.0"),
        "deployment.environment.name": os.getenv("DEPLOYMENT_ENVIRONMENT", "minikube"),
        "k8s.pod.name": os.getenv("K8S_POD_NAME", "local")
    }
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],
    force=True
)

logger = logging.getLogger()


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


@app.on_event("startup")
async def startup():
    logger.info(
        "Application startup"
    )

@app.get("/")
async def root():
    return {
        "message": "Wordbook API is running"
    }