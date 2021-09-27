import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((500, 500))

rect(screen, (200, 200 , 200), (0, 0, 500, 500)) #setting gray bacground

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
