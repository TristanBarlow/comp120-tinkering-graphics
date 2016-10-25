import pygame, sys, time, random, math
from pygame.locals import *
import

pygame.init()
pygame.mixer.init()

# Declare all variables etc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

window_width = 800
window_height = 600

tile_size = 20
run_once = True

red_total = 0
green_total = 0
blue_total = 0
luminosity_total = 0

colour_count = 0

doingSomethingToPassTheTime = 0

window = pygame.display.set_mode((window_width, window_height))
picture = pygame.image.load('pic2.jpg')
picture = pygame.transform.scale(picture, (window_width, window_height))

window.blit(picture, (0, 0))


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if run_once:
        run_once = False

        pixel_array = pygame.PixelArray(picture)

        for currentStartX in range(0, window_width, tile_size):
            for currentStartY in range (0, window_height, tile_size):
                for x in range(currentStartX, currentStartX + tile_size - 1):
                    for y in range(currentStartY, currentStartY + tile_size - 1):

                        current_red = window.get_at((x, y)).r
                        current_green = window.get_at((x, y)).g
                        current_blue = window.get_at((x, y)).b

                        red_total += current_red
                        green_total += current_green
                        blue_total += current_blue
                        colour_count += 1

                new_red = red_total / colour_count
                new_green = green_total / colour_count
                new_blue = blue_total / colour_count

                pixel_array[currentStartX: currentStartX + tile_size - 5, currentStartY: currentStartY + tile_size - 5] = (new_red, new_green, new_blue)

                colour_count = 0
                red_total = 0
                green_total = 0
                blue_total = 0
                luminosity_total = 0

        pict = pixel_array.make_surface()

        del pixel_array

        window.blit(pict, (0, 0))

    #    for x in range (0, windowWidth):
     #       for x in range (0, window_height):



        pygame.display.update()

    #    pygame.time.wait(10000)

    #    dino = False


