import RPi.GPIO as GPIO
import time
import config

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Ambil pin dari config.py
motor_pins = [config.IN1, config.IN2, config.IN3, config.IN4]

# Set pin sebagai output
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

# Urutan langkah (Half-step)
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

print("Motor muter terus nih bro. Tekan Ctrl+C buat berhenti.")

try:
    # Loop abadi biar motor muter terus
    while True:
        for step in step_sequence:
            for i in range(len(motor_pins)):
                GPIO.output(motor_pins[i], step[i])
            time.sleep(0.001)  # Jeda 1ms, bisa dibesarkan kalau mau lebih lambat
            
except KeyboardInterrupt:
    # Dijalankan saat kamu menekan Ctrl+C
    print("\nSip, pengetesan selesai. Motor berhenti.")
    
finally:
    # Mematikan arus ke motor biar nggak panas
    for pin in motor_pins:
        GPIO.output(pin, False)
    GPIO.cleanup()