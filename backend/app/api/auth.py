from fastapi import APIRouter, HTTPException
from app.schemas.auth import SignupRequest, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
service = AuthService()


@router.post("/signup")
def signup(payload: SignupRequest):
    try:
        return service.signup(payload.username, payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(payload: LoginRequest):
    try:
        return service.login(payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))