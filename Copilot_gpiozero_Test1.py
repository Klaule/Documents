import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected!")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()
