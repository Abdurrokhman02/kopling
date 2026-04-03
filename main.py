import time
import RPi.GPIO as GPIO
from modules.camera import Camera
from modules.detector import WasteDetector
from modules.processor import WasteProcessor
from modules.rfid_reader import RFIDReader
from modules.display import LCDDisplay
from modules.servo_motor import ServoMotor
# 1. IMPORT STEPPER
from modules.stepper_motor import StepperMotor

def main():
    # --- INISIALISASI ---
    # cam = Camera()
    # detector = WasteDetector()
    # processor = WasteProcessor()
    
    DAFTAR_USER = [123456789012, 987654321098] 
    
    rfid = RFIDReader(DAFTAR_USER)
    lcd = LCDDisplay(i2c_address=0x27)
    servo = ServoMotor(pin=18)
    
    # 2. INISIALISASI STEPPER (Sesuai pin S=21 dan D=20 yang kita bahas)
    stepper = StepperMotor(dir_pin=20, step_pin=21)
    
    print("Sistem Kopling Siap Beroperasi (Tekan Ctrl+C untuk berhenti)")
    
    try:
        while True:
            lcd.show_message("Sistem Kopling", "Tempelkan Kartu")
            uid = rfid.read_card() 
            print(f"\n[INFO] ID Kartu Terbaca: {uid}")
            
            if rfid.is_verified(uid):
                print("[STATUS] Terverifikasi")
                lcd.show_message("Terverifikasi!", "Silakan Buang")
                time.sleep(5) 
                
                lcd.show_message("Memproses AI...", "Mohon Tunggu")
                
                # --- TEMPAT PROSES AI & KAMERA ---
                # frame = cam.capture()
                # detections = detector.detect(frame)
                # result = processor.process(detections)
                
                # SIMULASI HASIL AI (Hapus 2 baris ini nanti kalau AI dinyalakan)
                result = {"dominant_category": "anorganik"} 
                
                kategori = result.get("dominant_category")
                print(f"[INFO] Hasil Deteksi: {kategori}")
                
                # 3. LOGIKA MEMUTAR TONG SAMPAH BAWAH BERDASARKAN KATEGORI
                langkah_kembali = 0
                arah_kembali = False # Berlawanan jarum jam
                
                if kategori == "organik":
                    lcd.show_message("Kategori:", "Organik")
                    # Misal posisi default sudah organik, jadi stepper tidak perlu mutar
                    langkah_kembali = 0
                    
                elif kategori == "anorganik":
                    lcd.show_message("Kategori:", "Anorganik")
                    # Misal anorganik butuh putar 66 langkah (sekitar 120 derajat) searah jarum jam
                    stepper.move(steps=66, clockwise=True, delay=0.005)
                    langkah_kembali = 66
                    arah_kembali = False
                    
                elif kategori == "b3":
                    lcd.show_message("Kategori:", "B3")
                    # Misal B3 butuh putar 133 langkah (sekitar 240 derajat) searah jarum jam
                    stepper.move(steps=133, clockwise=True, delay=0.005)
                    langkah_kembali = 133
                    arah_kembali = False
                
                else:
                    lcd.show_message("Kategori:", "Tidak Dikenali")
                
                time.sleep(1) # Jeda sebentar biar wadah di bawah stabil
                
                # 4. JATUHKAN SAMPAH DARI BOX ATAS
                lcd.show_message("Menjatuhkan", "Sampah...")
                servo.drop_waste(open_angle=90, close_angle=0, delay=3)
                
                # 5. KEMBALIKAN POSISI TONG SAMPAH KE DEFAULT (Posisi Organik)
                if langkah_kembali > 0:
                    print("[INFO] Mengembalikan posisi tong bawah ke default...")
                    stepper.move(steps=langkah_kembali, clockwise=arah_kembali, delay=0.005)
                
                lcd.show_message("Selesai!", "Terima Kasih")
                time.sleep(2)
                
            else:
                print("[STATUS] Akses Ditolak - Tidak Terdaftar")
                lcd.show_message("Akses Ditolak", "Tdk Terverifikasi")
                time.sleep(3)

    except KeyboardInterrupt:
        print("\n[INFO] Mematikan sistem Kopling...")
        lcd.show_message("Sistem Dimatikan")
        time.sleep(2)
        
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan fatal: {e}")
        lcd.show_message("Sistem Error!", "Cek Log")
        
    finally:
        # 6. PASTIKAN SEMUA HARDWARE DI-CLEANUP
        servo.cleanup()
        stepper.cleanup()
        GPIO.cleanup()
        lcd.clear()
        print("[INFO] GPIO Cleaned up. Selesai.")

if __name__ == "__main__":
    main()