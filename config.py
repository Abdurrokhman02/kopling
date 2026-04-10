# ==========================================
# KONFIGURASI SISTEM KOPLING
# ==========================================

# --- PENGATURAN PIN GPIO (Format BCM) ---
PIN_SERVO = 17
PIN_STEPPER_DIR = 16
PIN_STEPPER_STEP = 12
PIN_STEPPER_ENABLE = 20 # Isi dengan angka pin jika ingin diaktifkan, atau None

# --- PENGATURAN PIN LED ---
PIN_LED_RED = 22      # LED Merah - Sistem ON
PIN_LED_YELLOW = 23   # LED Kuning - Proses AI/Memproses
PIN_LED_GREEN = 24    # LED Hijau - RFID Terverifikasi

# --- PENGATURAN I2C ---
LCD_I2C_ADDRESS = 0x27

# --- PENGATURAN MEKANIK SERVO (Box Atas) ---
# Servo tipe MG996R kontinyu (360 derajat), pengaturan durasi rotasi.
# SERVO_OPEN_DURATION = 3   # Lama rotasi untuk membuka (detik)
# SERVO_CLOSE_DURATION = 3  # Lama rotasi untuk menutup (detik)
# SERVO_DROP_DELAY = 3      # Lama waktu tunggu (detik) saat sampah dijatuhkan

# --- PENGATURAN MEKANIK SERVO 360 (Box Atas) ---
SERVO_OPEN_SPEED = 50      # Kecepatan buka
SERVO_CLOSE_SPEED = -50    # Kecepatan tutup (nilai negatif)
SERVO_MOVE_DURATION = 1.2  # SESUAIKAN: Berapa detik waktu yang dibutuhkan untuk membuka pintu
SERVO_DROP_DELAY = 3       # Jeda sampah jatuh

# --- PENGATURAN MOTOR STEPPER (Tong Bawah) ---
# Nema 17 standar = 200 langkah per 360 derajat
STEPPER_DELAY = 0.0005
STEP_ORGANIK = 0     # Titik default
STEP_ANORGANIK = 2200   # Putaran ~120 derajat
STEP_B3 =  1850         # Putaran ~240 derajat