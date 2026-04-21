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
from modules.mqtt_client import MQTTClient
from modules.led import LEDController

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
    cam = Camera()
    detector = WasteDetector()
    processor = WasteProcessor()
    mqtt = MQTTClient()
    
    # Connect to MQTT broker
    if not mqtt.connect():
        print("[WARNING] MQTT connection failed, continuing without MQTT")
    else:
        # Subscribe ke topik respon autentikasi
        mqtt.subscribe("auth/response", qos=1)
    
    # Inisialisasi RFID reader dengan MQTT client untuk autentikasi
    rfid = RFIDReader(mqtt_client=mqtt)
    lcd = LCDDisplay(i2c_address=config.LCD_I2C_ADDRESS)
    servo = ServoMotor(pin=config.PIN_SERVO)
    stepper = StepperMotor(
        dir_pin=config.PIN_STEPPER_DIR, 
        step_pin=config.PIN_STEPPER_STEP, 
        enable_pin=config.PIN_STEPPER_ENABLE
    )
    
    # Inisialisasi LED Controller
    led = LEDController(
        red_pin=config.PIN_LED_RED,
        yellow_pin=config.PIN_LED_YELLOW,
        green_pin=config.PIN_LED_GREEN
    )
    
    print("Sistem Kopling Siap Beroperasi (Tekan Ctrl+C untuk berhenti)")
    
    # Nyalakan LED Merah untuk indikasi sistem ON
    led.red_on()
    
    try:
        while True:
            if not mqtt.connected:
                mqtt.reconnect()

            lcd.show_message("Sistem Kopling", "Tempelkan Kartu")
            uid = rfid.read_card() 
            print(f"\n[INFO] ID Kartu Terbaca: {uid}")
            
            if rfid.is_verified(uid):
                # Nyalakan LED Hijau untuk indikasi RFID terverifikasi
                led.green_on()
                print("[STATUS] Terverifikasi")
                lcd.show_message("Terverifikasi!", "Silakan Buang")
                time.sleep(5) 
                
                lcd.show_message("Memproses AI...", "Mohon Tunggu")
                
                # Nyalakan LED Kuning untuk indikasi proses dimulai
                led.yellow_on()

                # --- TEMPAT PROSES AI & KAMERA ---
                frame = cam.capture()
                detections = detector.detect(frame)
                result = processor.process(detections)

                status = result.get("status")
                waste_category = result.get("wasteCategory")
                details = result.get("details", [])
                jumlah = result.get("jumlah", 0)

                print(f"[INFO] Status: {status}")
                print(f"[INFO] Kategori: {waste_category}")
                print(f"[INFO] Detail: {details}")
                print(f"[INFO] Jumlah: {jumlah}")

                # Send detection result to MQTT
                mqtt.send_detection_result(uid, result)

                if status == "no_waste":
                    lcd.show_message("Tidak ada sampah", "Coba lagi")
                    time.sleep(3)
                    continue

                if status == "mixed_category":
                    lcd.show_message("Kategori beda!", "Ulangi dari awal")
                    time.sleep(4)
                    continue

                kategori = waste_category
                
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
                    open_speed=config.SERVO_OPEN_SPEED, 
                    close_speed=config.SERVO_CLOSE_SPEED, 
                    move_duration=config.SERVO_MOVE_DURATION
                )
                
                # --- KEMBALIKAN POSISI TONG ---
                if langkah_kembali > 0:
                    print("[INFO] Mengembalikan posisi tong bawah ke default...")
                    stepper.move(steps=langkah_kembali, clockwise=arah_kembali, delay=config.STEPPER_DELAY)
                
                # Matikan LED Kuning dan Hijau setelah proses selesai
                led.yellow_off()
                led.green_off()
                
                lcd.show_message("Selesai!", "Terima Kasih")
                time.sleep(2)
                
            else:
                print("[STATUS] Akses Ditolak - Tidak Terdaftar")
                lcd.show_message("Akses Ditolak", "Tdk Terverifikasi")
                lcd.show_message("Silakan Daftar", f"id: {uid}")
                time.sleep(3)

    except KeyboardInterrupt:
        print("\n[INFO] Mematikan sistem Kopling...")
        lcd.show_message("Sistem Dimatikan")
        time.sleep(2)
        
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan fatal: {e}")
        lcd.show_message("Sistem Error!", "Cek Log")
        
    finally:
        # Cleanup LED
        led.cleanup()
        mqtt.disconnect()
        servo.cleanup()
        stepper.cleanup()
        GPIO.cleanup()
        lcd.clear()
        print("[INFO] GPIO Cleaned up. Selesai.")

if __name__ == "__main__":
    main()