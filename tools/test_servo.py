import time
import RPi.GPIO as GPIO

from modules.servo_motor import ServoMotor
import config


def main():
    GPIO.setmode(GPIO.BCM)

    servo = ServoMotor(pin=config.PIN_SERVO)

    try:
        print("[TEST] Servo MG996R kontinyu test mulai.")
        print("[TEST] Tekan Ctrl+C untuk berhenti kapan saja.")

        while True:
            print("[TEST] Rotasi counter-clockwise (membuka)")
            servo.set_speed(50)  # Kecepatan sedang CCW
            time.sleep(2)
            servo.set_speed(0)   # Stop
            time.sleep(1)

            print("[TEST] Rotasi clockwise (menutup)")
            servo.set_speed(-50)  # Kecepatan sedang CW
            time.sleep(2)
            servo.set_speed(0)    # Stop
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[TEST] Pengujian dihentikan oleh pengguna.")

    finally:
        servo.cleanup()
        GPIO.cleanup()
        print("[TEST] Cleanup selesai. GPIO telah dinonaktifkan.")


if __name__ == "__main__":
    main()
