from fastapi import APIRouter, HTTPException

from app.schemas.analysis import (
    ImageAnalysisRequest,
    EnvironmentAnalysisResponse,
    WeatherAnalysisInput,
)
from app.services.obstacle_detection_service import ObstacleDetectionService
from app.services.terrain_analysis_service import TerrainAnalysisService
from app.services.weather_analysis_service import WeatherAnalysisService
from app.services.fusion_service import FusionService
from app.utils.terrain_utils import generate_fake_elevation
from app.services.weather_api_service import WeatherAPIService
from app.services.session_service import session_service


router = APIRouter(prefix="/analysis", tags=["Analysis"])

obstacle_service = ObstacleDetectionService()
terrain_service = TerrainAnalysisService()
weather_service = WeatherAnalysisService()
fusion_service = FusionService()
weather_api = WeatherAPIService()


@router.post("/image", response_model=EnvironmentAnalysisResponse)
def analyze_image(payload: ImageAnalysisRequest) -> EnvironmentAnalysisResponse:
    try:
        obstacle_result = obstacle_service.analyze_image(payload.image_path)

        elevation = generate_fake_elevation(20, 20)
        terrain_result = terrain_service.analyze_elevation(elevation)

        weather_result = None
        if payload.include_weather:
            lat, lon = 26.7271, 88.3953
            weather_data = weather_api.get_weather(lat, lon)
            weather_input = WeatherAnalysisInput(**weather_data)
            weather_result = weather_service.analyze(weather_input)

        fused = fusion_service.fuse(
            obstacle_analysis=obstacle_result,
            terrain_analysis=terrain_result,
            weather_analysis=weather_result,
        )

        return fused

    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(exc)}") from exc


@router.post("/run-current", response_model=EnvironmentAnalysisResponse)
def analyze_current() -> EnvironmentAnalysisResponse:
    try:
        setup = session_service.get_setup()

        payload = ImageAnalysisRequest(
            image_path=setup.image_path,
            include_weather=setup.include_weather,
        )

        return analyze_image(payload)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Current analysis failed: {str(exc)}") from exc