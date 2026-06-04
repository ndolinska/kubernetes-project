# Instrukcja uruchomienia projektu — kind (lokalnie)

## Wymagania wstępne

- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) v0.20+
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Docker](https://docs.docker.com/get-docker/) (działający daemon)

---

## 1. Utwórz klaster kind

```bash
kind create cluster --name tasks-cluster --config kind-config.yaml
```

Sprawdź:
```bash
kubectl get nodes
# Oczekiwany wynik: tasks-cluster-control-plane   Ready
```

---

## 2. Zainstaluj nginx ingress controller

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

---

## 3. Zastosuj manifesty Kubernetes

```bash
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/configmap.yaml
kubectl apply -f k8s/base/secret.yaml
kubectl apply -f k8s/base/postgres-service.yaml
kubectl apply -f k8s/base/postgres-statefulset.yaml
kubectl apply -f k8s/base/redis-service.yaml
kubectl apply -f k8s/base/redis-deployment.yaml
kubectl apply -f k8s/base/migration-job.yaml
kubectl apply -f k8s/base/api-service.yaml
kubectl apply -f k8s/base/api-deployment.yaml
kubectl apply -f k8s/base/worker-deployment.yaml
kubectl apply -f k8s/base/ingress.yaml
```

---

## 4. Poczekaj na gotowość aplikacji

Poczekaj na zakończenie migracji bazy danych:
```bash
kubectl wait --for=condition=complete job/db-migration -n tasks --timeout=120s
```

Sprawdź rollout deploymentów:
```bash
kubectl rollout status deployment/api    -n tasks --timeout=180s
kubectl rollout status deployment/redis  -n tasks --timeout=60s
kubectl rollout status deployment/worker -n tasks --timeout=120s
```

Sprawdź stan podów:
```bash
kubectl get pods -n tasks
# Oczekiwany wynik: wszystkie pody w stanie Running
```

---

## 5. Dodaj wpis DNS (jednorazowo)

**Windows (CMD jako Administrator):**
```cmd
echo 127.0.0.1 tasks.local >> C:\Windows\System32\drivers\etc\hosts
```

**WSL:**
```bash
echo "127.0.0.1 tasks.local" | sudo tee -a /etc/hosts
```

---

## 6. Testuj API

### Sprawdź zdrowie serwisu
```bash
curl http://tasks.local/health
# Oczekiwany wynik: {"status":"ok"}

curl http://tasks.local/ready
# Oczekiwany wynik: {"status":"ready"}
```

### Utwórz zadanie
```bash
curl -X POST http://tasks.local/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Moje pierwsze zadanie"}'
# Oczekiwany wynik: {"id":1,"title":"Moje pierwsze zadanie","status":"pending",...}
```

### Pobierz listę zadań
```bash
curl http://tasks.local/tasks/
# Oczekiwany wynik: lista zadań w JSON
```

### Sprawdź metryki Prometheus
```bash
curl http://tasks.local/metrics
# Oczekiwany wynik: metryki w formacie text/plain (http_requests_total itp.)
```

---

## 7. Przydatne komendy diagnostyczne

```bash
# Stan wszystkich zasobów w namespace tasks
kubectl get all -n tasks

# Logi API
kubectl logs -n tasks deployment/api

# Logi workera (powinien pokazywać przetwarzanie zadań)
kubectl logs -n tasks deployment/worker

# Logi migracji
kubectl logs -n tasks job/db-migration

# Szczegóły poda (jeśli coś nie działa)
kubectl describe pod -n tasks <nazwa-poda>

# Sprawdź PVC (trwałość danych Postgres)
kubectl get pvc -n tasks
```

---

## 8. Test trwałości danych

Dane PostgreSQL są przechowywane na PersistentVolumeClaim — przeżywają restart poda:

```bash
# Usuń poda Postgres (StatefulSet automatycznie go odtworzy)
kubectl delete pod postgres-0 -n tasks

# Poczekaj aż wróci
kubectl wait --for=condition=ready pod/postgres-0 -n tasks --timeout=60s

# Sprawdź czy dane są nadal dostępne
curl http://tasks.local/tasks/
```

---

## 9. Usuń klaster

```bash
kind delete cluster --name tasks-cluster
```

---

## CI/CD — GitHub Actions

Workflow `.github/workflows/deploy.yml` uruchamia się automatycznie przy każdym pushu na `main` i PR-ach.

**Trzy etapy:**
1. **Validate** — weryfikacja składni Pythona i plików YAML (działa na PR i main)
2. **Build & Push** — buduje obrazy Docker i wypycha do Docker Hub z tagami `:latest` i `:<sha>` (tylko main)
3. **Deploy & Verify** — tworzy klaster kind, wdraża wszystkie manifesty, sprawdza rollout (tylko main)

**Wymagane sekrety w ustawieniach repozytorium (Settings → Secrets → Actions):**
- `DOCKERHUB_USERNAME` — login Docker Hub
- `DOCKERHUB_TOKEN` — token dostępu (nie hasło, wygeneruj na hub.docker.com → Account Settings → Security → Access Tokens)

**Link do workflow:** [.github/workflows/deploy.yml](.github/workflows/deploy.yml)
