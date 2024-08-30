import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Taster_PIN = 24

GPIO.setup(Taster_PIN, GPIO.OUT)

try:
    while True:
        #Simuliere Taster dedrückt
        GPIO.output(Taster_PIN, GPIO.HIGH)
        print("Taster gedrückt")
        time.sleep(5)
        
        #Simuliere Taster nicht gedrückt
        GPIO.output(Taster_PIN, GPIO.LOW)
        print("Taster nicht gedrückt")
        time.sleep(5)
        
except KeyboardInterrupt:
    GPIO.cleanup()