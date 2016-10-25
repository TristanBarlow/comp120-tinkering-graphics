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
HEIGHT1 = 399
WIDTH1 = 799
def Same(Changecolor):
    if Changecolor > 175 and Changecolor < 255:
        Changecolor = 215
    return Changecolor
def distance(Red1, Red2, Green1, Green2, Blue1, Blue2):
    DiffRed = math.pow(Red1 - Red2,2)
    DiffGreen = math.pow(Green1 - Green2,2)
    DiffBlue = math.pow(Blue1- Blue2,2)
    likness = math.sqrt(DiffBlue +DiffGreen +DiffRed)
    return likness
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
Picture = pygame.image.load("cool_cat.jpg")
PictureTrans = pygame.transform.scale(Picture, (WIDTH,HEIGHT))
window.blit(PictureTrans,(0,0))
while True:
    keys = pygame.key.get_pressed()
    pxarray = pygame.PixelArray(window)
    clock = pygame.time.Clock()
    clock.tick(200)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
#Blurs When 'w' is pressed.
    if keys[pygame.K_w]:
        for y in xrange(0,HEIGHT1):
            for x in xrange(0,WIDTH1):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red1 = window.get_at((x+1, y+1)).r
                green1 = window.get_at((x+1, y+1)).g
                blue1 = window.get_at((x+1, y+1)).b
                RedF = (red+red1)/2
                GreenF = (green+green1)/2
                blue_final = (blue+blue1)/2
                pxarray[x:x+2,y:y+2] = (RedF, GreenF, blue_final)
#Inverts colours when 'q' is pressed.
    if keys[pygame.K_q]:
        for y in xrange(0,HEIGHT1):
            for x in xrange(0,WIDTH1):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                RedF = green
                blue_final = red
                GreenF = blue
                pxarray[x,y] = (RedF, GreenF, blue_final)
#Night Vision when e is pressed
    if keys[pygame.K_e]:
        for y in xrange(0,HEIGHT1):
            for x in xrange(0,WIDTH1):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                RedF = red*0.3
                GreenF = Same(green)
                blue_final = green*0.3
                pxarray[x,y] = (RedF, GreenF, blue_final)
#work in progress blurs back ground
    if keys[pygame.K_r]:
        for y in xrange(0,HEIGHT1,2):
            for x in xrange(0,WIDTH1,2):
                red = window.get_at((x, y)).r
                green = window.get_at((x, y)).g
                blue = window.get_at((x, y)).b
                red1 = window.get_at((x+1, y+1)).r
                green1 = window.get_at((x+1, y+1)).g
                blue1 = window.get_at((x+1, y+1)).b
                likeness = distance(red, red1, green, green1, blue, blue1)
                if likeness < 5:
                    RedF = (red+red1)/2
                    GreenF = (green+green1)/2
                    blue_final = (blue+blue1)/2
                    pxarray[x:x+1,y:y+1] = (RedF, GreenF, blue_final)
    del pxarray
#Blits original picture
    if keys[pygame.K_SPACE]:
        window.blit(PictureTrans, (0, 0))
    pygame.display.update()