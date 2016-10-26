import pygame, sys, time, random,math
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Declare all variables etc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HEIGHT = 900
WIDTH = 900
a=1
b=452
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
picture = pygame.image.load("pic5.png")
picture_transformed = pygame.transform.scale(picture, (WIDTH,HEIGHT))
window.blit(picture_transformed,(0,0))

# Define functions 


def reduce_colours(color_change):
    if color_change > 175 and color_change < 255:
        color_change = 215
    return color_change


def distance(r_1, r_2, g_1, g_2, b_1, b_2):
    difference_red = math.pow(r_1 - r_2, 2)
    difference_green = math.pow(g_1 - g_2, 2)
    difference_blue = math.pow(b_1 - b_2, 2)
    likeness = math.sqrt(difference_blue + difference_green + difference_red)
    return likeness

while True:
    keys = pygame.key.get_pressed()
    px_array = pygame.PixelArray(window)
    clock = pygame.time.Clock()
    clock.tick(200)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
# Blurs When 'w' is pressed
    if keys[pygame.K_w]:
        a = -a
        for y in xrange(1,HEIGHT-1):
            for x in xrange(1,WIDTH-1):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red_1 = window.get_at((x+a, y+a)).r
                green_1 = window.get_at((x+a, y+a)).g
                blue_1 = window.get_at((x+a, y+a)).b
                red_final = (red+red_1)/2
                green_final = (green+green_1)/2
                blue_final = (blue+blue_1)/2
                px_array[x:x+1,y:y+1] = (red_final, green_final, blue_final)
                
# Inverts colours when 'q' is pressed
    if keys[pygame.K_q]:
        for y in xrange(1,HEIGHT-1):
            for x in xrange(1,WIDTH-1):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red_final = green
                blue_final = red
                green_final = blue
                px_array[x,y] = (red_final, green_final, blue_final)
                
# Night Vision when e is pressed
    if keys[pygame.K_e]:
        for y in xrange(1,HEIGHT-1):
            for x in xrange(1,WIDTH-1):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red_final = red*0.3
                green_final = reduce_colours(green)
                blue_final = green*0.3
                px_array[x,y] = (red_final, green_final, blue_final)
                
# Press r for vertical lines
    if keys[pygame.K_r]:
        for y in xrange(1,HEIGHT-1):
            for x in xrange(1,WIDTH-1):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red_1 = window.get_at((x, y+1)).r
                green_1 = window.get_at((x, y+1)).g
                blue_1 = window.get_at((x, y+1)).b
                likeness = distance(red, red_1, green, green_1, blue, blue_1)
                pygame.draw.rect(window, (red_1, green_1, blue_1), (x + 1 , y , 1 , likeness/10),)
                
# Press t for horizontal lines
    if keys[pygame.K_t]:
        for y in xrange(1, HEIGHT-1):
            for x in xrange(1, WIDTH-1):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red_1 = window.get_at((x + 1, y)).r
                green_1 = window.get_at((x + 1, y)).g
                blue_1 = window.get_at((x + 1, y)).b
                likeness = distance(red, red_1, green, green_1, blue, blue_1)
                pygame.draw.rect(window, (red_1, green_1, blue_1), (x + 1, y, likeness/3, 1), 1)#Uses the likeness value to determine the length of the rectangle
                
# Press y for circles
    b = (HEIGHT+4)/2
    if keys[pygame.K_y]:
        for y in range(0,HEIGHT/2):
            b -= 1
            x = WIDTH/2
            red = window.get_at((x, y)).r
            green = window.get_at((x, y)).g
            blue = window.get_at((x, y)).b
            pygame.draw.circle(window,(red, green, blue),(WIDTH/2,HEIGHT/2),b ,1)
    del px_array

# Blits original picture
    if keys[pygame.K_SPACE]:
        window.blit(picture_transformed, (0, 0))
    pygame.display.update()
