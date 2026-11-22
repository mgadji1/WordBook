import logging
import os
from pythonjsonlogger.json import JsonFormatter
from datetime import datetime, timezone
import time

from app.metrics import (
    wordbook_requests_total,
    wordbook_request_duration_seconds
)


from app.database.database import engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


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


from fastapi import FastAPI, Request, Response
from app.api import words
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:{settings.FRONTEND_PORT}"],
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(words.router)


Instrumentator().instrument(app).expose(app)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.monotonic()

    try:
        response: Response = await call_next(request)

        wordbook_request_duration_seconds.observe(time.monotonic() - start_time)

        wordbook_requests_total.labels(status=str(response.status_code)).inc()
    
    except Exception:
        wordbook_request_duration_seconds.observe(time.monotonic() - start_time)

        wordbook_requests_total.labels(status="500").inc()

        raise

    response.headers["X-Service-Version"] = settings.SERVICE_VERSION

    return response

@app.on_event("startup")
async def startup():
    logger.info(
        "Application startup"
    )

@app.get("/")
async def root():
    return {
        "message": "Wordbook API is running",
        "version": settings.SERVICE_VERSION
    }

@app.get("/health")
async def health():
    return {
        "status": "alive"
    }

@app.get("/ready")
async def readiness():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        return {
            "status": "ready"
        }

    except SQLAlchemyError:
        return Response(
            content='{"status": "not ready"}',
            status_code=503,
            media_type="application/json"
        )