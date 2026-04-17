from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class GridPoint(BaseModel):
    row: int = Field(..., ge=0)
    col: int = Field(..., ge=0)


class GeoPoint(BaseModel):
    lat: float
    lon: float


class MissionBounds(BaseModel):
    north: float
    south: float
    east: float
    west: float


class CostmapConfig(BaseModel):
    rows: int = Field(default=20, ge=5, le=200)
    cols: int = Field(default=20, ge=5, le=200)
    diagonal_movement: bool = False


class RoutePlanningRequest(BaseModel):
    image_path: str
    start: GridPoint
    goal: GridPoint
    algorithm: Literal["astar", "dijkstra"] = "astar"
    costmap: CostmapConfig = CostmapConfig()
    bounds: MissionBounds
    include_weather: bool = False
    weather: Optional[dict] = None


class RouteStep(BaseModel):
    row: int
    col: int
    cumulative_cost: float


class GeoRouteStep(BaseModel):
    lat: float
    lon: float


class RoutePlanningResponse(BaseModel):
    algorithm: str
    image_path: str
    feasible: bool
    start: GridPoint
    goal: GridPoint
    total_cost: float
    path_length: int
    path: List[RouteStep]
    geo_path: List[GeoRouteStep]
    message: str
    costmap_rows: int
    costmap_cols: int
    bounds: MissionBounds