"""
uvicorn main:app --reload --port 8000 --env-file .env
Testy curl:
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl -X POST http://localhost:8000/tasks/ -H "Content-Type: application/json" -d "{\"title\": \"test task\"}"
curl http://localhost:8000/tasks/
"""

import os
from contextlib import asynccontextmanager

import redis as redis_lib
from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

import database
import routes

# Licznik requestów — eksportowany przez /metrics dla Prometheusa
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Łączna liczba requestów HTTP",
    ["method", "endpoint"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Kod uruchamiany przy starcie i zatrzymaniu aplikacji."""
    # Startup
    database.init_pool()
    database.create_tables()
    app.state.redis = redis_lib.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
    )
    yield
    # Shutdown — pula połączeń zamknie się sama przez GC


app = FastAPI(title="Tasks API", version="1.0.0", lifespan=lifespan)

# Rejestrujemy router z endpointami /tasks
app.include_router(routes.router)


@app.get("/health")
def health():
    """Liveness probe — K8s sprawdza czy kontener żyje."""
    REQUEST_COUNT.labels(method="GET", endpoint="/health").inc()
    return {"status": "ok"}


@app.get("/ready")
def ready():
    """Readiness probe — K8s sprawdza czy kontener jest gotowy do ruchu."""
    REQUEST_COUNT.labels(method="GET", endpoint="/ready").inc()

    # Sprawdzamy połączenie z bazą
    try:
        conn = database.get_conn()
        database.release_conn(conn)
    except Exception as exc:
        return {"status": "not ready", "error": f"db: {exc}"}

    # Sprawdzamy połączenie z Redis
    try:
        app.state.redis.ping()
    except Exception as exc:
        return {"status": "not ready", "error": f"redis: {exc}"}

    return {"status": "ready"}


@app.get("/metrics")
def metrics():
    """Endpoint dla Prometheusa — zwraca metryki w formacie text/plain."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
