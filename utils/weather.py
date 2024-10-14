from settings import geoloc_api_key, geoloc_api_url, meteo_api_url
import requests
import openmeteo_requests
import requests_cache
from retry_requests import retry


async def get_coordinates(city_name):
    """
    Получает координаты города по его имени.

    Args:
        city_name: Строка, содержащая название города.

    Returns:
        Словарь с координатами (широта, долгота),
        или None, если город не найден.
    """

    params = {"q": city_name, "key": geoloc_api_key}
    response = requests.get(geoloc_api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            coordinates = {
                "latitude": data["results"][0]["geometry"]["lat"],
                "longitude": data["results"][0]["geometry"]["lng"],
            }
            return coordinates
        else:
            return None
    else:
        return None


async def get_weather(coordinates):
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = meteo_api_url
    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
            "wind_direction_10m",
        ],
        "timezone": "Europe/Moscow",
        "forecast_days": 1,
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    return current
