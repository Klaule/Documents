import time
import pygame
from pygame.locals import *
from picamera2 import Picamera2

# Initialisiere PyGame
pygame.init()

# Einstellungen für das Pygame-Fenster
window_size = (800, 600)  # Anpassen der Fenstergröße nach Bedarf
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Picamera2 Live Feed")

# Erstellen des Picamera2-Objekts
camera = Picamera2()

# Kamera konfigurieren
camera.configure(camera.create_preview_configuration(main={"format": "RGB888", "size": (640, 480), "fps"}))
camera.set_controls({"AwbEnable": False, "AeEnable": False})
camera.set_controls({"AnalogueGain": 1.0, "ExposureTime": 10000})  # Anpassbar je nach Lichtverhältnissen


# Starte die Kamera
camera.start()

# Konvertiere das Bildformat für die Anzeige in Pygame
def convert_image(buffer):
    image_surface = pygame.image.frombuffer(buffer, (640, 480), "RGB")  # Korrektes Format sicherstellen
    # Dreh das Bild um 180 Grad
    return pygame.transform.rotate(pygame.transform.scale(image_surface, window_size), 180)

try:
    while True:
        # Erfassen des Kamerabilds
        buffer = camera.capture_array()
        
        # Konvertiere das Bild und zeige es auf dem Bildschirm an
        image = convert_image(buffer)
        screen.blit(image, (0, 0))
        pygame.display.flip()
        time.sleep(1 / 30)  # Synchronisiere die Anzeige mit der Framerate (30 fps)


        # Beenden des Programms bei Tastendruck
        for event in pygame.event.get():
            if event.type == QUIT:
                raise KeyboardInterrupt

except KeyboardInterrupt:
    # Beenden der Kameravorschau und schließen der Kamera
    camera.stop()

finally:
    pygame.quit()
