import time

from modules.servo_motor import ServoMotor
import config


def main():
    servo = ServoMotor(pin=config.PIN_SERVO)

    try:
        print("[TEST] Servo MG996R kontinyu test mulai.")
        print("[TEST] Tekan Ctrl+C untuk berhenti kapan saja.")

        while True:
            print("[TEST] Rotasi 90 derajat counter-clockwise")
            servo.rotate_degrees(90, speed=50)
            time.sleep(1)

            print("[TEST] Rotasi 90 derajat clockwise (kembali)")
            servo.rotate_degrees(-90, speed=50)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[TEST] Pengujian dihentikan oleh pengguna.")

    finally:
        servo.cleanup()
        print("[TEST] Cleanup selesai.")


if __name__ == "__main__":
    main()
