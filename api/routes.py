from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from prometheus_client import Counter

import database

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Licznik operacji na zasobie tasks
TASK_COUNT = Counter(
    "tasks_operations_total",
    "Łączna liczba operacji na tasks",
    ["operation"],
)

# Nazwa kolejki Redis — worker będzie z niej czytać
REDIS_QUEUE = "tasks_queue"


class TaskIn(BaseModel):
    """Schemat wejściowy — to co klient wysyła w body POST."""
    title: str


class TaskOut(BaseModel):
    """Schemat wyjściowy — to co zwracamy klientowi."""
    id: int
    title: str
    status: str
    created_at: str


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(task: TaskIn, request: Request):
    """Tworzy nowe zadanie i publikuje je do kolejki Redis."""
    TASK_COUNT.labels(operation="create").inc()

    conn = database.get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO tasks (title) VALUES (%s) RETURNING *",
                (task.title,),
            )
            row = cur.fetchone()
        conn.commit()
    except Exception as exc:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        database.release_conn(conn)

    # Publikujemy id zadania do kolejki — worker go przetworzy
    request.app.state.redis.rpush(REDIS_QUEUE, str(row["id"]))

    return {**row, "created_at": row["created_at"].isoformat()}


@router.get("/", response_model=list[TaskOut])
def list_tasks():
    """Zwraca wszystkie zadania z bazy."""
    TASK_COUNT.labels(operation="list").inc()

    conn = database.get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            rows = cur.fetchall()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        database.release_conn(conn)

    return [{**r, "created_at": r["created_at"].isoformat()} for r in rows]
