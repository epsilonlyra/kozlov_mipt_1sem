
import math 
import pygame
from pygame.draw import *

YELLOW = (255, 255, 0)
OLIVEGREEN = (40, 40, 2)
TAN = (210, 180, 140) #  colour of upper windows
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 255, 255)
DARKRED = (50, 0, 0)
GREY = (128, 128, 128)
DARKGREY = (105, 105, 105)
LIGHTGREY = (220, 220,220)
DARKERGREY = (80, 80, 80)
DARKESTGREY = (40, 40 ,40) #  we still have 45 to go))

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 1000))

rect(screen, GREY, (0, 0, 800, 500)) # draw sky

circle(screen, WHITE, (700, 70), (60)) # draw moon

'''
  bacground clouds
'''

ellipse(screen, DARKESTGREY, (400, 250, 500, 70))
ellipse(screen, DARKGREY, (600, 125, 500, 70))
ellipse(screen, DARKGREY, (300, 30, 400, 90))

'''
  main part of the house   
'''

rect(screen, OLIVEGREEN, (50, 200, 400, 600))

# drawing windows
for i in range(2):
    rect(screen, DARKRED, (60 + 150 * i, 600, 50, 100))
rect(screen, YELLOW, (60 + 150 * (i + 1), 600, 50, 100))

for i in range(4):
    rect(screen, TAN, (60 + 100 *i, 200, 50, 250))

#  drawing balcony
rect(screen, DARKESTGREY, (30,450,450,30))
for i in range(0,10,1):
    rect(screen, DARKESTGREY, ((30 + (450 - 10) / 9 * i), 400, 10, 50))
rect(screen, DARKESTGREY, ((30 + (450 - 10) / 9), 380, (450 * 7 /  9 + 3) , 20))

#  drawiing roof
polygon(screen, BLACK, ((30, 200), (50, 180), (450, 180), (470, 200)))

#  drawing pipes
rect(screen, BLACK, (50, 160, 10, 20))
rect(screen, BLACK, (150, 140, 20, 40))
rect(screen, BLACK, (420, 100, 20, 80))


'''
  close cloud
'''
ellipse(screen, DARKERGREY, (0, 100, 400, 60))


'''
  ghost
'''

circle(screen,LIGHTGREY, (600,700), (30))

#  eyes
circle(screen, BLUE, (580, 700), (8))
circle(screen, BLACK,(580, 700), (3))
ellipse(screen, WHITE, (580, 700, 8, 1))

circle(screen, BLUE, (620, 700), (8))
circle(screen, BLACK,(620, 700), (3))
ellipse(screen, WHITE, (620, 700, 8, 1))


polygon(screen, LIGHTGREY, ((590, 695),(800, 900),(600, 900))) #body



























pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)






















    



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
