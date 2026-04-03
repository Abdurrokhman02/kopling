# ==========================================
# KONFIGURASI SISTEM KOPLING
# ==========================================

# --- PENGATURAN PIN GPIO (Format BCM) ---
PIN_SERVO = 18
PIN_STEPPER_DIR = 20
PIN_STEPPER_STEP = 21
PIN_STEPPER_ENABLE = None # Isi dengan angka pin jika ingin diaktifkan, atau None

# --- PENGATURAN I2C ---
LCD_I2C_ADDRESS = 0x27

# --- PENGATURAN PENGGUNA (RFID) ---
DAFTAR_USER = [
    123456789012, 
    987654321098
]

# --- PENGATURAN MEKANIK SERVO (Box Atas) ---
SERVO_OPEN_ANGLE = 90
SERVO_CLOSE_ANGLE = 0
SERVO_DROP_DELAY = 3 # Lama waktu tunggu (detik) saat sampah dijatuhkan

# --- PENGATURAN MOTOR STEPPER (Tong Bawah) ---
# Nema 17 standar = 200 langkah per 360 derajat
STEPPER_DELAY = 0.005
STEP_ORGANIK = 0     # Titik default
STEP_ANORGANIK = 66  # Putaran ~120 derajat
STEP_B3 = 133        # Putaran ~240 derajat