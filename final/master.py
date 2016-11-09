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

WIDTH = 900
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))

# Insert picture name to load below
picture = pygame.image.load('pic7.jpg')
picture = pygame.transform.scale(picture, (WIDTH, HEIGHT))

window.blit(picture, (0, 0))
switch_comparison_direction = 1
run_once = True


# Define functions



# Stops the error when a colour value is greater than 255 or less than 0
def clamp(value):
    if value > 255:
        clamped_value = 255
    elif value < 0:
        clamped_value = 0
    else:
        clamped_value = value
    return clamped_value


# changes colours if within the a certain range.
def cap_colours(color_change):
    if 100 < color_change < 255:
        color_change = 215
    return color_change


# uses pythagoras to calculate distance between the colors 
def distance(r_1, g_1, b_1, r_2, g_2, b_2):
    difference_red = math.pow(r_1 - r_2, 2)
    difference_green = math.pow(g_1 - g_2, 2)
    difference_blue = math.pow(b_1 - b_2, 2)
    likeness = math.sqrt(difference_red + difference_green + difference_blue)
    return likeness


def circle():
    for y in range(0, HEIGHT / 2):
        a = (HEIGHT/2)           # Uses The height to determine maximum radius
        radius = (a-y)
        x = WIDTH / 2
        red = window.get_at((x, y)).r
        green = window.get_at((x, y)).g
        blue = window.get_at((x, y)).b
        pygame.draw.circle(window, (red, green, blue), (WIDTH / 2, HEIGHT / 2), radius, 1)


