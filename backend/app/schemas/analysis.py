from pydantic import BaseModel, Field
from typing import List, Optional


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class ObstacleDetection(BaseModel):
    label: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    bounding_box: BoundingBox
    center_x: float
    center_y: float
    width: float
    height: float
    risk_weight: float


class ObstacleAnalysisResult(BaseModel):
    image_path: str
    detections: List[ObstacleDetection]
    obstacle_count: int
    blocked: bool
    blocked_reason: Optional[str] = None


class TerrainAnalysisResult(BaseModel):
    image_path: str
    terrain_class: str
    difficulty_score: float = Field(..., ge=0.0, le=1.0)
    edge_density: float
    texture_variance: float
    vegetation_ratio: float
    water_ratio: float
    builtup_ratio: float
    recommended_penalty: float


class WeatherAnalysisInput(BaseModel):
    temperature_c: float
    wind_speed_mps: float
    humidity_percent: float = Field(..., ge=0, le=100)
    pressure_hpa: float
    visibility_m: Optional[float] = None
    rainfall_mm: Optional[float] = None
    condition: str


class WeatherAnalysisResult(BaseModel):
    severity_level: str
    risk_score: float = Field(..., ge=0.0, le=1.0)
    wind_penalty: float
    rain_penalty: float
    visibility_penalty: float
    total_weather_penalty: float
    no_fly: bool
    reason: Optional[str] = None


class RiskZone(BaseModel):
    zone_type: str
    score: float
    description: str


class EnvironmentAnalysisResponse(BaseModel):
    image_path: str
    obstacle_analysis: ObstacleAnalysisResult
    terrain_analysis: TerrainAnalysisResult
    weather_analysis: Optional[WeatherAnalysisResult] = None
    combined_risk_score: float = Field(..., ge=0.0, le=1.0)
    route_penalty: float
    feasible: bool
    risk_zones: List[RiskZone]
    recommended_action: str


class ImageAnalysisRequest(BaseModel):
    image_path: str
    include_weather: bool = False
    weather: Optional[WeatherAnalysisInput] = None