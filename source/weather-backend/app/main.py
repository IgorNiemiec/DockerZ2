import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Path, Query
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware

from .locations import LocationStore
from .weather import get_weather





# 1. Konfiguracja loggera

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-5s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("weather-backend")


# 2. Inicjalizacja aplikacji FastAPI

app = FastAPI(
    title="Weather App API",
    description="API do wyboru kraju/miasta i pobierania pogody",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)





# 3. Wczytanie danych lokalizacji

store = LocationStore()
logger.info(f"Załadowano {len(store.list_countries())} krajów")

# 4. Logowanie przy starcie

@app.on_event("startup")
async def log_startup_event():
    port = 8000  
    author = "Igor Niemiec"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    logger.info(
        f"Aplikacja wystartowała — data: {now}, autor: {author}, port: {port}"
    )

# 5. Healthcheck

@app.get("/health", tags=["Health"], summary="Stan aplikacji")
async def health_check():
    return {"status": "ok"}

# 6. Endpointy lokalizacji

@app.get(
    "/countries",
    response_model=List[Dict[str, str]],
    tags=["Locations"],
    summary="Lista krajów"
)
async def get_countries():
    return store.list_countries()

@app.get(
    "/countries/{country_code}/cities",
    response_model=List[str],
    tags=["Locations"],
    summary="Lista miast dla kraju"
)
async def get_cities(
    country_code: str = Path(
        ..., min_length=2, max_length=2,
        description="Kod ISO2 kraju, np. 'PL'"
    )
):
    cities = [c["name"] for c in store.list_cities(country_code)]
    if not cities:
        raise HTTPException(status_code=404, detail="Kraj nie znaleziony lub brak miast")
    return cities

# 7. Endpoint pogody

@app.get(
    "/weather",
    response_model=Dict[str, Any],
    tags=["Weather"],
    summary="Aktualna pogoda dla miasta (Visual Crossing)"
)
async def weather_endpoint(
    country_code: str = Query(
        ..., min_length=2, max_length=2,
        description="Kod ISO2 kraju, np. 'PL'"
    ),
    city: str = Query(
        ..., min_length=1,
        description="Nazwa miasta, np. 'Warsaw'"
    )
):
    location = store.find_city(country_code, city)
    if location is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono miasta")

    lat = location["lat"]
    lon = location["lon"]
    logger.info(f"Pobieranie pogody (Visual Crossing) dla {city}, {country_code} (lat={lat}, lon={lon})")

    try:
        weather_data = await get_weather(lat, lon)
    except Exception as e:
        logger.error(f"Błąd podczas pobierania pogody: {e}")
        raise HTTPException(status_code=502, detail="Błąd zewnętrznego API pogodowego")

    return weather_data
