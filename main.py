import time
import RPi.GPIO as GPIO
from kopling.core.camera import Camera
from kopling.core.detector import WasteDetector
from kopling.core.processor import WasteProcessor
from kopling.core.rfid_reader import RFIDReader
from kopling.core.display import LCDDisplay

# 1. TAMBAHKAN IMPORT INI
from kopling.core.servo_motor import ServoMotor 

def main():
    # --- INISIALISASI ---
    # cam = Camera()
    # detector = WasteDetector()
    # processor = WasteProcessor()
    
    DAFTAR_USER = [123456789012, 987654321098] 
    
    rfid = RFIDReader(DAFTAR_USER)
    lcd = LCDDisplay(i2c_address=0x27)
    
    # 2. INISIALISASI SERVO (Misal terpasang di pin BCM 18)
    servo = ServoMotor(pin=18) 
    
    print("Sistem Kopling Siap Beroperasi (Tekan Ctrl+C untuk berhenti)")
    
    try:
        # --- INFINITE LOOP IOT ---
        while True:
            lcd.show_message("Sistem Kopling", "Tempelkan Kartu")
            
            uid = rfid.read_card() 
            print(f"\n[INFO] ID Kartu Terbaca: {uid}")
            
            if rfid.is_verified(uid):
                print("[STATUS] Terverifikasi")
                lcd.show_message("Terverifikasi!", "System Bekerja")
                
                # Jeda waktu memberi kesempatan user memasukkan sampah ke box atas
                time.sleep(5) 
                
                lcd.show_message("Memproses AI...", "Mohon Tunggu")
                
                # --- TEMPAT PROSES AI & KAMERA ---
                # frame = cam.capture()
                # detections = detector.detect(frame)
                # result = processor.process(detections)
                # print(result)
                # -------------------------------
                
                # 3. SETELAH AI SELESAI, JATUHKAN SAMPAH KE BAWAH
                lcd.show_message("Menjatuhkan", "Sampah...")
                servo.drop_waste(open_angle=90, close_angle=0, delay=3)
                
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
        # 4. PASTIKAN SERVO DI-CLEANUP
        servo.cleanup()
        GPIO.cleanup()
        lcd.clear()
        print("[INFO] GPIO Cleaned up. Selesai.")

if __name__ == "__main__":
    main()