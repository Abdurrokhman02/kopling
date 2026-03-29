import time
import RPi.GPIO as GPIO
from camera import Camera
from detector import WasteDetector
from processor import WasteProcessor
from rfid_reader import RFIDReader
from display import LCDDisplay

def main():
    # --- INISIALISASI ---
    # cam = Camera()
    # detector = WasteDetector()
    # processor = WasteProcessor()
    
    DAFTAR_USER = [123456789012, 987654321098] 
    
    rfid = RFIDReader(DAFTAR_USER)
    lcd = LCDDisplay(i2c_address=0x27)
    
    print("Sistem Kopling Siap Beroperasi (Tekan Ctrl+C untuk berhenti)")
    
    try:
        # --- INFINITE LOOP IOT ---
        while True:
            # 1. Status Standby
            lcd.show_message("Sistem Kopling", "Tempelkan Kartu")
            
            # 2. Menunggu RFID Ditempel
            # Program akan tertahan di baris ini sampai ada kartu
            uid = rfid.read_card() 
            print(f"\n[INFO] ID Kartu Terbaca: {uid}")
            
            # 3. Proses Verifikasi
            if rfid.is_verified(uid):
                print("[STATUS] Terverifikasi")
                lcd.show_message("Terverifikasi!", "Silakan Buang")
                
                # --- TEMPAT PROSES AI & KAMERA ---
                # frame = cam.capture()
                # detections = detector.detect(frame)
                # result = processor.process(detections)
                # print(result)
                # -------------------------------
                
                # Jeda waktu saat user membuang sampah
                time.sleep(5) 
                
            else:
                print("[STATUS] Akses Ditolak - Tidak Terdaftar")
                lcd.show_message("Akses Ditolak", "Tdk Terverifikasi")
                
                # Jeda sebentar agar pesan terbaca sebelum kembali standby
                time.sleep(3)
                
            # Setelah jeda, loop akan kembali ke atas (Status Standby)

    except KeyboardInterrupt:
        # Menangkap sinyal Ctrl+C dari user
        print("\n[INFO] Mematikan sistem Kopling...")
        lcd.show_message("Sistem Dimatikan")
        time.sleep(2)
        
    except Exception as e:
        # Menangkap error lain yang tidak terduga
        print(f"\n[ERROR] Terjadi kesalahan fatal: {e}")
        lcd.show_message("Sistem Error!", "Cek Log")
        
    finally:
        # Reset pin GPIO dan matikan LCD secara aman
        GPIO.cleanup()
        lcd.clear()
        print("[INFO] GPIO Cleaned up. Selesai.")

if __name__ == "__main__":
    main()