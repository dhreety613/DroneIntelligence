from fastapi import APIRouter, HTTPException

from app.schemas.mission import (
    CreateMissionRequest,
    MissionResponse,
    MissionListResponse,
    AdvanceMissionResponse,
    MissionWaypointResponse,
    MissionBounds,
)
from app.services.mission_execution_service import MissionExecutionService
from app.services.session_service import session_service
from app.schemas.mission import MissionBounds as SchemaBounds

router = APIRouter(prefix="/mission", tags=["Mission"])

mission_service = MissionExecutionService()


def _to_mission_response(mission) -> MissionResponse:
    return MissionResponse(
        mission_id=mission.mission_id,
        drone_id=mission.drone_id,
        status=mission.status,
        image_path=mission.image_path,
        algorithm=mission.algorithm,
        start_row=mission.start_row,
        start_col=mission.start_col,
        goal_row=mission.goal_row,
        goal_col=mission.goal_col,
        total_cost=mission.total_cost,
        total_waypoints=mission.total_waypoints,
        current_waypoint_index=mission.current_waypoint_index,
        current_row=mission.current_row,
        current_col=mission.current_col,
        created_at=mission.created_at,
        updated_at=mission.updated_at,
        notes=mission.notes,
        bounds=MissionBounds(**mission.bounds.model_dump()),
        waypoints=[
            MissionWaypointResponse(
                row=wp.row,
                col=wp.col,
                cumulative_cost=wp.cumulative_cost,
            )
            for wp in mission.waypoints
        ],
    )


@router.post("/create", response_model=MissionResponse)
def create_mission(payload: CreateMissionRequest) -> MissionResponse:
    try:
        mission = mission_service.create_mission(payload)
        return _to_mission_response(mission)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Mission creation failed: {str(exc)}"
        ) from exc


@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: str) -> MissionResponse:
    try:
        mission = mission_service.get_mission(mission_id)
        return _to_mission_response(mission)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/", response_model=MissionListResponse)
def list_missions() -> MissionListResponse:
    missions = mission_service.list_missions()
    return MissionListResponse(
        missions=[_to_mission_response(mission) for mission in missions]
    )


@router.post("/{mission_id}/start", response_model=MissionResponse)
def start_mission(mission_id: str) -> MissionResponse:
    try:
        mission = mission_service.start_mission(mission_id)
        return _to_mission_response(mission)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{mission_id}/pause", response_model=MissionResponse)
def pause_mission(mission_id: str) -> MissionResponse:
    try:
        mission = mission_service.pause_mission(mission_id)
        return _to_mission_response(mission)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/{mission_id}/advance", response_model=AdvanceMissionResponse)
def advance_mission(mission_id: str) -> AdvanceMissionResponse:
    try:
        result = mission_service.advance_mission(mission_id)
        return AdvanceMissionResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{mission_id}/fail", response_model=MissionResponse)
def fail_mission(mission_id: str, reason: str | None = None) -> MissionResponse:
    try:
        mission = mission_service.fail_mission(mission_id, reason)
        return _to_mission_response(mission)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/create-from-setup", response_model=MissionResponse)
def create_from_setup() -> MissionResponse:
    try:
        setup = session_service.get_setup()

        # If mission already exists, just return it
        try:
            existing = mission_service.get_mission(setup.mission_id)
            return _to_mission_response(existing)
        except ValueError:
            pass

        payload = CreateMissionRequest(
            mission_id=setup.mission_id,
            drone_id=setup.drone_id,
            image_path=setup.image_path,
            start_row=setup.start_row,
            start_col=setup.start_col,
            goal_row=setup.goal_row,
            goal_col=setup.goal_col,
            algorithm=setup.algorithm,
            rows=setup.rows,
            cols=setup.cols,
            diagonal_movement=setup.diagonal_movement,
            include_weather=setup.include_weather,
            bounds=SchemaBounds(**setup.bounds.model_dump()),
        )

        mission = mission_service.create_mission(payload)
        return _to_mission_response(mission)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Mission creation from setup failed: {str(exc)}"
        ) from exc