import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def baca_id():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    reader = SimpleMFRC522()
    
    print("=== PROGRAM CEK ID KARTU ===")
    print("Tempelkan kartu RFID kamu ke sensor...")
    print("Tekan Ctrl+C untuk keluar.\n")
    
    try:
        while True:
            # Sistem akan menunggu sampai ada kartu yang ditempel
            id_kartu, text = reader.read()
            
            print(f"-> ID Kartu Terdeteksi: {id_kartu}")
            
            # Beri jeda 2 detik biar layarnya nggak *spam* kalau kartu ditahan di sensor
            time.sleep(2) 
            print("Tempelkan kartu lain...")
            
    except KeyboardInterrupt:
        print("\nSelesai mengecek kartu.")
        
    finally:
        # Selalu bersihkan pin GPIO saat selesai
        GPIO.cleanup()

if __name__ == "__main__":
    baca_id()