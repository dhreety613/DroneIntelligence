from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.surveillance import router as surveillance_router
from app.api.analysis import router as analysis_router
from app.api.planning import router as planning_router
from app.api.mission import router as mission_router
from app.api.replanning import router as replanning_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(surveillance_router, prefix=settings.API_PREFIX)
app.include_router(analysis_router, prefix=settings.API_PREFIX)
app.include_router(planning_router, prefix=settings.API_PREFIX)
app.include_router(mission_router, prefix=settings.API_PREFIX)
app.include_router(replanning_router, prefix=settings.API_PREFIX)


@app.get("/")
def root() -> dict:
    return {
        "message": "Drone Intelligence System backend is running.",
        "step": "Step 1 + Step 2 + Step 3 + Step 4 + Step 5 ready",
    }