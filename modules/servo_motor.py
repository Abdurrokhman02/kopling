import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pin=18):
        """
        Inisialisasi motor servo MG996R kontinyu (360 derajat).
        Default menggunakan pin GPIO 18 (format BCM).
        """
        self.pin = pin
        
        GPIO.setup(self.pin, GPIO.OUT)
        # Frekuensi 50Hz adalah standar untuk kebanyakan motor servo
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

    def set_speed(self, speed):
        """
        Mengatur kecepatan dan arah rotasi servo kontinyu MG996R.
        Speed: -100 (full clockwise) sampai 100 (full counter-clockwise).
        0 = stop.
        """
        # Duty cycle untuk stop: 7.5%
        # Rentang: 5% (CW) sampai 10% (CCW)
        duty = 7.5 + (speed / 100) * 2.5
        
        # Batasi duty cycle antara 5% dan 10%
        duty = max(5, min(10, duty))
        
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)  # Waktu singkat untuk stabil
        
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)  # Nol-kan duty cycle

    def drop_waste(self, open_duration=3, close_duration=3):
        """
        Fungsi utama untuk membuka katup pembuangan sampah dengan rotasi kontinyu
        dan menutupnya kembali.
        """
        print("[INFO] Menggerakkan servo: Membuka pintu box...")
        self.set_speed(50)  # Rotasi CCW untuk membuka
        time.sleep(open_duration)
        self.set_speed(0)   # Stop
        
        # Jeda waktu menunggu sampah jatuh
        time.sleep(1)
        
        print("[INFO] Menggerakkan servo: Menutup pintu box...")
        self.set_speed(-50)  # Rotasi CW untuk menutup
        time.sleep(close_duration)
        self.set_speed(0)    # Stop

    def cleanup(self):
        """Menghentikan PWM saat sistem dimatikan."""
        self.pwm.stop()