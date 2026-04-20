import cv2
from ultralytics import YOLO
import threading


class RTSPStreamService:
    def __init__(self, rtsp_url: str, model_path: str = "models/yolo11n.pt"):
        self.rtsp_url = rtsp_url
        self.model = YOLO(model_path)
        self.cap = None
        self.running = False
        self.latest_frame = None
        self.detections = []

    def start(self):
        self.cap = cv2.VideoCapture(self.rtsp_url)

        if not self.cap.isOpened():
            raise Exception("Failed to open RTSP stream")

        self.running = True
        thread = threading.Thread(target=self._read_stream, daemon=True)
        thread.start()

    def _read_stream(self):
        while self.running:
            ret, frame = self.cap.read()

            if not ret:
                continue

            self.latest_frame = frame
            self._run_inference(frame)

    def _run_inference(self, frame):
        results = self.model(frame)

        detections = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                detections.append({
                    "label": self.model.names[cls],
                    "confidence": conf,
                    "bbox": [x1, y1, x2, y2]
                })

        self.detections = detections

    def get_latest(self):
        return {
            "frame_available": self.latest_frame is not None,
            "detections": self.detections
        }

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()