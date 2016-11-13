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
TILE_SIZE = 20
TILE_SPACING = 5
ORIGIN = (0,0)

WIDTH = 900
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))

# Insert picture name to load below
picture = pygame.image.load('pic1.jpg')
picture = pygame.transform.scale(picture, (WIDTH, HEIGHT))

window.blit(picture, ORIGIN)
switch_comparison_direction = 1

# Define functions


def clamp(value):
    """Clamps a colour value to within 0 and 255"""
    if value > 255:
        clamped_value = 255
    elif value < 0:
        clamped_value = 0
    else:
        clamped_value = value
    return clamped_value


def cap_colours(color_change):
    """Changes colours if within a range"""
    if 100 < color_change < 255:          # caps colours within range, the 100, 255 combination gets a good result
        color_change = 215                # value it changes the rgb too
    return color_change


def distance((r_1, g_1, b_1, a_1), (r_2, g_2, b_2, a_2)):
    """uses pythagoras theorem to calculate numerical distance between the colors"""
    difference_red = math.pow(r_1 - r_2, 2)
    difference_green = math.pow(g_1 - g_2, 2)
    difference_blue = math.pow(b_1 - b_2, 2)
    likeness = math.sqrt(difference_red + difference_green + difference_blue)
    return likeness


def circle():
    """draws circles based on pixel colours"""
    for y in xrange(0, HEIGHT / 2):
        a = (HEIGHT/2)           # Uses The height to determine maximum radius
        radius = (a-y)
        x = WIDTH / 2
        colour_1 = window.get_at((x, y))
        pygame.draw.circle(window, colour_1, (WIDTH / 2, HEIGHT / 2), radius, 1)


def outline():
    """calculates and draws outline"""
    for x in xrange(1, WIDTH - 1):
        for y in xrange(1, HEIGHT - 1):
            colour_1 = window.get_at((x, y))
            colour_2 = window.get_at((x + 1, y))
            likeness = distance(colour_1, colour_2)
            if likeness > 150:
                px_array[x, y] = BLACK
            else:
                px_array[x, y] = WHITE


def water_fall():
    """draws vertical rectangles, the length of the rectangles and colour depend on their vertical neighbour."""
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            colour_1 = window.get_at((x, y))
            colour_2 = window.get_at((x, y + 1))
            likeness = distance(colour_1, colour_2)
            pygame.draw.rect(window, colour_2, (x + 1, y, 1, likeness / 10), )


def horizontal_lines():
    """draws horizontal lines, the size and colour of the lines depend on their horizontal neighbour."""
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            colour_1 = window.get_at((x, y))
            colour_2 = window.get_at((x + 1, y))
            likeness = distance(colour_1, colour_2)
            pygame.draw.rect(window, colour_2, (x + 1, y, likeness / 3, 1), 1)


def night_vision():
    """clamps the green colour and reduces the other colours to give a green tint"""
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            red_final = red*0.4
            green_final = cap_colours(green)
            blue_final = blue*0.4
            px_array[x, y] = (red_final, green_final, blue_final)


def color_invert():
    """swaps the colour value around"""
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            red_final = green                           # not necessary but added a final variable for clarity.
            blue_final = red
            green_final = blue
            px_array[x, y] = (red_final, green_final, blue_final)


def streaker_1():
    """passes an argument into function not possible from dictionary delegate"""
    streaker(switch_comparison_direction, px_array)


def blur_picture(a=1):
    """blurs picture along different axis on subsequent presses"""
    a *= -a                                             # used so that each time blur is called it will blur in the opposite direction
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            red_1 = window.get_at((x + a, y + a)).r
            green_1 = window.get_at((x + a, y + a)).g
            blue_1 = window.get_at((x + a, y + a)).b
            red_final = (red + red_1) / 2                # averages the value of the two red pixels
            green_final = (green + green_1) / 2
            blue_final = (blue + blue_1) / 2
            px_array[x:x + 1, y:y + 1] = (red_final, green_final, blue_final)


