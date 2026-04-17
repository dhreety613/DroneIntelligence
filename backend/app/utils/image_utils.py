from pathlib import Path
from uuid import uuid4
import cv2
import numpy as np


def generate_unique_filename(original_name: str) -> str:
    path = Path(original_name)
    return f"{path.stem}_{uuid4().hex}{path.suffix.lower()}"


def normalize_image(image: np.ndarray, target_size: tuple[int, int]) -> np.ndarray:
    resized = cv2.resize(image, target_size)
    normalized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)
    return normalized


def save_image(path: Path, image: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(path), image)
    if not success:
        raise ValueError(f"Failed to save image to {path}")


def extract_video_frames(
    video_path: Path,
    output_dir: Path,
    interval: int,
    target_size: tuple[int, int],
) -> list[str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(video_path))

    if not capture.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    frame_paths: list[str] = []
    frame_index = 0
    saved_count = 0

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        if frame_index % interval == 0:
            processed = normalize_image(frame, target_size)
            frame_file = output_dir / f"frame_{saved_count:05d}.jpg"
            save_image(frame_file, processed)
            frame_paths.append(str(frame_file))
            saved_count += 1

        frame_index += 1

    capture.release()
    return frame_paths