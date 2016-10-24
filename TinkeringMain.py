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

HEIGHT = 600
WIDTH = 800

window = pygame.display.set_mode((WIDTH, HEIGHT))
picture = pygame.image.load('picture.bmp')
picture = pygame.transform.scale(picture, (WIDTH, HEIGHT))


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pxArray = pygame.PixelArray(pict)
    for x in range(0, windowWidth - 1):
        for y in range(0, windowHeight - 1):
            currentRed = window.get_at((x, y)).r
            currentGreen = window.get_at((x, y)).g
            currentBlue = window.get_at((x, y)).b

            pixelSum = (currentRed + currentGreen + currentBlue) / 3

            nextPixelSum = (window.get_at((x + 1, y + 1)).r + window.get_at((x + 1, y + 1)).g + window.get_at(
                (x + 1, y + 1)).b) / 3

            diff = 255 - abs(nextPixelSum - pixelSum)

            pxArray[x, y] = (diff, diff, diff)


            # if currentRed > 150 and currentGreen < 100 and currentBlue < 100:
            #   currentRed = 0

            # pxArray[x, y] = (currentRed, currentGreen, currentBlue)

    pict = pxArray.make_surface()

    del pxArray

    window.blit(pict, (0, 0))

    pygame.display.update()