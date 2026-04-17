from app.schemas.analysis import WeatherAnalysisInput, WeatherAnalysisResult


class WeatherAnalysisService:
    def analyze(self, weather: WeatherAnalysisInput) -> WeatherAnalysisResult:
        wind_penalty = 0.0
        rain_penalty = 0.0
        visibility_penalty = 0.0
        no_fly = False
        reasons = []

        # Wind
        if weather.wind_speed_mps >= 15:
            wind_penalty = 1.0
            no_fly = True
            reasons.append("Wind speed too high")
        elif weather.wind_speed_mps >= 10:
            wind_penalty = 0.7
            reasons.append("Moderately high wind")
        elif weather.wind_speed_mps >= 5:
            wind_penalty = 0.3

        # Rain
        rainfall = weather.rainfall_mm or 0.0
        if rainfall >= 20:
            rain_penalty = 1.0
            no_fly = True
            reasons.append("Heavy rain")
        elif rainfall >= 8:
            rain_penalty = 0.7
            reasons.append("Moderate rain")
        elif rainfall > 0:
            rain_penalty = 0.3

        # Visibility
        visibility = weather.visibility_m if weather.visibility_m is not None else 10000
        if visibility < 500:
            visibility_penalty = 1.0
            no_fly = True
            reasons.append("Very poor visibility")
        elif visibility < 1500:
            visibility_penalty = 0.7
            reasons.append("Poor visibility")
        elif visibility < 4000:
            visibility_penalty = 0.3

        base_condition_penalty = 0.0
        condition = weather.condition.lower()
        if "storm" in condition or "thunder" in condition:
            base_condition_penalty = 1.0
            no_fly = True
            reasons.append("Storm conditions")
        elif "fog" in condition or "mist" in condition:
            base_condition_penalty = max(base_condition_penalty, 0.5)
            reasons.append("Fog or mist")
        elif "rain" in condition:
            base_condition_penalty = max(base_condition_penalty, 0.4)

        total_weather_penalty = min(
            1.0,
            0.35 * wind_penalty
            + 0.30 * rain_penalty
            + 0.25 * visibility_penalty
            + 0.10 * base_condition_penalty,
        )

        if no_fly:
            severity = "HIGH"
        elif total_weather_penalty >= 0.55:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        reason = "; ".join(reasons) if reasons else None

        return WeatherAnalysisResult(
            severity_level=severity,
            risk_score=round(total_weather_penalty, 3),
            wind_penalty=round(wind_penalty, 3),
            rain_penalty=round(rain_penalty, 3),
            visibility_penalty=round(visibility_penalty, 3),
            total_weather_penalty=round(total_weather_penalty, 3),
            no_fly=no_fly,
            reason=reason,
        )