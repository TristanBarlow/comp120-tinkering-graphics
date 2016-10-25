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

window_width = 800
window_height = 600

tile_size = 50
run_once = True

red_total = 0
green_total = 0
blue_total = 0
luminosity_total = 0

colour_count = 0

doingSomethingToPassTheTime = 0

window = pygame.display.set_mode((window_width, window_height))
picture = pygame.image.load('pic6.png')
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
#written twice
                    pixel_array = pygame.PixelArray(picture)
                    for y in range(currentStartY, currentStartY + tile_size - 1):
                        current_red = window.get_at((x, y)).r
                        current_green = window.get_at((x, y)).g
                        current_blue = window.get_at((x, y)).b

                        red_total += current_red
                        green_total += current_green
                        blue_total += current_blue
                        colour_count += 1

                        luminosity = math.sqrt(math.pow(current_red, 2) +
                                               math.pow(current_green, 2) +
                                               math.pow(current_blue, 2))

                        luminosity_total += luminosity

                new_red = red_total / colour_count
                new_green = green_total / colour_count
                new_blue = blue_total / colour_count

                average_luminosity = luminosity_total / colour_count


                picture2 = pygame.transform.scale(picture, (tile_size, tile_size))

                new_pixel_array = pygame.PixelArray(picture2)
                for x in range(0, tile_size):
                    for y in range (0, tile_size):
                        pass
                        #new_pixel_array[x, y] =



                pixel_array[currentStartX: currentStartX + tile_size, currentStartY: currentStartY + tile_size] = (new_red, new_green, new_blue)
                picture2 = new_pixel_array.make_surface()
                del new_pixel_array
                del pixel_array

                window.blit(picture2, (currentStartX, currentStartY))

                colour_count = 0
                red_total = 0
                green_total = 0
                blue_total = 0
                luminosity_total = 0

    #    pict = pxArray.make_surface()

    #    del pxArray

    #    window.blit(pict, (0, 0))

    #    for x in range (0, windowWidth):
     #       for x in range (0, window_height):



        pygame.display.update()

    #    pygame.time.wait(10000)

    #    dino = False


