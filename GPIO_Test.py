import RPi.GPIO as GPIO
import time

pir_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)

try:
    while True:
        state = GPIO.input(pir_pin)
        print(f"PIR Pin State: {state}")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
