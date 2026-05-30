import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

# Parametry bazy — czytane z env vars, które K8s wstrzyknie z ConfigMap i Secret
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", "5432")),
    "dbname":   os.getenv("DB_NAME", "tasksdb"),
    "user":     os.getenv("DB_USER", "tasks"),
    "password": os.getenv("DB_PASSWORD", ""),
}

# Pula połączeń: klasycznie min 1, max 10 
_pool: pool.SimpleConnectionPool | None = None


def init_pool() -> None:
    """Inicjalizuje pulę połączeń. Wywoływana raz przy starcie aplikacji."""
    global _pool
    _pool = pool.SimpleConnectionPool(1, 10, **DB_CONFIG)


def get_conn():
    """Pobiera połączenie z puli."""
    return _pool.getconn()


def release_conn(conn) -> None:
    """Zwraca połączenie do puli."""
    _pool.putconn(conn)


def create_tables() -> None:
    """Tworzy tabelę tasks jeśli jeszcze nie istnieje."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id         SERIAL PRIMARY KEY,
                    title      TEXT        NOT NULL,
                    status     TEXT        NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
        conn.commit()
    finally:
        release_conn(conn)
