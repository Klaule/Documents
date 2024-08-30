import RPi.GPIO as GPIO
import time

pir_pin =24

GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)

print("PIR Module Test (CTRL+C to exit)")
time.sleep(2)
print("Ready")

try:
    while True:
        if GPIO.input(pir_pin):
            print("Motion detected")
        else:
            print("No motion detected")
        time.sleep(1)

except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()
    
    
    
    
    
    