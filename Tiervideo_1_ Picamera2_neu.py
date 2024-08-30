import logging
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from time import sleep
from datetime import datetime
import os
from threading import Thread

# Logger konfigurieren
logging.basicConfig(filename='/home/klaule/Videos/motion_log.txt', level=logging.INFO)

pir_pin = 24
temp_folder_path = "/home/klaule/Videos/temp/" 
final_folder_path = "/home/klaule/Videos/"

GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

recording_in_progress = False
camera_running = False

# Verzeichnisse erstellen, falls sie nicht existieren
os.makedirs(temp_folder_path, exist_ok=True)
os.makedirs(final_folder_path, exist_ok=True)

# Funktion, die für das kontinuierliche Aufnehmen des Videos verantwortlich ist
def record_video():
    global camera_running, temp_folder_path
    
    picam2 = Picamera2()  # Erstellen einer Picamera2-Instanz
    
    while True:
        if not camera_running:
            continue
        
        timestamp = datetime.now().strftime('%d.%m.%Y_%H:%M:%S')
        temp_video_path = os.path.join(temp_folder_path, f"{timestamp}.h264")
        
        # Video aufnehmen
        picam2.start_and_capture_files(temp_video_path, num_frames=300)  # ca. 10 Sekunden bei 30 fps
         
        if not recording_in_progress:
            os.remove(temp_video_path)

# Startet die kontinuierliche Videoaufnahme in einem separaten Thread
video_thread = Thread(target=record_video)
video_thread.start()

# Callback-Funktion für die Bewegungserkennung
def mein_callback(channel):
    global recording_in_progress, camera_running, final_folder_path
    
    if recording_in_progress:
        logging.info(f"{datetime.now()} - Recording already in progress. Ignoring motion.")
        return
    
    logging.info(f"{datetime.now()} - Bewegung erkannt!")
    print("-Bewegung erkannt!")
    recording_in_progress = True

    # Sichern der letzten 5s vor der Bewegung und Aufnehmen der nächsten 5s
    final_video_path = None

    try:
        temp_videos = sorted(os.listdir(temp_folder_path))
        if temp_videos:
            last_video = temp_videos[-1]
            final_video_path = os.path.join(final_folder_path, last_video)
            os.rename(os.path.join(temp_folder_path, last_video), final_video_path)
        
        picam2 = Picamera2()
        picam2.start_and_capture_files(final_video_path, num_frames=150)  # 5 Sekunden bei 30 fps
        
        logging.info(f"{datetime.now()} - Video {final_video_path} gespeichert")
        print(f"{datetime.now()} - Video gespeichert")
    
    finally:
        recording_in_progress = False
        logging.info(f"{datetime.now()} - Recording complete, waiting for next motion.")
    
try:
    GPIO.add_event_detect(pir_pin, GPIO.RISING, callback=mein_callback, bouncetime=300)
    logging.info("Bereit zur Bewegungserkennung. Drücke STRG+C zum Beenden.")
    camera_running = True
    while True:
        sleep(1)

except Exception as e:
    logging.error(f"Fehler: {e}")
    
finally:
    logging.info("Programm wird beendet, GPIO cleanup.")
    camera_running = False
    GPIO.cleanup()
