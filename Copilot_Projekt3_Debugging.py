import time
import threading
from picamera2 import Picamera2
import RPi.GPIO as GPIO
from datetime import datetime

# Setup
GPIO.setmode(GPIO.BCM)
PIR_PIN = 24
GPIO.setup(PIR_PIN, GPIO.IN)

camera = Picamera2()
camera.start_preview()

# Variables
recording = False
last_motion_time = 0

def record_video():
    global recording
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'/home/pi/video_{timestamp}.h264'
    camera.start_recording(filename)
    time.sleep(10)  # Record for 10 seconds (5s before + 5s after motion)
    camera.stop_recording()
    recording = False

def motion_detected(channel):
    global recording, last_motion_time
    current_time = time.time()
    if not recording and (current_time - last_motion_time) > 20:
        recording = True
        last_motion_time = current_time
        threading.Thread(target=record_video).start()

# Event detection
try:
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)
    print("Edge detection added successfully")
except RuntimeError as e:
    print(f"Failed to add edge detection: {e}")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()
    camera.stop_preview()
