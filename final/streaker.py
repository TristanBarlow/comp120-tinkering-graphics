import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Declare all variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

window_width = 600
window_height = 400

tail_length = 200
sum_of_squares_total = 0
sum_of_squares_count = 0
ignore_next_batch = False
ignore_next_batch_count = 0

window = pygame.display.set_mode((window_width, window_height))

# Insert picture name to load below
picture = pygame.image.load('pic2.jpg')
picture = pygame.transform.scale(picture, (window_width, window_height))

window.blit(picture, (0, 0))
run_once = True


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if run_once:
        run_once = False

        print ('Reading source picture...')

        pixel_array = pygame.PixelArray(picture)

        # Create a new empty list to write to
        new_pixel_array = pygame.PixelArray(pygame.Surface((window_width, window_height)))

        # First cycle
        # Get the rgb values of every pixel in picture
        for x in range(0, window_width - 1):
            for y in range(0, window_height - 1):
                current_red = window.get_at((x, y)).r
                current_green = window.get_at((x, y)).g
                current_blue = window.get_at((x, y)).b
                current_alpha = window.get_at((x, y)).a

                # Calculate a strength comparison value for the pixel
                sum_of_squares = math.sqrt(math.pow(current_red, 2) +
                                       math.pow(current_green, 2) +
                                       math.pow(current_blue, 2))

                # Ignore pure white and black outliers
                if 10 < sum_of_squares < 440:

                    # Keep a running total and count number to calculate average, ignoring outliers
                    sum_of_squares_total += sum_of_squares
                    sum_of_squares_count += 1

        sum_of_squares_average = sum_of_squares_total / sum_of_squares_count

        # First cycle checkpoint... This can take a while to get to
        print ('Average sum_of_squares:')
        print sum_of_squares_average
        print ('Over this many pixels:')
        print sum_of_squares_count
        print ('Calculating "art".')
        print ('This may take a while...')

        # Second cycle
        # Looks at every pixel in picture and compares it's strength value to the average calculated in first cycle
        for x in range(0, window_width - 1):
            for y in range(0, window_height - 1):

                # Had to put in a check to stop overdraw once a tail was drawn
                if ignore_next_batch:
                    ignore_next_batch_count += 1
                    pixel_array[x, y] = BLACK
                    if ignore_next_batch_count == tail_length:
                        ignore_next_batch = False
                        ignore_next_batch_count = 0
                else:

                    # Check current pixel to compare against average obtained from first cycle
                    current_red = window.get_at((x, y)).r
                    current_green = window.get_at((x, y)).g
                    current_blue = window.get_at((x, y)).b

                    sum_of_squares = math.sqrt(math.pow(current_red, 2) +
                                           math.pow(current_green, 2) +
                                           math.pow(current_blue, 2))

                    # If pixel above or below the average, do something interesting
                    if sum_of_squares < sum_of_squares_average:

                        # Create a tail fading to black from that pixel
                        for i in range (0, tail_length):
                            if x - i > 0:
                                new_red =  current_red - (current_red * i / tail_length)
                                new_green = current_green - (current_green * i / tail_length)
                                new_blue = current_blue - (current_blue * i / tail_length)

                                pixel_array[x - i, y] = (new_blue, new_green, new_red)
                                ignore_next_batch = True

                    else:
                        # Completes the effect of tail fading to black, by setting all else to black,
                        pixel_array[x, y] = BLACK


        # Draw new picture from altered pixel_array
        pict = pixel_array.make_surface()
        del pixel_array

        window.blit(pict, (0, 0))
        pygame.display.update()

        print ('Done, sorry if it is black.')

    clock = pygame.time.Clock()
    clock.tick(15)



