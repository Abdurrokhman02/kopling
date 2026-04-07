import time

from modules.stepper_motor import StepperMotor
import config


def main():
    stepper = StepperMotor(
        dir_pin=config.PIN_STEPPER_DIR,
        step_pin=config.PIN_STEPPER_STEP,
        enable_pin=config.PIN_STEPPER_ENABLE,
    )

    try:
        print("[TEST] Stepper motor test mulai.")
        print("[TEST] Tekan Ctrl+C untuk berhenti kapan saja.")

        if config.PIN_STEPPER_ENABLE is not None:
            stepper.enable()

        while True:
            print("[TEST] Memutar searah jarum jam (200 langkah)")
            stepper.move(steps=200, clockwise=True, delay=0.005)
            time.sleep(1)

            print("[TEST] Memutar berlawanan jarum jam (200 langkah)")
            stepper.move(steps=200, clockwise=False, delay=0.005)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[TEST] Pengujian dihentikan oleh pengguna.")

    finally:
        stepper.cleanup()
        print("[TEST] Cleanup selesai. GPIO telah dinonaktifkan.")


if __name__ == "__main__":
    main()