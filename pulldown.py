import RPi.GPIO as GPIO
import time # datetime

# GPIO-Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO-Pin festlegen
TASTER_PIN = 17

# Pin als Ausgang festlegen
GPIO.setup(TASTER_PIN, GPIO.OUT)

try:
    while True:
        # Simuliere Taster gedr�ckt
        GPIO.output(TASTER_PIN, GPIO.HIGH)
        print("Taster gedr�ckt")
        time.sleep(1)
        
        # Simuliere Taster nicht gedr�ckt
        GPIO.output(TASTER_PIN, GPIO.LOW)
        print("Taster nicht gedr�ckt")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
