from fastapi import APIRouter, HTTPException

from app.schemas.route import RoutePlanningRequest, RoutePlanningResponse
from app.services.global_route_planning_service import GlobalRoutePlanningService
from app.services.session_service import session_service
from app.schemas.route import RoutePlanningRequest, GridPoint, CostmapConfig, MissionBounds

router = APIRouter(prefix="/planning", tags=["Planning"])

planning_service = GlobalRoutePlanningService()


@router.post("/route", response_model=RoutePlanningResponse)
def plan_route(payload: RoutePlanningRequest) -> RoutePlanningResponse:
    try:
        return planning_service.plan_route(payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Route planning failed: {str(exc)}") from exc
    
@router.post("/run-current")
def plan_current():
    setup = session_service.get_setup()

    payload = RoutePlanningRequest(
        image_path=setup.image_path,
        start=GridPoint(row=setup.start_row, col=setup.start_col),
        goal=GridPoint(row=setup.goal_row, col=setup.goal_col),
        algorithm=setup.algorithm,
        costmap=CostmapConfig(
            rows=setup.rows,
            cols=setup.cols,
            diagonal_movement=setup.diagonal_movement
        ),
        bounds=MissionBounds(**setup.bounds.model_dump()),
        include_weather=setup.include_weather
    )

    return planning_service.plan_route(payload)