def outline():
    for x in xrange(1, WIDTH - 1):
        for y in xrange(1, HEIGHT - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            red_1 = window.get_at((x + 1, y)).r
            green_1 = window.get_at((x + 1, y)).g
            blue_1 = window.get_at((x + 1, y)).b
            likeness = distance(red, red_1, green, green_1, blue, blue_1)
            if likeness > 150:
                px_array[x, y] = BLACK
            else:
                px_array[x, y] = WHITE


# draws vertical rectangles, the length of the rectangles and colour depend on their vertical neighbour.
def water_fall():
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            red_1 = window.get_at((x, y + 1)).r
            green_1 = window.get_at((x, y + 1)).g
            blue_1 = window.get_at((x, y + 1)).b
            likeness = distance(red, green, blue, red_1, green_1, blue_1,)
            pygame.draw.rect(window, (red_1, green_1, blue_1), (x + 1, y, 1, likeness / 10), )


# draws horizontal lines, the size and colour of the lines depend on their horzontal neighbour.
def horizontal_lines():
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            red_1 = window.get_at((x + 1, y)).r
            green_1 = window.get_at((x + 1, y)).g
            blue_1 = window.get_at((x + 1, y)).b
            likeness = distance(red, green, blue, red_1, green_1, blue_1,)
            pygame.draw.rect(window, (red_1, green_1, blue_1), (x + 1, y, likeness / 3, 1), 1)


# caps the green colour and reduces the other colours to give a green tint.
def night_vision():
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            red_final = red*0.4
            green_final = cap_colours(green)
            blue_final = blue*0.4
            px_array[x, y] = (red_final, green_final, blue_final)


# simply swaps the colour value around.
def color_invert():
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            red_final = green   # not necessary but added a final variable for clarity.
            blue_final = red
            green_final = blue
            px_array[x, y] = (red_final, green_final, blue_final)


def blur_picture_1():
    a = 1
    blur_picture(a)


def blur_picture(a):
    a *= -a                    # used so that each time blur is called it will blur in the opposite direction
    for y in xrange(1, HEIGHT - 1):
        for x in xrange(1, WIDTH - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            red_1 = window.get_at((x + a, y + a)).r
            green_1 = window.get_at((x + a, y + a)).g
            blue_1 = window.get_at((x + a, y + a)).b
            red_final = (red + red_1) / 2           # averages the value of the two red pixels
            green_final = (green + green_1) / 2
            blue_final = (blue + blue_1) / 2
            px_array[x:x + 1, y:y + 1] = (red_final, green_final, blue_final)


def streaker():
    global run_once
    global switch_comparison_direction
    global px_array
    tail_length = 200
    sum_of_squares_total = 0
    sum_of_squares_count = 0
    ignore_next_batch = False
    ignore_next_batch_count = 0
    if run_once:
        run_once = False
        print ('Reading source picture...')

        # Porting variable names to master .py file
        pixel_array = px_array

        # First cycle
        # Get the rgb values of every pixel in picture
        for x in range(0, WIDTH - 1):
            for y in range(0, HEIGHT - 1):
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
        for x in range(0, WIDTH - 1):
            for y in range(0, HEIGHT - 1):

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

                    # allows changing of the comparison parameters on successive executions
                    sum_of_squares *= switch_comparison_direction
                    sum_of_squares_average *= switch_comparison_direction

                    # If pixel above or below the average, do something interesting
                    if sum_of_squares > sum_of_squares_average:

                        # Create a tail fading to black from that pixel
                        for i in range (0, tail_length):
                            if x - i > 0:
                                new_red =  current_red - (current_red * i / tail_length)
                                new_green = current_green - (current_green * i / tail_length)
                                new_blue = current_blue - (current_blue * i / tail_length)

                                pixel_array[x - i, y] = (new_red, new_green, new_blue)
                                ignore_next_batch = True

                    else:
                        # Completes the effect of tail fading to black, by setting all else to black,
                        pixel_array[x, y] = BLACK

        # Draw new picture from altered pixel_array
        pict = pixel_array.make_surface()
        del pixel_array
        del px_array

        window.blit(pict, (0, 0))
        pygame.display.update()

        print ('Done, press space then i again if it is mostly black.')
        switch_comparison_direction *= -1

    else:
        print ('It really will turn black if you run it again.')
        print ('press space to reset.')


def simplify_colour():
    px_array = pygame.PixelArray(window)

    # The step in the colour range which each colour value will be rounded to
    simplify_strength = 255 / 3

    for x in range(0, WIDTH - 1):
        for y in range(0, HEIGHT - 1):
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b

            # Essentially this divides by a number, truncates the decimal portion then multiplies it back to scale
            # for instance were the strength = 100, a value of 234 would go to 2.34 to 2 then return 200
            new_red = clamp(simplify_strength * int(red / simplify_strength) + (simplify_strength / 2))
            new_green = clamp(simplify_strength * int(green / simplify_strength) + (simplify_strength / 2))
            new_blue = clamp(simplify_strength * int(blue / simplify_strength) + (simplify_strength / 2))

            px_array[x, y] = (new_red, new_green, new_blue)


def pixelise():

    tile_size = 20
    tile_spacing = 5
    global px_array
    pixel_array = pygame.PixelArray(window)

    for currentStartX in range(0, WIDTH, tile_size):
        for currentStartY in range(0, HEIGHT, tile_size):

            red_total = 0
            green_total = 0
            blue_total = 0
            colour_count = 0

            for x in range(currentStartX, currentStartX + tile_size - 1):
                for y in range(currentStartY, currentStartY + tile_size - 1):
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

            pixel_array[currentStartX: currentStartX + tile_size - tile_spacing,
                currentStartY: currentStartY + tile_size - tile_spacing] = (new_red, new_green, new_blue)

    pict = pixel_array.make_surface()
    del pixel_array
    del px_array

    window.blit(pict, (0, 0))
    pygame.display.update()


def good_combo():
    pixelise()
    simplify_colour()

controls = {'q': circle,
            'w': blur_picture_1,
            'e': night_vision,
            'r': color_invert,
            't': outline,
            'y': water_fall,
            'u': horizontal_lines,
            'i': streaker,
            'o': simplify_colour,
            'p': pixelise,
            'a': good_combo}


def print_controls():
    print ('Controls:')
    print ('Q - Invert colours')
    print ('W - Blur')
    print ('E - Night vision')
    print ('R - Waterfall')
    print ('T - Horizontal lines, length is similarity strength')
    print ('Y - Circles')
    print ('U - Outline')
    print ('I - Horizontal lines, fading, chosen by strength')
    print ('O - Simplify colours')
    print ('P - Pixelise, with tile effect')
    print ('L - P then O combo. Works well.')
    print ('Space - Reset')

print_controls()


while True:
    keys = pygame.key.get_pressed()
    px_array = pygame.PixelArray(window)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if event.type == pygame.KEYDOWN:
        which_key = pygame.key.name(event.key)
        if which_key in controls:
                command = controls[which_key]
                command()
        elif which_key != 'space':
            print('key ' + which_key + ' not in use')

    # Blits original picture
    if keys[pygame.K_SPACE]:
        del px_array
        window.blit(picture, (0, 0))
        run_once = True

    pygame.display.update()
