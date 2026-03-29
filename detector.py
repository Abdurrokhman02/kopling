import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter

class WasteDetector:
    def __init__(self, model_path="model.tflite"):
        self.model_path = model_path
        
        # Load TFLite model
        self.interpreter = Interpreter(model_path=self.model_path, num_threads=4)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Ambil ukuran input YOLOv8 (biasanya 640x640 atau 320x320)
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        self.is_floating_model = (self.input_details[0]['dtype'] == np.float32)
        
        # Masukkan urutan labelmu di sini (sesuaikan dengan saat training di Ultralytics/Roboflow)
        self.labels = ["organik", "plastic", "b3"]

    def detect(self, frame):
        # --- 1. PRE-PROCESSING ---
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image_rgb, (self.width, self.height))
        input_data = np.expand_dims(image_resized, axis=0)
        
        if self.is_floating_model:
            input_data = input_data.astype(np.float32) / 255.0

        # --- 2. INFERENSI ---
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        # --- 3. POST-PROCESSING KHUSUS YOLOV8 ---
        # Ambil tensor output (biasanya shape-nya [1, num_classes + 4, 8400])
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        
        # Transpose matriks agar lebih mudah dibaca menjadi baris per deteksi
        output_data = np.transpose(output_data)

        boxes = []
        scores = []
        class_ids = []

        # Looping semua kemungkinan deteksi (ribuan baris)
        for row in output_data:
            # 4 nilai pertama adalah koordinat kotak (x_center, y_center, width, height)
            box = row[:4] 
            # Nilai sisanya adalah skor probabilitas untuk tiap kelas
            classes_scores = row[4:] 
            
            # Cari kelas dengan skor paling tinggi
            class_id = np.argmax(classes_scores)
            score = classes_scores[class_id]

            # Filter deteksi yang skornya di atas 60%
            if score > 0.6:
                boxes.append(box.tolist())
                scores.append(float(score))
                class_ids.append(class_id)

        detections = []
        
        # --- 4. NON-MAXIMUM SUPPRESSION (NMS) ---
        # Menghapus kotak deteksi yang bertumpuk pada satu objek yang sama
        if len(boxes) > 0:
            # Format kotak YOLOv8 adalah (xc, yc, w, h), OpenCV butuh format kotak untuk NMS.
            # Kita bisa langsung masukkan karena NMS OpenCV cukup toleran, 
            # tapi parameter threshold-nya kita set (Score Threshold=0.6, NMS Threshold=0.4)
            indices = cv2.dnn.NMSBoxes(boxes, scores, 0.6, 0.4)
            
            if len(indices) > 0:
                for i in indices.flatten():
                    label_name = self.labels[class_ids[i]] if class_ids[i] < len(self.labels) else "unknown"
                    detections.append({
                        "label": label_name,
                        "confidence": scores[i]
                    })
                    
        return detections