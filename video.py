
import picamera
import time
import pygame
from pygame.locals import *
import io
import faulthandler

faulthandler.enable()


#Initialisiere PyGame

 

pygame.init()


#Einstellungen für das Pygame -Fenster


window_size = (800, 600) #Anpassen der Fenstergröße nach Bedarf

screen = pygame.display.set_mode(window_size)

pygame.display.set_caption("Picamera Live Feed")

# Erstellen des Kameraobjekts
camera = picamera.PiCamera()
camera.rotation = 270

try:
    
    # Größe der Vorschau festlegen
    camera.resolution = (640, 480)
    
    # Starte die Kameravorschau
    camera.start_preview()
        
    # Warten bis Kameravorschau gestartet ist
    time.sleep(2)
    
    while True:
        # Erfassen des Kamerabilds und Zeichnen auf das Surface-Objekt
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        image = pygame.image.load(stream)
        screen.blit(image, (0, 0))
        pygame.display.flip()
        
       

  
except KeyboardInterrupt:
    # Beenden der Kameravorschau und schließen der Kamera
    camera.stop_preview()
    camera.close()
    
finally:
    pygame.quit()
        
        
