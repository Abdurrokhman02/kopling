import time
import RPi.GPIO as GPIO

# Import modul Kopling
from modules.camera import Camera
from modules.detector import WasteDetector
from modules.processor import WasteProcessor
from modules.rfid_reader import RFIDReader
from modules.display import LCDDisplay
from modules.servo_motor import ServoMotor
from modules.stepper_motor import StepperMotor

# Import file konfigurasi yang baru dibuat
import config

def setup_gpio_mode():
    current_mode = GPIO.getmode()

    if current_mode is None:
        GPIO.setmode(GPIO.BCM)
    elif current_mode != GPIO.BCM:
        raise RuntimeError(
            "Mode GPIO tidak konsisten, proyek ini menggunakan BCM"
            "kembalikan semua GPIO.setmode() ke GPIO.BCM"
        )

def main():
    setup_gpio_mode()

    # --- INISIALISASI HARDWARE MENGGUNAKAN CONFIG ---
    rfid = RFIDReader(config.DAFTAR_USER)
    lcd = LCDDisplay(i2c_address=config.LCD_I2C_ADDRESS)
    servo = ServoMotor(pin=config.PIN_SERVO)
    stepper = StepperMotor(
        dir_pin=config.PIN_STEPPER_DIR, 
        step_pin=config.PIN_STEPPER_STEP, 
        enable_pin=config.PIN_STEPPER_ENABLE
    )
    
    cam = Camera()
    detector = WasteDetector()
    processor = WasteProcessor()
    
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
                frame = cam.capture()
                detections = detector.detect(frame)
                result = processor.process(detections)
                
                kategori = result.get("dominant_category")
                print(f"[INFO] Hasil Deteksi: {kategori}")
                
                # --- LOGIKA STEPPER ---
                langkah_kembali = 0
                arah_kembali = False # Berlawanan jarum jam
                
                if kategori == "organik":
                    lcd.show_message("Kategori:", "Organik")
                    langkah_kembali = config.STEP_ORGANIK
                    
                elif kategori == "anorganik":
                    lcd.show_message("Kategori:", "Anorganik")
                    stepper.move(steps=config.STEP_ANORGANIK, clockwise=True, delay=config.STEPPER_DELAY)
                    langkah_kembali = config.STEP_ANORGANIK
                    arah_kembali = False
                    
                elif kategori == "b3":
                    lcd.show_message("Kategori:", "B3")
                    stepper.move(steps=config.STEP_B3, clockwise=True, delay=config.STEPPER_DELAY)
                    langkah_kembali = config.STEP_B3
                    arah_kembali = False
                
                else:
                    lcd.show_message("Kategori:", "Tidak Dikenali")
                
                time.sleep(1) 
                
                # --- LOGIKA SERVO ---
                lcd.show_message("Menjatuhkan", "Sampah...")
                servo.drop_waste(
                    open_angle=config.SERVO_OPEN_ANGLE, 
                    close_angle=config.SERVO_CLOSE_ANGLE, 
                    delay=config.SERVO_DROP_DELAY
                )
                
                # --- KEMBALIKAN POSISI TONG ---
                if langkah_kembali > 0:
                    print("[INFO] Mengembalikan posisi tong bawah ke default...")
                    stepper.move(steps=langkah_kembali, clockwise=arah_kembali, delay=config.STEPPER_DELAY)
                
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
        servo.cleanup()
        stepper.cleanup()
        GPIO.cleanup()
        lcd.clear()
        print("[INFO] GPIO Cleaned up. Selesai.")

if __name__ == "__main__":
    main()