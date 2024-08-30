from gpiozero import MotionSensor
from picamera2 import Picamera2
from datetime import datetime
import time
import threading

# Setup
pir = MotionSensor(23)
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

def motion_detected():
    global recording, last_motion_time
    current_time = time.time()
    if not recording and (current_time - last_motion_time) > 20:
        recording = True
        print("Aufnahme")
        last_motion_time = current_time
        threading.Thread(target=record_video).start()

# Event detection
pir.when_motion = motion_detected
print("Bewegung erkannt")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program")
finally:
    camera.stop_preview()
