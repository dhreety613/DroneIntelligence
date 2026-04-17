from pydantic import BaseModel, Field
from typing import Optional, Literal, List


class LocalObstacleEvent(BaseModel):
    row: int = Field(..., ge=0)
    col: int = Field(..., ge=0)
    severity: float = Field(..., ge=0.0, le=1.0)
    label: str = "unknown_obstacle"
    source: str = "onboard_sensor"


class LocalWeatherEvent(BaseModel):
    wind_speed_mps: float
    visibility_m: Optional[float] = None
    rainfall_mm: Optional[float] = None
    condition: str
    severity: float = Field(..., ge=0.0, le=1.0)
    source: str = "onboard_weather"


class ReplanningRequest(BaseModel):
    mission_id: str
    algorithm: Literal["astar", "dijkstra"] = "astar"
    diagonal_movement: bool = False
    local_obstacle: Optional[LocalObstacleEvent] = None
    local_weather: Optional[LocalWeatherEvent] = None


class GeoRouteStep(BaseModel):
    lat: float
    lon: float


class ReplanningResponse(BaseModel):
    mission_id: str
    feasible: bool
    algorithm: str
    old_remaining_waypoints: int
    new_total_waypoints: int
    current_row: int
    current_col: int
    goal_row: int
    goal_col: int
    total_cost: float
    adjusted_geo_path: List[GeoRouteStep]
    message: str