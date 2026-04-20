from pydantic import BaseModel


class MissionBounds(BaseModel):
    north: float
    south: float
    east: float
    west: float


class SetupRequest(BaseModel):
    mission_id: str
    drone_id: str

    image_path: str

    start_row: int
    start_col: int
    goal_row: int
    goal_col: int

    rows: int = 20
    cols: int = 20
    diagonal_movement: bool = False

    include_weather: bool = True
    algorithm: str = "astar"

    bounds: MissionBounds