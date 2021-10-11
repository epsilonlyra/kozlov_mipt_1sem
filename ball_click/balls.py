import pygame
from pygame.draw import *
import random
from random import randint

def sign(x):
  
  if (x>=0):
    return(1)
  else:
    return(-1)

pygame.init()

FPS = 30
width = 1200
height = 900
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont(None, 24)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Ball():
  
   
     
    def __init__(self):
        self.x = randint(100,700)
        self.y = randint(100,500)
        self.r = randint(30,50)
        self.color = COLORS[randint(0, 5)]
        self.speed = 5
        self.v_x = randint(-self.speed, self.speed)
        self.v_y = randint(-self.speed, self.speed)
        
    def create(self):
        circle(screen, self.color, (self.x, self.y), self.r)
    
    def move_x(self):
        self.x = self.x + self.v_x
    
    def move_y(self):
        self.y = self.y +  self.v_y

    def bounce_wall(self):
            
        if (self.x + self.v_x + self.r >= width) or (self.x  + self.v_x - self.r <= 0):
                k = randint(1,self.speed)
                self.v_x = -sign(self.v_x) * k
                self.v_y = randint(-min(self.speed, self.y + self.r),
                                   min(self.speed, height-self.r-self.y))
                
        if (self.y + self.r + self.v_y >= height) or (self.y - self.r + self.v_y <= 0):         
                k = randint(1,self.speed)
                self.v_y = -sign(self.v_y) * k
                self.v_x = randint(-min(self.speed, self.x + self.r),
                                   min(self.speed, width - self.r - self.x))

generation_rate = 2  # seconds per ball generation


pygame.display.update()
clock = pygame.time.Clock()
finished = False

TIME = 0
SCORE = 0
Points = bytes('Score:' + '0', encoding = 'utf-8')
Balls = []

while not finished:
      clock.tick(FPS)
      TIME = TIME + 1 / FPS
      for event in pygame.event.get():
              if event.type == pygame.QUIT:
                      finished = True
              elif event.type == pygame.MOUSEBUTTONDOWN:
                      Mouse_coordinates = (pygame.mouse.get_pos())  
                      for ball in Balls: 
                              if (Mouse_coordinates[0] - ball.x) **2 \
                               + (Mouse_coordinates[1] - ball.y) **2 \
                               <= (ball.r) **2:
                                      Balls.remove(ball)
                                      SCORE = SCORE + 1
                                      Points = bytes('Score:' + str(SCORE), encoding = 'utf-8')
      if int(TIME * FPS) % (FPS * generation_rate) == 0:
              Balls.append(Ball())
              
      for ball in Balls:
              ball.bounce_wall()
              
      for ball in Balls:
              ball.move_x()
              ball.move_y()
      
      for ball  in Balls:
              ball.create()
              
      img = font.render(Points, True, BLUE)
      screen.blit(img, (20, 20))
                                 

      
      pygame.display.update()
      screen.fill(BLACK)

pygame.quit()

