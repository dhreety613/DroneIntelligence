from fastapi import APIRouter, HTTPException

from app.schemas.route import RoutePlanningRequest, RoutePlanningResponse
from app.services.global_route_planning_service import GlobalRoutePlanningService

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