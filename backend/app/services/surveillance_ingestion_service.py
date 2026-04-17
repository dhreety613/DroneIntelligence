import json
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile, HTTPException

from app.core.config import settings
from app.schemas.surveillance import DroneTelemetryIn, WeatherInputIn
from app.services.preprocessing_service import PreprocessingService
from app.utils.image_utils import generate_unique_filename


class SurveillanceIngestionService:
    @staticmethod
    async def save_image_upload(drone_id: str, file: UploadFile) -> dict:
        suffix = Path(file.filename).suffix.lower()
        if suffix not in settings.ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported image format.")

        unique_name = generate_unique_filename(file.filename)
        raw_path = settings.RAW_IMAGES_DIR / drone_id / unique_name
        raw_path.parent.mkdir(parents=True, exist_ok=True)

        content = await file.read()
        raw_path.write_bytes(content)

        processed_name = unique_name
        processed_path = PreprocessingService.preprocess_image(raw_path, processed_name)

        return {
            "message": "Image uploaded and preprocessed successfully.",
            "drone_id": drone_id,
            "file_name": unique_name,
            "raw_path": str(raw_path),
            "processed_path": str(processed_path),
            "metadata": {
                "uploaded_at": datetime.utcnow().isoformat(),
                "type": "image",
            },
        }

    @staticmethod
    async def save_video_upload(drone_id: str, file: UploadFile) -> dict:
        suffix = Path(file.filename).suffix.lower()
        if suffix not in settings.ALLOWED_VIDEO_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported video format.")

        unique_name = generate_unique_filename(file.filename)
        raw_path = settings.RAW_VIDEOS_DIR / drone_id / unique_name
        raw_path.parent.mkdir(parents=True, exist_ok=True)

        content = await file.read()
        raw_path.write_bytes(content)

        frame_paths = PreprocessingService.preprocess_video(raw_path, Path(unique_name).stem)

        return {
            "message": "Video uploaded and frames extracted successfully.",
            "drone_id": drone_id,
            "file_name": unique_name,
            "raw_path": str(raw_path),
            "processed_path": None,
            "metadata": {
                "uploaded_at": datetime.utcnow().isoformat(),
                "type": "video",
                "extracted_frames_count": len(frame_paths),
                "frame_paths": frame_paths,
            },
        }

    @staticmethod
    def save_telemetry(payload: DroneTelemetryIn) -> dict:
        drone_dir = settings.RAW_STATS_DIR / payload.drone_id
        drone_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"telemetry_{payload.timestamp.strftime('%Y%m%dT%H%M%S')}.json"
        file_path = drone_dir / file_name

        file_path.write_text(payload.model_dump_json(indent=2), encoding="utf-8")

        return {
            "message": "Telemetry saved successfully.",
            "drone_id": payload.drone_id,
            "saved_path": str(file_path),
            "payload": payload,
        }

    @staticmethod
    def save_weather(payload: WeatherInputIn) -> dict:
        file_name = f"weather_{payload.timestamp.strftime('%Y%m%dT%H%M%S')}.json"
        file_path = settings.RAW_WEATHER_DIR / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(payload.model_dump_json(indent=2), encoding="utf-8")

        return {
            "message": "Weather input saved successfully.",
            "saved_path": str(file_path),
            "payload": payload,
        }