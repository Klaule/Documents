import RPi.GPIO as GPIO
import time

PIR_PIN = 17  # or whichever pin you're using

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    while True:
        input_state = GPIO.input(PIR_PIN)
        if input_state:
            print("Motion detected!")
        else:
            print("No motion")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()

# Hallo 