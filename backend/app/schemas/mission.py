from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


class MissionBounds(BaseModel):
    north: float
    south: float
    east: float
    west: float


class CreateMissionRequest(BaseModel):
    mission_id: str = Field(..., min_length=1)
    drone_id: str = Field(..., min_length=1)
    image_path: str
    start_row: int = Field(..., ge=0)
    start_col: int = Field(..., ge=0)
    goal_row: int = Field(..., ge=0)
    goal_col: int = Field(..., ge=0)
    algorithm: Literal["astar", "dijkstra"] = "astar"
    rows: int = Field(default=20, ge=5, le=200)
    cols: int = Field(default=20, ge=5, le=200)
    diagonal_movement: bool = False
    include_weather: bool = False
    weather: Optional[dict] = None
    bounds: MissionBounds
    notes: Optional[str] = None


class MissionWaypointResponse(BaseModel):
    row: int
    col: int
    cumulative_cost: float


class MissionResponse(BaseModel):
    mission_id: str
    drone_id: str
    status: str
    image_path: str
    algorithm: str
    start_row: int
    start_col: int
    goal_row: int
    goal_col: int
    total_cost: float
    total_waypoints: int
    current_waypoint_index: int
    current_row: int
    current_col: int
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None
    bounds: MissionBounds
    waypoints: List[MissionWaypointResponse]


class AdvanceMissionResponse(BaseModel):
    mission_id: str
    status: str
    moved: bool
    current_waypoint_index: int
    current_row: int
    current_col: int
    message: str


class MissionListResponse(BaseModel):
    missions: List[MissionResponse]