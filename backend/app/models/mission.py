from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


MissionStatus = Literal[
    "CREATED",
    "PLANNED",
    "IN_PROGRESS",
    "PAUSED",
    "COMPLETED",
    "FAILED",
]


class MissionWaypoint(BaseModel):
    row: int = Field(..., ge=0)
    col: int = Field(..., ge=0)
    cumulative_cost: float = Field(..., ge=0)


class MissionBounds(BaseModel):
    north: float
    south: float
    east: float
    west: float


class MissionState(BaseModel):
    mission_id: str
    drone_id: str
    status: MissionStatus
    created_at: datetime
    updated_at: datetime
    image_path: str
    algorithm: str
    start_row: int
    start_col: int
    goal_row: int
    goal_col: int
    total_cost: float
    total_waypoints: int
    current_waypoint_index: int = 0
    current_row: int
    current_col: int
    waypoints: List[MissionWaypoint]
    bounds: MissionBounds
    notes: Optional[str] = None