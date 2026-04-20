from fastapi import APIRouter, HTTPException
from app.services.rtsp_stream_service import RTSPStreamService

router = APIRouter(prefix="/rtsp", tags=["RTSP"])

stream_service = None


@router.post("/start")
def start_stream(rtsp_url: str):
    global stream_service

    try:
        stream_service = RTSPStreamService(rtsp_url)
        stream_service.start()
        return {"status": "RTSP stream started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/latest")
def get_latest_frame():
    if not stream_service:
        raise HTTPException(status_code=400, detail="Stream not started")

    return stream_service.get_latest()


@router.post("/stop")
def stop_stream():
    global stream_service

    if stream_service:
        stream_service.stop()
        stream_service = None

    return {"status": "Stream stopped"}