from typing import List, Dict, Any
from ml.object_detection.model_loader import YOLOModelLoader


class YOLOInference:
    def __init__(self, model_path: str, conf_threshold: float = 0.25):
        self.model = YOLOModelLoader.get_model(model_path)
        self.conf_threshold = conf_threshold

    def predict_image(self, image_path: str) -> List[Dict[str, Any]]:
        results = self.model.predict(
            source=image_path,
            conf=self.conf_threshold,
            verbose=False,
        )

        detections: List[Dict[str, Any]] = []

        for result in results:
            if result.boxes is None:
                continue

            for box in result.boxes:
                conf = float(box.conf[0].item())
                cls_idx = int(box.cls[0].item())
                label = result.names.get(cls_idx, str(cls_idx))

                x1, y1, x2, y2 = map(float, box.xyxy[0].tolist())
                width = x2 - x1
                height = y2 - y1
                center_x = x1 + width / 2.0
                center_y = y1 + height / 2.0

                detections.append({
                    "label": label,
                    "confidence": conf,
                    "bounding_box": {
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                    },
                    "center_x": center_x,
                    "center_y": center_y,
                    "width": width,
                    "height": height,
                })

        return detections