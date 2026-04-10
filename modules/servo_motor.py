from gpiozero import Servo
import time

class ServoMotor:
    def __init__(self, pin=18):
        """
        Inisialisasi motor servo MG996R kontinyu (360 derajat) menggunakan gpiozero.Servo.
        Default menggunakan pin GPIO 18 (format BCM).
        """
        self.pin = pin
        # Servo untuk kontrol kontinyu: value -1 (CW), 0 (stop), 1 (CCW)
        self.servo = Servo(pin)

    def set_speed(self, speed):
        """
        Mengatur kecepatan dan arah rotasi servo kontinyu MG996R.
        Speed: -100 (full clockwise) sampai 100 (full counter-clockwise).
        0 = stop.
        """
        # Map speed -100 to 100 ke value -1 to 1
        value = speed / 100.0
        self.servo.value = value

    def rotate_degrees(self, degrees, speed=50):
        """
        Rotasi servo kontinyu sejumlah derajat pada kecepatan tertentu.
        Degrees positif: counter-clockwise, negatif: clockwise.
        Speed: 1-100, kecepatan rotasi.
        """
        # Asumsi: pada speed 100 (value=1), servo berputar ~60 RPM atau sekitar 360 derajat per 6 detik.
        # Jadi, untuk 90 derajat: 90/360 * 6 = 1.5 detik pada speed 100.
        # Waktu = (abs(degrees) / 360) * (100 / speed) * 6
        rpm_at_100 = 60  # asumsi 60 RPM pada full speed
        time_per_360 = 60 / rpm_at_100  # detik per 360 derajat pada speed 100
        time_needed = (abs(degrees) / 360) * time_per_360 * (100 / speed)
        
        direction = 1 if degrees > 0 else -1
        self.set_speed(direction * speed)
        time.sleep(time_needed)
        self.set_speed(0)

    def drop_waste(self):
        """
        Fungsi utama untuk membuka katup pembuangan sampah dengan rotasi 90 derajat
        dan menutupnya kembali.
        """
        print("[INFO] Menggerakkan servo: Membuka pintu box (rotasi 90 derajat)...")
        self.rotate_degrees(90, speed=50)  # Rotasi 90 derajat CCW
        
        # Jeda waktu menunggu sampah jatuh
        time.sleep(1)
        
        print("[INFO] Menggerakkan servo: Menutup pintu box (rotasi kembali 90 derajat)...")
        self.rotate_degrees(-90, speed=50)  # Rotasi 90 derajat CW

    def cleanup(self):
        """Menghentikan servo saat sistem dimatikan."""
        self.servo.value = None  # Disable signal