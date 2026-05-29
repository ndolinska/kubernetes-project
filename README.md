# Projekt

<p class="editor-paragraph mb-2" dir="ltr"><span style="white-space: pre-wrap;">Przygotuj aplikację wieloserwisową uruchamianą w Kubernetes oraz wdrażaną przez GitHub Actions. Funkcjonalność aplikacji ma być ograniczona i pomocnicza; oceniana jest przede wszystkim architektura wdrożeniowa w klastrze oraz automatyzacja CI/CD.</span></p>

## Opis Wyzwania
<p class="editor-paragraph mb-2" dir="ltr"><b><strong class="editor-text-bold font-bold" style="white-space: pre-wrap;">Projekt Kubernetes — aplikacja wieloserwisowa z CI/CD</strong></b></p><p class="editor-paragraph mb-2" dir="ltr"><span style="white-space: pre-wrap;">Projekt polega na przygotowaniu działającej aplikacji wieloserwisowej uruchamianej w </span><code spellcheck="false" style="white-space: pre-wrap;"><span class="editor-text-code bg-muted px-1 py-0.5 rounded font-mono text-sm">Kubernetes</span></code><span style="white-space: pre-wrap;"> oraz wdrażanej przez pipeline </span><code spellcheck="false" style="white-space: pre-wrap;"><span class="editor-text-code bg-muted px-1 py-0.5 rounded font-mono text-sm">CI/CD</span></code><span style="white-space: pre-wrap;"> w </span><code spellcheck="false" style="white-space: pre-wrap;"><span class="editor-text-code bg-muted px-1 py-0.5 rounded font-mono text-sm">GitHub Actions</span></code><span style="white-space: pre-wrap;">. Wariant Kubernetes jest trudniejszy od wariantu Docker: wymaga manifestów klastra, trwałego storage, Ingressa, sond, limitów zasobów, securityContext i automatycznego wdrożenia.</span></p><p class="editor-paragraph mb-2" dir="ltr"><span style="white-space: pre-wrap;">Projekt powinien dać się sprawdzić w około 20 minut na osobę. Repozytorium musi zawierać </span><code spellcheck="false" style="white-space: pre-wrap;"><span class="editor-text-code bg-muted px-1 py-0.5 rounded font-mono text-sm">CHECKLIST.md</span></code><span style="white-space: pre-wrap;"> z instrukcją uruchomienia na kind, minikube albo k3d, listą zasobów Kubernetes, komendami kubectl, przykładowymi wynikami i linkiem do ostatniego udanego workflow GitHub Actions.</span></p><p class="editor-paragraph mb-2"><br></p>

## Kryteria Oceny
Całkowita liczba punktów: 40

| Wymaganie | Opis | Waga |
|-----------|------|------|
| Wymaganie | Projekt zawiera katalog k8s/ albo Helm/Kustomize. Manifesty obejmują minimum: Namespace, Deployment, StatefulSet lub równoważny zasób dla bazy, Service, Ingress, ConfigMap, Secret, PVC. | 12% |
| Wymaganie | Frontend/API/worker działają jako Deployment. Backend ma minimum 2 repliki i strategię aktualizacji rolling update. Sprawdzenie: kubectl get deploy i kubectl rollout status. | 10% |
| Wymaganie | Baza danych działa jako StatefulSet albo przez jasno uzasadniony zasób zapewniający trwałość. Musi używać PersistentVolumeClaim. | 12% |
| Wymaganie | Komunikacja wewnętrzna odbywa się przez Service. Ruch zewnętrzny przechodzi przez Ingress. Baza danych, cache i worker nie są wystawione na zewnątrz klastra. | 10% |
| Wymaganie | Konfiguracja niepoufna jest w ConfigMap, a dane poufne w Secret. Hasła i tokeny nie mogą być zapisane jawnie w kodzie aplikacji ani w README jako prawdziwe wartości produkcyjne. | 8% |
| Wymaganie | Główne kontenery mają readinessProbe i livenessProbe oraz ustawione resources.requests i resources.limits. Sprawdzenie: szybka analiza manifestów i kubectl describe pod. | 10% |
| Wymaganie | Kontenery aplikacyjne działają jako non-root i mają podstawowy securityContext. Projekt używa initContainer albo Job do migracji bazy, inicjalizacji danych lub oczekiwania na zależności. | 8% |
| Wymaganie | Repozytorium zawiera workflow, który buduje obraz, uruchamia testy lub podstawową walidację, publikuje obraz do rejestru i wykonuje deploy przez kubectl, Helm albo Kustomize. Workflow sprawdza rollout po wdrożeniu. | 10% |
| Wymaganie | Projekt definiuje NetworkPolicy, które ograniczają ruch między podami, np. baza przyjmuje ruch tylko z backendu lub workera. | 2.5% |
| Wymaganie | Dla backendu dodano PodDisruptionBudget, który chroni minimalną dostępność replik podczas aktualizacji lub prac utrzymaniowych klastra. | 2.5% |
| Wymaganie | Projekt używa Helm albo Kustomize do parametryzacji manifestów i obsługuje minimum dwa środowiska, np. dev i prod. | 2.5% |
| Wymaganie | Aplikacja udostępnia /metrics, adnotacje dla Prometheusa albo inną prostą formę obserwowalności oraz instrukcję sprawdzenia metryk/logów. | 2.5% |
| Wymaganie | Aplikacja ma jeden główny zasób biznesowy i obsługuje co najmniej dodanie danych, odczyt danych oraz endpoint /health lub /ready. Sprawdzenie: 2-3 komendy curl po wdrożeniu. | 10% |
| Wymaganie | Dane aplikacji są zapisywane w bazie danych działającej w Kubernetes i pozostają dostępne po restarcie poda bazy. Sprawdzenie: dodać rekord, usunąć pod bazy, odczytać rekord po odtworzeniu poda. | 5% |
| Wymaganie | Projekt zawiera dodatkowy komponent architektury, np. Redis, RabbitMQ albo worker. Musi być prosty dowód działania w CHECKLIST.md. | 5% |

## Zgłoszenie Rozwiązania
Proszę zaimplementować swoje rozwiązanie w tym repozytorium. Kiedy będziesz gotowy, prześlij link do tego repozytorium na platformie Cursora (cursora.org).
