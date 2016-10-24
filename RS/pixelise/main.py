import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Declare all variables etc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

windowWidth = 800
windowHeight = 600

tileSize = 40

redTotal = 0
greenTotal = 0
blueTotal = 0
colourCount = 0
currentStartX = 0
currentEndX = 0
currentStartY = 0
currentEndY = 0

doingSomethingToPassTheTime = 0

window = pygame.display.set_mode((windowWidth, windowHeight))
picture = pygame.image.load('pic6.png')
picture = pygame.transform.scale(picture, (windowWidth, windowHeight))

window.blit(picture, (0, 0))


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pxArray = pygame.PixelArray(picture)

    for currentStartX in range(0, windowWidth, tileSize):
        for currentStartY in range (0, windowHeight, tileSize):

            for x in range(currentStartX, currentStartX + tileSize - 1):
                for y in range(currentStartY, currentStartY + tileSize - 1):
                    currentRed = window.get_at((x, y)).r
                    currentGreen = window.get_at((x, y)).g
                    currentBlue = window.get_at((x, y)).b

                    redTotal += currentRed
                    greenTotal += currentGreen
                    blueTotal += currentBlue
                    colourCount += 1

            newRed = redTotal / colourCount
            newGreen = greenTotal / colourCount
            newBlue = blueTotal / colourCount

            pxArray[currentStartX : currentStartX + tileSize, currentStartY : currentStartY + tileSize] = (newRed, newGreen, newBlue)
            colourCount = 0
            redTotal = 0
            greenTotal = 0
            blueTotal = 0

    pict = pxArray.make_surface()

    del pxArray

    window.blit(pict, (0, 0))

    pygame.display.update()


