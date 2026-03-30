import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pin=18):
        """
        Inisialisasi motor servo.
        Default menggunakan pin GPIO 18 (format BCM).
        """
        self.pin = pin
        
        # Mengatur mode pin GPIO ke BCM
        GPIO.setmode(GPIO.BCM)
        # Menonaktifkan warning jika pin sudah pernah dipakai sebelumnya
        GPIO.setwarnings(False)
        
        GPIO.setup(self.pin, GPIO.OUT)
        # Frekuensi 50Hz adalah standar untuk kebanyakan motor servo
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

    def set_angle(self, angle):
        """Menggerakkan servo ke sudut tertentu (0 - 180 derajat)."""
        # Rumus konversi sudut ke duty cycle (biasanya rentang 2% - 12%)
        duty = 2 + (angle / 18)
        
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5) # Beri waktu servo untuk bergerak mencapai posisi
        
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0) # Nol-kan duty cycle agar servo tidak bergetar (jitter)

    def drop_waste(self, open_angle=90, close_angle=0, delay=3):
        """
        Fungsi utama untuk membuka katup pembuangan sampah 
        dan menutupnya kembali.
        """
        print("[INFO] Menggerakkan servo: Membuka pintu box...")
        self.set_angle(open_angle)
        
        # Jeda waktu menunggu sampah benar-benar jatuh ke bawah
        time.sleep(delay) 
        
        print("[INFO] Menggerakkan servo: Menutup pintu box...")
        self.set_angle(close_angle)

    def cleanup(self):
        """Menghentikan PWM saat sistem dimatikan."""
        self.pwm.stop()