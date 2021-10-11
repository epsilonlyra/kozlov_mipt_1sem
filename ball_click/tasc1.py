import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 20
screen = pygame.display.set_mode((1200, 900))

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
		self.v_x = randint(-30, 30)
		self.v_y = randint(-30, 30)
		
	def create(self):
		circle(screen, self.color, (self.x, self.y), self.r)
	
	def radius(self):
		return(self.r)
		
	def x_position(self):
		return(self.x)
		
	def y_position(self):
		return(self.y)
		
	def v_x(self):
		return(self.v_x)
		
	def v_y(self):
		return(self.y)
	
	def move_x(self):
		self.x = self.x + self.v_x
	
	def move_y(self):
		self.y = self.y +  self.v_y

generation_rate =1

pygame.display.update()
clock = pygame.time.Clock()
finished = False

TIME = 0
Balls = []

while not finished:
	clock.tick(FPS)
	TIME= TIME+ FPS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			finished = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			Mouse_coordinates = (pygame.mouse.get_pos())  
			for item in Balls:
				if ((Mouse_coordinates[0] - item.x_position()) **2 + (Mouse_coordinates[1] - item.y_position())**2)<= (item.radius())**2:
					Balls.remove(item)
				
	if ((TIME % generation_rate) == 0):
		ball=Ball()
		Balls.append(ball)
	
	for item in Balls:
		item.move_x()
		item.move_y()
		
	for item in Balls:
		item.create()
		
	pygame.display.update()
	screen.fill(BLACK)

pygame.quit()

