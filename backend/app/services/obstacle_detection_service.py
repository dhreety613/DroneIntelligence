from pathlib import Path
from typing import List
from app.core.config import settings

from app.schemas.analysis import ObstacleAnalysisResult, ObstacleDetection
from ml.object_detection.infer import YOLOInference


class ObstacleDetectionService:
    HIGH_RISK_CLASSES = {
        "truck", "bus", "car", "person", "tree", "building", "motorcycle", "bicycle"
    }

    def __init__(self, model_path: str = settings.YOLO_MODEL_PATH, conf_threshold: float = settings.YOLO_CONF_THRESHOLD):
        self.detector = YOLOInference(model_path=model_path, conf_threshold=conf_threshold)

    @staticmethod
    def _risk_weight_for_detection(label: str, width: float, height: float) -> float:
        area_factor = min((width * height) / 50000.0, 1.0)

        if label.lower() in {"truck", "bus", "building"}:
            class_factor = 0.9
        elif label.lower() in {"car", "person", "motorcycle", "bicycle"}:
            class_factor = 0.7
        else:
            class_factor = 0.5

        return round(min(1.0, 0.5 * class_factor + 0.5 * area_factor), 3)

    def analyze_image(self, image_path: str) -> ObstacleAnalysisResult:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        raw_detections = self.detector.predict_image(image_path)
        detections: List[ObstacleDetection] = []

        for det in raw_detections:
            risk_weight = self._risk_weight_for_detection(
                label=det["label"],
                width=det["width"],
                height=det["height"],
            )
        DRONE_OBSTACLE_CLASSES = {
           "person": "human",
           "car": "vehicle",
           "truck": "heavy_vehicle",
           "bus": "heavy_vehicle",
           "motorcycle": "vehicle",
           "bicycle": "vehicle",
           "tree": "natural_obstacle",
           "building": "structure"
           }
        detections.append(
                ObstacleDetection(
                    label = DRONE_OBSTACLE_CLASSES.get(det["label"], det["label"]),
                    confidence=det["confidence"],
                    bounding_box=det["bounding_box"],
                    center_x=det["center_x"],
                    center_y=det["center_y"],
                    width=det["width"],
                    height=det["height"],
                    risk_weight=risk_weight,
                )
            )

        obstacle_count = len(detections)
        blocked = obstacle_count >= 8 or any(d.risk_weight > 0.9 for d in detections)
        blocked_reason = None
        if blocked:
            blocked_reason = "Dense or large obstacles detected in the current frame."

        return ObstacleAnalysisResult(
            image_path=image_path,
            detections=detections,
            obstacle_count=obstacle_count,
            blocked=blocked,
            blocked_reason=blocked_reason,
        )