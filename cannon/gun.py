import pygame
import math
from random import choice
from random import randint as rnd

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

g_y = -1  # gravity


def rectangleplus(screen, color, x, y, width, length, alpha):
    """
    draws a turned rectabhlr on screen
    x,y are coordinates of upper left corner
    alpha is angle clockwise in radians
    """
    cos = math.cos(alpha)
    sin = math.sin(alpha)

    x1 = x
    y1 = y
    x2 = x + length * cos
    y2 = y + length * sin
    x3 = x2 - width * sin
    y3 = y2 + width * cos
    x4 = x1 - width * sin
    y4 = y1 + width * cos
    pygame.draw.polygon(screen, color, ((x1, y1), (x2, y2),
                                        (x3, y3), (x4, y4)))
    




class Basecircle:
    
        
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (int(self.x), int(self.y)),
            int(self.r)
            )
    

    
class Ball(Basecircle):

    global BALLS
    def __init__(self, screen: pygame.Surface):
        """


        """
        self.screen = screen
        self.x = gun.x
        self.y = gun.y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 150 # how long ball lives in frames
        

    def move(self):
        """
        """
        
        self.x += self.vx
        self.y -= self.vy
        self.vy += g_y
        if ((self.x + self.vx + self.r) >= WIDTH):
            self.vx = -self.vx
        if (self.y  + self.r) >= HEIGHT:
            self.vy = - self.vy/2
            if self.vy <= 2:  # magical number, used to stop bouncing
                self.vy = 0
                self.vx = 0
                self.live = self.live - 1
            self.y = HEIGHT - self.r
        
    def destroy(self):
        if self.live <= 0:
            BALLS.remove(ball)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if ( self.x - obj.x) **  2 + (self.y -obj.y) ** 2 <= (self.r +obj.r) ** 2:
            return(True)
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10 # min gun power
        self.f2_on = 0  # is gun loading
        self.an = 1  # angle in radians
        self.color = GREY 
        self.width = 10
        self.length = 10
        self.x = 20
        self.y = 450

    def fire2_start(self, event):
        """
        start loading the gun
        """
        
        self.f2_on = 1


    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy
        зависят от положения мыши.
        """
        global BALLS, bullet
        bullet += 1
        ball = Ball(self.screen)
        ball.r += 20
        self.an = math.atan2((event.pos[1]-ball.y),
                             (event.pos[0]-ball.x))  # angle in radians
        ball.vx = self.f2_power * math.cos(self.an)
        ball.vy = - self.f2_power * math.sin(self.an)
        BALLS.append(ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-450), (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        rectangleplus(screen, self.color, self.x, self.y,
                      self.width, self.length, self.an)
        

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.length = self.length + 1
            self.color = RED
        else:
            self.color = GREY
            self.length = 10


class Target(Basecircle):
    
    global TARGETS

    def __init__(self, screen):
        
        self.screen = screen
        self.points = 10
        self.live = 1
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(30, 50)
        self.color = RED


    def create():
        target = Target(screen)
        TARGETS.append(target)

    def destroy(self):
        if self.live <= 0:
            TARGETS.remove(target)


pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

TARGETS=[]
BALLS= []
bullet = 0
gun = Gun(screen)

finished = False
Target.create()
while not finished:
    screen.fill(WHITE)
    gun.draw()
    for target in TARGETS:
        target.destroy()
        target.draw()
    for ball in BALLS:
        ball.destroy()
        ball.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for ball in BALLS:
        ball.move()
        if ball.hittest(target):
            target.live = 0
    gun.power_up()

pygame.quit()

