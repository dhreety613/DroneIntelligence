from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Any


class DroneTelemetryIn(BaseModel):
    drone_id: str = Field(..., min_length=1)
    timestamp: datetime
    latitude: float
    longitude: float
    altitude: float
    speed: float
    heading: float
    battery: float = Field(..., ge=0, le=100)
    status: str


class WeatherInputIn(BaseModel):
    source: str = Field(..., description="api | onboard | operator | simulation")
    timestamp: datetime
    latitude: float
    longitude: float
    temperature_c: float
    wind_speed_mps: float
    humidity_percent: float = Field(..., ge=0, le=100)
    pressure_hpa: float
    visibility_m: Optional[float] = None
    rainfall_mm: Optional[float] = None
    condition: str


class FileUploadResponse(BaseModel):
    message: str
    drone_id: str
    file_name: str
    raw_path: str
    processed_path: Optional[str] = None
    metadata: dict[str, Any]


class TelemetryResponse(BaseModel):
    message: str
    drone_id: str
    saved_path: str
    payload: DroneTelemetryIn


class WeatherResponse(BaseModel):
    message: str
    saved_path: str
    payload: WeatherInputIn


class HealthResponse(BaseModel):
    status: str
    app: str