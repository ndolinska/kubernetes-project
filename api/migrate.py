"""
Skrypt migracyjny — uruchamiany jako Kubernetes Job przed startem API.
Tworzy tabelę tasks jeśli jeszcze nie istnieje.
"""

import sys
import database

if __name__ == "__main__":
    print("Uruchamiam migrację bazy danych...")
    try:
        database.init_pool()
        database.create_tables()
        print("Migracja zakończona pomyślnie.")
        sys.exit(0)
    except Exception as exc:
        print(f"Błąd migracji: {exc}", file=sys.stderr)
        sys.exit(1)
