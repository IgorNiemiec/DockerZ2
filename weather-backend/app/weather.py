from dotenv import load_dotenv
import os
from typing import Dict, Any
import httpx
from dateutil import parser

load_dotenv()

# 1. Pobranie klucza API z ENV

API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
if not API_KEY:
    raise RuntimeError("Brak VISUAL_CROSSING_API_KEY w środowisku")

# 2. Bazowy URL

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast"

async def get_weather(lat: float, lon: float) -> Dict[str, Any]:
    """
    Pobiera dane pogodowe z Visual Crossing Weather dla podanych współrzędnych.
    Zwraca JSON z kluczowymi polami: currentConditions, days (daily), hours (hourly).
    """
    params = {
        "locations": f"{lat},{lon}",
        "aggregateHours": 1,       
        "unitGroup": "metric",   
        "contentType": "json",
        "shortColumnNames": "false",
        "key": API_KEY
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(BASE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

   
    loc_key = next(iter(data.get("locations", {})), None)
    if not loc_key:
        raise RuntimeError("Nieprawidłowa odpowiedź API pogodowego")
    loc_data = data["locations"][loc_key]

  
    result = {
        "current": loc_data.get("currentConditions", {}),
        "hourly": loc_data.get("hours", []),
        "daily": loc_data.get("days", [])
    }
    return result
