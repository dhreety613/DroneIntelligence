import requests
from app.core.config import settings


class WeatherAPIService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, lat: float, lon: float) -> dict:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric",
        }

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise ValueError("Weather API failed")

        data = response.json()

        return {
            "temperature_c": data["main"]["temp"],
            "wind_speed_mps": data["wind"]["speed"],
            "humidity_percent": data["main"]["humidity"],
            "pressure_hpa": data["main"]["pressure"],
            "visibility_m": data.get("visibility", 10000),
            "rainfall_mm": data.get("rain", {}).get("1h", 0),
            "condition": data["weather"][0]["description"],
        }