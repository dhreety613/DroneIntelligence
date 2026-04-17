from fastapi import APIRouter, HTTPException

from app.schemas.replanning import ReplanningRequest, ReplanningResponse
from app.services.dynamic_replanning_service import DynamicReplanningService
from app.services.mission_execution_service import MissionExecutionService

router = APIRouter(prefix="/replanning", tags=["Replanning"])

dynamic_replanning_service = DynamicReplanningService()

# IMPORTANT:
# This must be the same shared mission service instance used in mission.py in a real app.
# For now, we import and reuse the router-level singleton from mission API.
from app.api.mission import mission_service


@router.post("/local", response_model=ReplanningResponse)
def local_replan(payload: ReplanningRequest) -> ReplanningResponse:
    try:
        mission = mission_service.get_mission(payload.mission_id)

        result = dynamic_replanning_service.replan(mission, payload)

        if result["feasible"]:
            mission_service.update_mission_after_replanning(
                mission_id=payload.mission_id,
                algorithm=payload.algorithm,
                total_cost=result["total_cost"],
                message=result["message"],
            )

        return ReplanningResponse(**result)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Dynamic replanning failed: {str(exc)}") from exc