import pygame, sys, time, random
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Declare all variables etc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

HEIGHT = 400
WIDTH = 800
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()