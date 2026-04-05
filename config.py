# ==========================================
# KONFIGURASI SISTEM KOPLING
# ==========================================

# --- PENGATURAN PIN GPIO (Format BCM) ---
PIN_SERVO = 17
PIN_STEPPER_DIR = 16
PIN_STEPPER_STEP = 12
PIN_STEPPER_ENABLE = 20 # Isi dengan angka pin jika ingin diaktifkan, atau None

# --- PENGATURAN I2C ---
LCD_I2C_ADDRESS = 0x27

# --- PENGATURAN PENGGUNA (RFID) ---
DAFTAR_USER = [
    893884915489, 
    893655474073
]

# --- PENGATURAN MEKANIK SERVO (Box Atas) ---
SERVO_OPEN_ANGLE = 180
SERVO_CLOSE_ANGLE = 0
SERVO_DROP_DELAY = 3 # Lama waktu tunggu (detik) saat sampah dijatuhkan

# --- PENGATURAN MOTOR STEPPER (Tong Bawah) ---
# Nema 17 standar = 200 langkah per 360 derajat
STEPPER_DELAY = 0.005
STEP_ORGANIK = 1200     # Titik default
STEP_ANORGANIK = 1200   # Putaran ~120 derajat
STEP_B3 =  1200         # Putaran ~240 derajat