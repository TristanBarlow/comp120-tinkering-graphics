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

windowWidth = 256
windowHeight = 256

tailLength = 20
lumTotal = 0
lumCount = 0
doingSomethingToPassTheTime = 0
firstPart = True
secondPart = False

window = pygame.display.set_mode((windowWidth, windowHeight))
picture = pygame.image.load('pic1.jpg')
picture = pygame.transform.scale(picture, (windowWidth, windowHeight))

window.blit(picture, (0, 0))


while firstPart == True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pxArray = pygame.PixelArray(picture)

    for x in range(0, windowWidth - 1):
        for y in range(0, windowHeight - 1):
            currentRed = window.get_at((x, y)).r
            currentGreen = window.get_at((x, y)).g
            currentBlue = window.get_at((x, y)).b
            currentAlpha = window.get_at((x, y)).a

            pxArray[currentRed, currentGreen] = RED
            pxArray[currentRed, currentBlue] = BLACK
            pxArray[currentGreen, currentRed] = GREEN
            pxArray[currentGreen, currentBlue] = BLACK
            pxArray[currentBlue, currentRed] = BLUE
            pxArray[currentBlue, currentGreen] = BLACK

    print ('checkpoint2')

    pict = pxArray.make_surface()

    del pxArray

    print('checkpoint3')

    window.blit(pict, (0, 0))

    pygame.display.update()

    print('checkpoint4')

    firstPart = False
    secondPart = True


while secondPart == True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pxArray = pygame.PixelArray(picture)

    for x in range(0, windowWidth - 1):
        for y in range(0, windowHeight - 1):
            currentRed = window.get_at((x, y)).r
            currentGreen = window.get_at((x, y)).g
            currentBlue = window.get_at((x, y)).b

            luminosity = math.sqrt(math.pow(currentRed, 2) +
                                   math.pow(currentGreen, 2) +
                                   math.pow(currentBlue, 2))
            if luminosity != 0 or luminosity < 440:
                lumTotal += luminosity
                lumCount += 1

    lumAverage = lumTotal / lumCount #(windowWidth * windowHeight)
    print('checkpoint1')
    print('average luminosity: ')
    print lumAverage
    print lumCount

    for x in range(0, windowWidth - 1):
        for y in range(0, windowHeight - 1):
            currentRed = window.get_at((x, y)).r
            currentGreen = window.get_at((x, y)).g
            currentBlue = window.get_at((x, y)).b
            currentAlpha = window.get_at((x, y)).a

            luminosity = math.sqrt(math.pow(currentRed, 2) +
                                   math.pow(currentGreen, 2) +
                                   math.pow(currentBlue, 2))

            if luminosity > lumAverage:
                for i in range (0, tailLength):
                    if x - i > 0:
                        newRed =  currentRed - (currentRed * i / tailLength)
                        newGreen = currentGreen - (currentGreen * i / tailLength)
                        newBlue = currentBlue - (currentBlue * i / tailLength)

                        pxArray[x - i, y] = (newBlue, newGreen, newRed)
            else:
                pxArray[x, y] = BLACK

    print ('checkpoint2')

    pict = pxArray.make_surface()

    del pxArray

    print('checkpoint3')

    window.blit(pict, (0, 0))

    pygame.display.update()

    print('checkpoint4')

    while True:
        doingSomethingToPassTheTime += 1
