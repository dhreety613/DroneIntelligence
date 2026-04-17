from ultralytics import YOLO


class YOLOModelLoader:
    _model = None

    @classmethod
    def get_model(cls, model_path: str):
        if cls._model is None:
            print(f"Loading YOLO model from {model_path}...")
            cls._model = YOLO(model_path)
        return cls._model