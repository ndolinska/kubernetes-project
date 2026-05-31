"""
Worker czyta id zadań z kolejki Redis i loguje ich przetworzenie.
Kolejka jest zasilana przez API przy każdym POST /tasks/.
"""

import os
import logging
import redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [worker] %(message)s",
)

REDIS_HOST  = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT  = int(os.getenv("REDIS_PORT", "6379"))
REDIS_QUEUE = "tasks_queue"

# Timeout blokującego odczytu — co ile sekund worker "obudzi się" nawet bez wiadomości
BLPOP_TIMEOUT = 5


def main() -> None:
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    logging.info("Worker uruchomiony, nasłuchuję na kolejce '%s'", REDIS_QUEUE)

    while True:
        # blpop blokuje wątek do BLPOP_TIMEOUT sekund czekając na wiadomość
        result = client.blpop(REDIS_QUEUE, timeout=BLPOP_TIMEOUT)

        if result is None:
            # Timeout — brak wiadomości, wracamy do nasłuchiwania
            continue

        _, task_id = result
        logging.info("Przetwarzam zadanie id=%s", task_id)

        # Tu docelowo mogłoby być np. wysłanie e-maila, generowanie raportu itp.
        # Na potrzeby projektu samo logowanie jest wystarczającym dowodem działania.
        logging.info("Zadanie id=%s przetworzone", task_id)


if __name__ == "__main__":
    main()
