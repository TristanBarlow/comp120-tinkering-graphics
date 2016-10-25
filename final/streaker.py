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

windowWidth = 600
windowHeight = 400

tailLength = 200
lumTotal = 0
lumCount = 0
average_total = 0
average_counter = 0
first_pass_average = 0

window = pygame.display.set_mode((windowWidth, windowHeight))
picture = pygame.image.load('cool_cat.jpg')
picture = pygame.transform.scale(picture, (windowWidth, windowHeight))

window.blit(picture, (0, 0))
run_once = True


while True:
    if run_once:
        run_once = False

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

        lumAverage = lumTotal / lumCount
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

        pygame.time.wait(10000)

        #clock.tick



