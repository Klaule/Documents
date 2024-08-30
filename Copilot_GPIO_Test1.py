import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
PIR_PIN = 24
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.remove(24)
try:
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, )
    print("Edge detection added successfully")
except RuntimeError as e:
    print(f"Failed to add edge detection: {e}")
