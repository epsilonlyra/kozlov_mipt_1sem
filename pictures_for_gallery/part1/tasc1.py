import math 
import pygame
from pygame.draw import *

pygame.init()

'''

creates a turned black rectangle, given the coordinates of down right corner,
(alpha is beetween -90 and 90 degrees)

'''

def rectangleplus(screen, x, y, width, length, alpha):
    cos = math.cos(alpha / 180 * math.pi)
    sin = math.sin(alpha / 180 * math.pi)

    x1 = x
    y1 = y
    
    x2 = x + length * cos
    y2 = y + length * sin
    
    x3 = x2 + width * sin
    y3 = y2 - width * cos

    x4 = x1 + width * sin
    y4 = y1 - width * cos
    
    polygon(screen, (0, 0, 0), ((x1, y1), (x2, y2), (x3, y3), (x4, y4)))


FPS = 30

screen = pygame.display.set_mode((500, 500))

rect(screen, (200, 200 , 200), (0, 0, 500, 500)) #  setting gray background

circle(screen, (200, 200, 0), (250, 250), 200) #  body

rect(screen, (0, 0, 0), (150, 350, 200, 20)) #  mouth

#  left eye
circle(screen, (255, 69, 0), (150,200), 50) 

circle(screen, (0, 0, 0), (150, 200), 20)

rectangleplus(screen, 40, 80, 20, 200, 30)

# right eye
circle(screen, (255, 69, 0), (350, 200), 30)

circle(screen, (0, 0, 0), (350, 200), 10)

rectangleplus(screen, 300, 200, 20, 150, -30)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
