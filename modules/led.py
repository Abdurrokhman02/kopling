import RPi.GPIO as GPIO
import time

class LEDController:
    def __init__(self, red_pin, yellow_pin, green_pin):
        """
        Inisialisasi LED Controller dengan 3 LED
        
        Args:
            red_pin: GPIO pin untuk LED merah (sistem ON)
            yellow_pin: GPIO pin untuk LED kuning (processing)
            green_pin: GPIO pin untuk LED hijau (RFID verified)
        """
        self.red_pin = red_pin
        self.yellow_pin = yellow_pin
        self.green_pin = green_pin
        
        # Setup GPIO pins sebagai OUTPUT
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.yellow_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        
        # Matikan semua LED di awal
        self.all_off()
        
    def red_on(self):
        """Nyalakan LED merah"""
        GPIO.output(self.red_pin, GPIO.HIGH)
        print("[LED] Merah: ON")
        
    def red_off(self):
        """Matikan LED merah"""
        GPIO.output(self.red_pin, GPIO.LOW)
        print("[LED] Merah: OFF")
        
    def yellow_on(self):
        """Nyalakan LED kuning"""
        GPIO.output(self.yellow_pin, GPIO.HIGH)
        print("[LED] Kuning: ON")
        
    def yellow_off(self):
        """Matikan LED kuning"""
        GPIO.output(self.yellow_pin, GPIO.LOW)
        print("[LED] Kuning: OFF")
        
    def green_on(self):
        """Nyalakan LED hijau"""
        GPIO.output(self.green_pin, GPIO.HIGH)
        print("[LED] Hijau: ON")
        
    def green_off(self):
        """Matikan LED hijau"""
        GPIO.output(self.green_pin, GPIO.LOW)
        print("[LED] Hijau: OFF")
        
    def all_on(self):
        """Nyalakan semua LED"""
        self.red_on()
        self.yellow_on()
        self.green_on()
        
    def all_off(self):
        """Matikan semua LED"""
        self.red_off()
        self.yellow_off()
        self.green_off()
        
    def blink(self, led_color, times=3, interval=0.5):
        """
        Membuat LED berkedip
        
        Args:
            led_color: 'red', 'yellow', atau 'green'
            times: jumlah kali berkedip
            interval: durasi on/off dalam detik
        """
        led_on = getattr(self, f"{led_color}_on")
        led_off = getattr(self, f"{led_color}_off")
        
        for _ in range(times):
            led_on()
            time.sleep(interval)
            led_off()
            time.sleep(interval)
            
    def cleanup(self):
        """Bersihkan GPIO dan matikan semua LED"""
        self.all_off()
        print("[LED] Cleanup - semua LED dimatikan")