def streaker(switch_comparison_direction, px_array):
    """Runs once, does two passes, firstly determines an average value of the numerical distance
    of the colour values, secondly compares every value to the average and draws a tail fading to
    black. Abstract effect based off the colour strengths essentially"""
    TAIL_LENGTH = 200
    sum_of_squares_total = 0
    sum_of_squares_count = 0
    ignore_next_batch = False
    ignore_next_batch_count = 0

    print ('Reading source picture...')

    # First cycle
    # Get the rgb values of every pixel in picture
    for x in xrange(0, WIDTH - 1):
        for y in xrange(0, HEIGHT - 1):
            current_red = window.get_at((x, y)).r
            current_green = window.get_at((x, y)).g
            current_blue = window.get_at((x, y)).b
            current_alpha = window.get_at((x, y)).a

            # Calculate a strength comparison value for the pixel
            sum_of_squares = math.sqrt(math.pow(current_red, 2) +
                                       math.pow(current_green, 2) +
                                       math.pow(current_blue, 2))

            # Ignore pure white and black outliers
            if 10 < sum_of_squares < 430:       # these numbers represent the outlying values of white around the value of 0 and black around the value 441

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
    for x in xrange(0, WIDTH - 1):
        for y in xrange(0, HEIGHT - 1):

            # Had to put in a check to stop overdraw once a tail was drawn
            if ignore_next_batch:
                ignore_next_batch_count += 1
                px_array[x, y] = BLACK
                if ignore_next_batch_count == TAIL_LENGTH:
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

                # allows changing of the comparison parameters on successive executions
                sum_of_squares *= switch_comparison_direction
                sum_of_squares_average *= switch_comparison_direction

                # If pixel above or below the average, do something interesting
                if sum_of_squares > sum_of_squares_average:

                    # Create a tail fading to black from that pixel
                    for i in xrange(0, TAIL_LENGTH):
                        if x - i > 0:
                            new_red = current_red - (current_red * i / TAIL_LENGTH)
                            new_green = current_green - (current_green * i / TAIL_LENGTH)
                            new_blue = current_blue - (current_blue * i / TAIL_LENGTH)

                            px_array[x - i, y] = (new_red, new_green, new_blue)
                            ignore_next_batch = True

                else:
                    # Completes the effect of tail fading to black, by setting all else to black,
                    px_array[x, y] = BLACK

    print ('Done, press space then i again if it is mostly black.')
    # reverses the comparison direction for a better result on some images
    switch_comparison_direction *= -1


def simplify_colour():
    """rounds the colour values to preset increments"""

    # The step in the colour range which each colour value will be rounded to
    SIMPLIFY_STRENGTH = 255 / 3

    for x in xrange(0, WIDTH - 1):
        for y in xrange(0, HEIGHT - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b

            # Essentially this divides by a number, truncates the decimal portion then multiplies it back to scale
            # for instance were the strength = 100, a value of 234 would go to 2.34 to 2 then return 200
            new_red = clamp(SIMPLIFY_STRENGTH * int(red / SIMPLIFY_STRENGTH) + (SIMPLIFY_STRENGTH / 2))
            new_green = clamp(SIMPLIFY_STRENGTH * int(green / SIMPLIFY_STRENGTH) + (SIMPLIFY_STRENGTH / 2))
            new_blue = clamp(SIMPLIFY_STRENGTH * int(blue / SIMPLIFY_STRENGTH) + (SIMPLIFY_STRENGTH / 2))

            px_array[x, y] = (new_red, new_green, new_blue)


def pixelise():
    """swaps ranges of pixels for the average colour of that range, allows smaller tiles than the range to
    give an effect where the tiles are spaced apart"""
    for current_start_x in xrange(0, WIDTH, TILE_SIZE):
        for current_start_y in xrange(0, HEIGHT, TILE_SIZE):

            red_total = 0
            green_total = 0
            blue_total = 0
            colour_count = 0

            for x in xrange(current_start_x, current_start_x + TILE_SIZE - 1):
                for y in xrange(current_start_y, current_start_y + TILE_SIZE - 1):
                    current_red = window.get_at((x, y)).r
                    current_green = window.get_at((x, y)).g
                    current_blue = window.get_at((x, y)).b

                    red_total += current_red
                    green_total += current_green
                    blue_total += current_blue
                    colour_count += 1

            # Have to swap red and blue here sometimes... No idea why. Maybe png and jpg render bgr not rgb
            new_red = red_total / colour_count
            new_green = green_total / colour_count
            new_blue = blue_total / colour_count

            px_array[current_start_x: current_start_x + TILE_SIZE - TILE_SPACING,
                        current_start_y: current_start_y + TILE_SIZE - TILE_SPACING] = (new_red, new_green, new_blue)


# creates dictionary for controls.
controls = {'q': (circle, "circle"),
            'w': (blur_picture, "blur picture"),
            'e': (night_vision,"night vision"),
            'r': (color_invert, "colour invert"),
            't': (outline, "outline"),
            'y': (water_fall, "waterfall"),
            'u': (horizontal_lines, "horizontal lines"),
            'i': (streaker_1, "streaker"),
            'o': (simplify_colour, "simplify colour"),
            'p': (pixelise, "pixelise")}


def print_controls():
    """prints controls directly from dictionary tuple and associated key"""
    for letters in controls:
        print letters + " : " + controls[letters][1]
    print "space : reset"

print_controls()


while True:
    keys = pygame.key.get_pressed()
    px_array = pygame.PixelArray(window)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Handles controls by referring to a dictionary.
    if event.type == pygame.KEYDOWN:
        which_key = pygame.key.name(event.key)              # gives back the key pressed as a string
        if which_key in controls:
                command = controls[which_key][0]            # assigns function pointer dependent on key to command
                command()                                   # actually executes the function refered to in the dict
        elif which_key != 'space':                          # an exception so space isn't printed as not in use
            print ""
            print('key ' + which_key + ' not in use')

    # Blits original picture
    if keys[pygame.K_SPACE]:
        del px_array
        window.blit(picture, ORIGIN)
        print_controls()
    pygame.display.update()