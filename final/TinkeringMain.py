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
HEIGHT = 400
WIDTH = 800
a=1

def reduce_colours(color_change):
    if color_change > 175 and color_change < 255:
        color_change = 215
    return color_change


def distance(red1, red2, green1, green2, blue1, blue2):
    diffred = math.pow(red1 - red2,2)
    diffgreen = math.pow(green1 - green2,2)
    diffblue = math.pow(blue1- blue2,2)
    likness = math.sqrt(diffblue +diffgreen +diffred)
    return likness

window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
Picture = pygame.image.load("cool_cat.jpg")
PictureTrans = pygame.transform.scale(Picture, (WIDTH,HEIGHT))
window.blit(PictureTrans,(0,0))
while True:
    keys = pygame.key.get_pressed()
    px_array = pygame.PixelArray(window)
    clock = pygame.time.Clock()
    clock.tick(200)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
#Blurs When 'w' is pressed.
    if keys[pygame.K_w]:
        a = -a
        for y in xrange(1,HEIGHT-1):
            for x in xrange(1,WIDTH-1):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red1 = window.get_at((x+a, y+a)).r
                green1 = window.get_at((x+a, y+a)).g
                blue1 = window.get_at((x+a, y+a)).b
                red_final = (red+red1)/2
                green_final = (green+green1)/2
                blue_final = (blue+blue1)/2
                px_array[x:x+1,y:y+1] = (red_final, green_final, blue_final)
#Inverts colours when 'q' is pressed.
    if keys[pygame.K_q]:
        for y in xrange(0,HEIGHT):
            for x in xrange(0,WIDTH):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red_final = green
                blue_final = red
                green_final = blue
                px_array[x,y] = (red_final, green_final, blue_final)
#Night Vision when e is pressed
    if keys[pygame.K_e]:
        for y in xrange(0,HEIGHT):
            for x in xrange(0,WIDTH):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red_final = red*0.3
                green_final = reduce_colours(green)
                blue_final = green*0.3
                px_array[x,y] = (red_final, green_final, blue_final)
# Press r for verticle lines
    if keys[pygame.K_r]:
        for y in xrange(0,HEIGHT):
            for x in xrange(0,WIDTH):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red1 = window.get_at((x+1, y)).r
                green1 = window.get_at((x+1, y)).g
                blue1 = window.get_at((x+1, y)).b
                likeness = distance(red, red1, green, green1, blue, blue1)
                pygame.draw.rect(window, (red1, green1, blue1), (x + 1 , y , 1 , likeness/2), 1)
# Press t for horizontal lines
    if keys[pygame.K_t]:
        for y in xrange(0, HEIGHT):
            for x in xrange(0, WIDTH):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red1 = window.get_at((x + 1, y)).r
                green1 = window.get_at((x + 1, y)).g
                blue1 = window.get_at((x + 1, y)).b
                likeness = distance(red, red1, green, green1, blue, blue1)
                pygame.draw.rect(window, (red1, green1, blue1), (x + 1, y, likeness/3, 1), 1)
    #if keys[pygame.K_t]:

    del px_array
#Blits original picture
    if keys[pygame.K_SPACE]:
        window.blit(PictureTrans, (0, 0))
    pygame.display.update()