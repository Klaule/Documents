import RPi.GPIO as GPIO
import time

# GPIO-Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO-Pin festlegen
TASTER_PIN = 17

# Pin als Ausgang festlegen
GPIO.setup(TASTER_PIN, GPIO.OUT)

try:
    while True:
        # Simuliere Taster gedrückt
        GPIO.output(TASTER_PIN, GPIO.HIGH)
        print("Taster gedrückt")
        time.sleep(1)
        
        # Simuliere Taster nicht gedrückt
        GPIO.output(TASTER_PIN, GPIO.LOW)
        print("Taster nicht gedrückt")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
