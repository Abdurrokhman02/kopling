import cv2
from ultralytics import YOLO

# 1. Load model
model = YOLO('models/model.tflite', task='detect')

def deteksi_sekali_jepret():
    cap = cv2.VideoCapture(0)
    
    # Warm up kamera
    for _ in range(30): cap.read()
    success, frame = cap.read()
    cap.release() # Langsung lepas biar hemat RAM

    if not success:
        return "Error Kamera", {}

    # 2. Proses deteksi
    # conf=0.5 artinya hanya ambil yang tingkat keyakinannya di atas 50%
    results = model.predict(frame, conf=0.1, imgsz=320)
    
    # 3. Analisis Hasil (Menghitung jumlah benda per label)
    counts = {}
    
    for r in results:
        for box in r.boxes:
            # Ambil ID kelas (misal: 0, 1, 2)
            class_id = int(box.cls[0])
            # Ubah ID jadi nama label (misal: 'Botol', 'Organik')
            label = model.names[class_id]
            
            # Hitung jumlahnya
            counts[label] = counts.get(label, 0) + 1

    return counts

# --- CARA PAKAI ---
if __name__ == "__main__":
    print("Menganalisis sampah...")
    hasil = deteksi_sekali_jepret()
    
    if isinstance(hasil, dict) and hasil:
        print("\n--- HASIL DETEKSI ---")
        for benda, jumlah in hasil.items():
            print(f"Item: {benda} | Jumlah: {jumlah}")
            
        # Contoh logika buat LCD nanti:
        # if 'Anorganik' in hasil:
        #    lcd.write_string("Jenis: Anorganik")
    else:
        print("Tidak ada sampah terdeteksi atau kamera error.")