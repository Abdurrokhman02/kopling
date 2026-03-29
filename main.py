from camera import Camera
from detector import WasteDetector
from processor import WasteProcessor

def main():
    cam = Camera()
    detector = WasteDetector()
    processor = WasteProcessor()
    
    print("mengambil gambar...")
    frame = cam.capture()
    
    print("Deteksi...")
    detections = detector.detect(frame)
    
    print("Processing...")
    result = processor.process(detections)
    
    print("\n HASIL")
    print("jumlah per label: :", result[label_count"])
    print("jumlah per kategori:", result["category_count])
    print("Total poin:", result["total_points"])
    print("Kategori dominan:", result["dominant_category"])
    
if __name__ == "__main__":
    main()
    
    