from typing import Dict


class LocalWeatherService:
    def analyze(self, weather_data: Dict) -> Dict:
        wind_speed = weather_data.get("wind_speed", 0)
        rain = weather_data.get("rain", 0)
        visibility = weather_data.get("visibility", 10000)

        risk = 0.0

        # Wind risk
        if wind_speed > 10:
            risk += 0.4
        elif wind_speed > 5:
            risk += 0.2

        # Rain risk
        if rain > 5:
            risk += 0.4
        elif rain > 1:
            risk += 0.2

        # Visibility risk
        if visibility < 2000:
            risk += 0.3
        elif visibility < 5000:
            risk += 0.1

        return {
            "wind_speed": wind_speed,
            "rain": rain,
            "visibility": visibility,
            "risk_score": min(risk, 1.0),
        }