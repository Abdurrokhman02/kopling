import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, dir_pin=20, step_pin=21, enable_pin=None):
        """
        Inisialisasi motor stepper Nema 17 dengan driver A4988.
        - dir_pin: Pin untuk mengatur arah putaran.
        - step_pin: Pin untuk memberikan sinyal langkah (pulse).
        - enable_pin: (Opsional) Pin untuk menyalakan/mematikan motor agar tidak panas saat standby.
        """
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.enable_pin = enable_pin
        
        # Setup pin sebagai Output
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        
        if self.enable_pin is not None:
            GPIO.setup(self.enable_pin, GPIO.OUT)
            # LOW pada A4988 berarti motor aktif (Enable)
            GPIO.output(self.enable_pin, GPIO.LOW)

    def move(self, steps, clockwise=True, delay=0.002):
        """
        Fungsi untuk memutar motor.
        Nema 17 standar memiliki 200 langkah per 1 putaran penuh (360 derajat).
        
        - steps: Jumlah langkah.
        - clockwise: True (searah jarum jam), False (berlawanan).
        - delay: Jeda waktu per langkah (semakin kecil = semakin cepat putarannya).
        """
        # Atur arah putaran
        if clockwise:
            GPIO.output(self.dir_pin, GPIO.HIGH)
        else:
            GPIO.output(self.dir_pin, GPIO.LOW)
            
        print(f"[INFO] Stepper bergerak {steps} langkah. Arah: {'CW' if clockwise else 'CCW'}")
        
        # Berikan sinyal pulse HIGH lalu LOW untuk menciptakan 1 langkah
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

    def disable(self):
        """Mematikan arus ke motor agar tidak panas saat standby (jika pakai pin Enable)."""
        if self.enable_pin is not None:
            GPIO.output(self.enable_pin, GPIO.HIGH)
            
    def enable(self):
        """Menyalakan arus kembali sebelum bergerak."""
        if self.enable_pin is not None:
            GPIO.output(self.enable_pin, GPIO.LOW)
            time.sleep(0.1) # Jeda sebentar agar arus stabil

    def cleanup(self):
        """Membersihkan status pin saat sistem dimatikan."""
        self.disable()