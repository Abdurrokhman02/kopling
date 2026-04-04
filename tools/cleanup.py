import RPi.GPIO as GPIO

def cleanup_gpio():
    GPIO.cleanup()
    print("GPIO cleaned up!")

cleanup_gpio