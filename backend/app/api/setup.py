from fastapi import APIRouter, HTTPException
from app.schemas.setup import SetupRequest
from app.services.session_service import session_service

router = APIRouter(prefix="/setup", tags=["Setup"])


@router.post("/")
def set_setup(payload: SetupRequest):
    return session_service.set_setup(payload)


@router.get("/")
def get_setup():
    try:
        return session_service.get_setup()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))