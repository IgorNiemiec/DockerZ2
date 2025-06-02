from typing import Dict, List, Optional
import geonamescache

class LocationStore:

    def __init__(self):
        gc = geonamescache.GeonamesCache()
        countries_raw = gc.get_countries()
        cities_raw = gc.get_cities()

  

        self.countries: List[Dict[str, str]] = [
            {"iso2": code, "name": data["name"]}
            for code, data in countries_raw.items()
        ]

        temp_map: Dict[str, List[Dict[str, float]]] = {}
        for city in cities_raw.values():
            code = city["countrycode"].upper()
            entry = {
                "name": city["name"],
                "lat": float(city["latitude"]),
                "lon": float(city["longitude"])
            }
            temp_map.setdefault(code, []).append(entry)

   
        for code, lst in temp_map.items():
            temp_map[code] = sorted(lst, key=lambda x: x["name"])

        self.cities = temp_map

    def list_countries(self) -> List[Dict[str, str]]:
        return self.countries

    def list_cities(self, country_code: str) -> List[Dict[str, float]]:
        return self.cities.get(country_code.upper(), [])

    def find_city(self, country_code: str, city_name: str) -> Optional[Dict[str, float]]:
        """
        Znajduje miasto po nazwie (case-insensitive) w danym kraju.
        Zwraca słownik {'name', 'lat', 'lon'} lub None.
        """
        cities = self.list_cities(country_code)
        for city in cities:
            if city["name"].lower() == city_name.lower():
                return city
        return None
