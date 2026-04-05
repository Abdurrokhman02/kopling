import cv2
from ultralytics import YOLO

class WasteDetector:
    def __init__(self, model_path="models/model.tflite", conf=0.1, imgsz=320):
        self.model = YOLO(model_path, task="detect")
        self.conf = conf
        self.imgsz = imgsz

    def detect(self, frame):
        if frame is None:
            raise ValueError("Frame tidak boleh None. Gunakan Camera.capture() untuk mengambil frame.")

        results = self.model.predict(frame, conf=self.conf, imgsz=self.imgsz)
        detections = []

        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                label = self.model.names[class_id]
                confidence = float(box.conf[0]) if hasattr(box, "conf") else None
                detections.append({
                    "label": label,
                    "confidence": confidence
                })

        return detections

if __name__ == "__main__":
    detector = WasteDetector()
    print("Menganalisis sampah...")

    try:
        import time
        from modules.camera import Camera

        cam = Camera()
        frame = cam.capture()
        detections = detector.detect(frame)

        if detections:
            print("\n--- HASIL DETEKSI ---")
            for item in detections:
                print(f"Label: {item['label']} | Confidence: {item['confidence']}")
        else:
            print("Tidak ada objek terdeteksi.")
    except Exception as e:
        print(f"Terjadi error: {e}")