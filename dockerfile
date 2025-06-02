#!/bin/bash

# Uruchomienie backendu w tle
echo "Uruchamianie backendu..."
cd weather-backend
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Przejście do katalogu frontendowego
echo "Uruchamianie frontendu..."
cd ../weather-frontend
npm start

# Zatrzymanie backendu po zakończeniu frontendu
echo "Zatrzymywanie backendu..."
kill $(jobs -p)
