FROM python:3.12-slim

# Katalog roboczy wewnątrz kontenera
WORKDIR /app

# Najpierw kopiujemy tylko requirements — warstwa cache'uje się osobno od kodu
# Dzięki temu rebuild po zmianie kodu nie reinstaluje paczek od nowa
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Dopiero teraz kopiujemy kod aplikacji
COPY . .

# Tworzymy użytkownika non-root (wymóg securityContext w K8s)
RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
