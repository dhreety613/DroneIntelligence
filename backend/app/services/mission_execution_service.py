from datetime import datetime
from typing import Dict, List

from app.models.mission import (
    MissionState,
    MissionWaypoint,
    MissionBounds as MissionStateBounds,
)
from app.schemas.mission import CreateMissionRequest
from app.schemas.route import (
    RoutePlanningRequest,
    GridPoint,
    CostmapConfig,
    MissionBounds as RouteMissionBounds,
)
from app.services.global_route_planning_service import GlobalRoutePlanningService


class MissionExecutionService:
    def __init__(self) -> None:
        self.route_service = GlobalRoutePlanningService()
        self._missions: Dict[str, MissionState] = {}

    def create_mission(self, payload: CreateMissionRequest) -> MissionState:
        if payload.mission_id in self._missions:
            raise ValueError(f"Mission with id '{payload.mission_id}' already exists.")

        route_request = RoutePlanningRequest(
            image_path=payload.image_path,
            start=GridPoint(row=payload.start_row, col=payload.start_col),
            goal=GridPoint(row=payload.goal_row, col=payload.goal_col),
            algorithm=payload.algorithm,
            costmap=CostmapConfig(
                rows=payload.rows,
                cols=payload.cols,
                diagonal_movement=payload.diagonal_movement,
            ),
            bounds=RouteMissionBounds(**payload.bounds.model_dump()),
            include_weather=payload.include_weather,
            weather=payload.weather,
        )

        route_response = self.route_service.plan_route(route_request)

        if not route_response.feasible or len(route_response.path) == 0:
            raise ValueError("Could not create mission because no feasible route was found.")

        now = datetime.utcnow()

        waypoints = [
            MissionWaypoint(
                row=step.row,
                col=step.col,
                cumulative_cost=step.cumulative_cost,
            )
            for step in route_response.path
        ]

        first = waypoints[0]

        mission = MissionState(
            mission_id=payload.mission_id,
            drone_id=payload.drone_id,
            status="PLANNED",
            created_at=now,
            updated_at=now,
            image_path=payload.image_path,
            algorithm=payload.algorithm,
            start_row=payload.start_row,
            start_col=payload.start_col,
            goal_row=payload.goal_row,
            goal_col=payload.goal_col,
            total_cost=route_response.total_cost,
            total_waypoints=len(waypoints),
            current_waypoint_index=0,
            current_row=first.row,
            current_col=first.col,
            waypoints=waypoints,
            bounds=MissionStateBounds(**payload.bounds.model_dump()),
            notes=payload.notes,
        )

        self._missions[payload.mission_id] = mission
        return mission

    def get_mission(self, mission_id: str) -> MissionState:
        mission = self._missions.get(mission_id)
        if not mission:
            raise ValueError(f"Mission '{mission_id}' not found.")
        return mission

    def list_missions(self) -> List[MissionState]:
        return list(self._missions.values())

    def start_mission(self, mission_id: str) -> MissionState:
        mission = self.get_mission(mission_id)

        if mission.status == "COMPLETED":
            raise ValueError("Mission is already completed.")
        if mission.status == "FAILED":
            raise ValueError("Mission has already failed.")

        mission.status = "IN_PROGRESS"
        mission.updated_at = datetime.utcnow()
        return mission

    def pause_mission(self, mission_id: str) -> MissionState:
        mission = self.get_mission(mission_id)

        if mission.status != "IN_PROGRESS":
            raise ValueError("Only an in-progress mission can be paused.")

        mission.status = "PAUSED"
        mission.updated_at = datetime.utcnow()
        return mission

    def advance_mission(self, mission_id: str) -> dict:
        mission = self.get_mission(mission_id)

        if mission.status == "COMPLETED":
            return {
                "mission_id": mission.mission_id,
                "status": mission.status,
                "moved": False,
                "current_waypoint_index": mission.current_waypoint_index,
                "current_row": mission.current_row,
                "current_col": mission.current_col,
                "message": "Mission already completed.",
            }

        if mission.status not in {"IN_PROGRESS", "PLANNED"}:
            return {
                "mission_id": mission.mission_id,
                "status": mission.status,
                "moved": False,
                "current_waypoint_index": mission.current_waypoint_index,
                "current_row": mission.current_row,
                "current_col": mission.current_col,
                "message": "Mission must be PLANNED or IN_PROGRESS to advance.",
            }

        if mission.status == "PLANNED":
            mission.status = "IN_PROGRESS"

        next_index = mission.current_waypoint_index + 1

        if next_index >= mission.total_waypoints:
            mission.status = "COMPLETED"
            mission.updated_at = datetime.utcnow()
            return {
                "mission_id": mission.mission_id,
                "status": mission.status,
                "moved": False,
                "current_waypoint_index": mission.current_waypoint_index,
                "current_row": mission.current_row,
                "current_col": mission.current_col,
                "message": "Mission reached final waypoint and is completed.",
            }

        next_wp = mission.waypoints[next_index]
        mission.current_waypoint_index = next_index
        mission.current_row = next_wp.row
        mission.current_col = next_wp.col
        mission.updated_at = datetime.utcnow()

        if mission.current_waypoint_index == mission.total_waypoints - 1:
            mission.status = "COMPLETED"
            message = "Drone moved to final waypoint. Mission completed."
        else:
            mission.status = "IN_PROGRESS"
            message = "Drone advanced to next waypoint."

        return {
            "mission_id": mission.mission_id,
            "status": mission.status,
            "moved": True,
            "current_waypoint_index": mission.current_waypoint_index,
            "current_row": mission.current_row,
            "current_col": mission.current_col,
            "message": message,
        }

    def fail_mission(self, mission_id: str, reason: str | None = None) -> MissionState:
        mission = self.get_mission(mission_id)
        mission.status = "FAILED"
        mission.notes = reason or mission.notes
        mission.updated_at = datetime.utcnow()
        return mission

    def update_mission_after_replanning(
        self,
        mission_id: str,
        algorithm: str,
        total_cost: float,
        message: str | None = None,
    ) -> MissionState:
        mission = self.get_mission(mission_id)
        mission.algorithm = algorithm
        mission.total_cost = total_cost
        mission.updated_at = datetime.utcnow()

        if mission.status == "PAUSED":
            mission.status = "IN_PROGRESS"

        if message:
            mission.notes = message

        return mission