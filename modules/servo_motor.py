import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pin=18):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(0)

    def set_speed(self, speed, duration):
        """
        speed: -100 (full speed balik), 0 (berhenti), 100 (full speed maju)
        """
        # Konversi speed ke duty cycle (rentang 5% sampai 10%)
        # 7.5 adalah titik tengah (berhenti)
        duty = 7.5 + (speed / 40) 
        time.sleep(duration)
        
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
        GPIO.output(self.pin, False)

    def drop_waste(self, open_speed=50, close_speed=-50, move_duration=1.0, delay=3):
        """
        Menggunakan durasi waktu untuk membuka dan menutup.
        """
        print("[INFO] Menggerakkan servo 360: Membuka pintu...")
        self.set_speed(open_speed, 5)
        time.sleep(move_duration) # Putar selama X detik untuk membuka
        self.stop()
        
        # Jeda waktu menunggu sampah jatuh
        time.sleep(delay)
        
        print("[INFO] Menggerakkan servo 360: Menutup pintu...")
        self.set_speed(close_speed, 8)
        time.sleep(move_duration) # Putar balik selama X detik untuk menutup
        self.stop()

    def cleanup(self):
        self.pwm.stop()