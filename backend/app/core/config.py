from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    APP_NAME: str = "Drone Intelligence System"
    API_PREFIX: str = "/api/v1"

    BASE_DIR: Path = Path(__file__).resolve().parents[2]
    DATA_DIR: Path = BASE_DIR / "data"

    RAW_IMAGES_DIR: Path = DATA_DIR / "raw" / "surveillance_images"
    RAW_VIDEOS_DIR: Path = DATA_DIR / "raw" / "surveillance_videos"
    RAW_STATS_DIR: Path = DATA_DIR / "raw" / "drone_stats"
    RAW_WEATHER_DIR: Path = DATA_DIR / "raw" / "weather"

    PROCESSED_FRAMES_DIR: Path = DATA_DIR / "processed" / "frames"
    PROCESSED_IMAGES_DIR: Path = DATA_DIR / "processed" / "normalized_images"

    ALLOWED_IMAGE_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    ALLOWED_VIDEO_EXTENSIONS: set[str] = {".mp4", ".avi", ".mov", ".mkv"}

    IMAGE_SIZE: tuple[int, int] = (640, 640)
    FRAME_EXTRACTION_INTERVAL: int = 15

    YOLO_MODEL_PATH: str = "models/yolo11n.pt"
    YOLO_CONF_THRESHOLD: float = 0.25

    WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")

    def ensure_directories(self) -> None:
        dirs = [
            self.RAW_IMAGES_DIR,
            self.RAW_VIDEOS_DIR,
            self.RAW_STATS_DIR,
            self.RAW_WEATHER_DIR,
            self.PROCESSED_FRAMES_DIR,
            self.PROCESSED_IMAGES_DIR,
        ]
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()