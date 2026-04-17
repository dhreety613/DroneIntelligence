from fastapi import APIRouter, UploadFile, File, Form
from app.core.constants import SURVEILLANCE_TAG
from app.schemas.surveillance import (
    FileUploadResponse,
    DroneTelemetryIn,
    TelemetryResponse,
    WeatherInputIn,
    WeatherResponse,
    HealthResponse,
)
from app.services.surveillance_ingestion_service import SurveillanceIngestionService

router = APIRouter(prefix="/surveillance", tags=[SURVEILLANCE_TAG])


@router.get("/health", response_model=HealthResponse)
def surveillance_health() -> HealthResponse:
    return HealthResponse(status="ok", app="surveillance-step1")


@router.post("/image", response_model=FileUploadResponse)
async def upload_surveillance_image(
    drone_id: str = Form(...),
    file: UploadFile = File(...),
) -> FileUploadResponse:
    result = await SurveillanceIngestionService.save_image_upload(drone_id, file)
    return FileUploadResponse(**result)


@router.post("/video", response_model=FileUploadResponse)
async def upload_surveillance_video(
    drone_id: str = Form(...),
    file: UploadFile = File(...),
) -> FileUploadResponse:
    result = await SurveillanceIngestionService.save_video_upload(drone_id, file)
    return FileUploadResponse(**result)


@router.post("/telemetry", response_model=TelemetryResponse)
def upload_drone_telemetry(payload: DroneTelemetryIn) -> TelemetryResponse:
    result = SurveillanceIngestionService.save_telemetry(payload)
    return TelemetryResponse(**result)


@router.post("/weather", response_model=WeatherResponse)
def upload_weather_input(payload: WeatherInputIn) -> WeatherResponse:
    result = SurveillanceIngestionService.save_weather(payload)
    return WeatherResponse(**result)