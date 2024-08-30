#!/usr/bin/python3
import time
import threading
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import RPi.GPIO as GPIO
from datetime import datetime
from collections import deque

# Global Variables
PIR_PIN = 17  # Changed to GPIO 17 based on your working setup
recording = False
last_motion_time = 0
buffer = deque(maxlen=200)  # Buffer for 5 seconds (100 frames at 20 fps)
motion_detected_time = None

def setup():
    """Initial setup for GPIO and camera."""
    GPIO.cleanup()  # Clean up any previous GPIO settings
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)

    global camera, encoder
    camera = Picamera2()
    encoder = H264Encoder(bitrate=1000000)    #bitrate 1Mbit/s
    camera.start_preview()

def record_video():
    """Record video to file with 5 seconds pre and post motion detection."""
    global recording, motion_detected_time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'/home/klaule/Videos/video_{timestamp}.h264'
    output = FileOutput(filename)
    camera.start_recording(encoder, output)
    
    # Write buffered frames (frames are raw data, not encoded)
    for frame in buffer:
        output.write(frame)
    
    # Record for 5 seconds after motion
    time.sleep(10)
    camera.stop_recording()
    recording = False
    motion_detected_time = None

def motion_detected(channel):
    """Callback function triggered by PIR sensor."""
    global recording, last_motion_time, motion_detected_time
    current_time = time.time()

    # Check if we're already recording or if the timeout period has not passed
    if not recording and (current_time - last_motion_time) > 20:
        recording = True
        last_motion_time = current_time
        motion_detected_time = datetime.now()
        threading.Thread(target=record_video).start()

        # Add a 20-second delay to prevent overload
        print("motion detected")
        time.sleep(20)
        recording = False
        

def continuous_recording():
    """Continuously capture video frames and store them in a buffer."""
    global buffer
    try:
        while True:
            frame = camera.capture_buffer()
            buffer.append(frame)
            time.sleep(0.1)  # Adjust based on desired frame rate
    except KeyboardInterrupt:
        GPIO.cleanup()

def main():
    """Main function to set up event detection and start continuous recording."""
    setup()
    print(f"GPIO {PIR_PIN} setup as input: {GPIO.gpio_function(PIR_PIN) == GPIO.IN}")

    # Event detection using a simple polling mechanism
    try:
        while True:
            input_state = GPIO.input(PIR_PIN)
            if input_state:  # Motion detected
                motion_detected(PIR_PIN)

                
            time.sleep(1)  # Polling delay
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        GPIO.cleanup()
        camera.stop_preview()

if __name__ == "__main__":
    main()
