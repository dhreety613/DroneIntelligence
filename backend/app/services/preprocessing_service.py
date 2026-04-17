from pathlib import Path
import cv2

from app.core.config import settings
from app.utils.image_utils import normalize_image, save_image, extract_video_frames


class PreprocessingService:
    @staticmethod
    def preprocess_image(raw_image_path: Path, output_name: str) -> Path:
        image = cv2.imread(str(raw_image_path))
        if image is None:
            raise ValueError(f"Unable to read image: {raw_image_path}")

        processed = normalize_image(image, settings.IMAGE_SIZE)
        output_path = settings.PROCESSED_IMAGES_DIR / output_name
        save_image(output_path, processed)
        return output_path

    @staticmethod
    def preprocess_video(raw_video_path: Path, video_stem: str) -> list[str]:
        frame_output_dir = settings.PROCESSED_FRAMES_DIR / video_stem
        return extract_video_frames(
            video_path=raw_video_path,
            output_dir=frame_output_dir,
            interval=settings.FRAME_EXTRACTION_INTERVAL,
            target_size=settings.IMAGE_SIZE,
        )