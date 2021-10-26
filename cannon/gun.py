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

#  screen param
WIDTH = 800
HEIGHT = 600

g_y = -1  # gravity


def rectangleplus(screen, color, x, y, width, length, alpha):
    """
    draws a turned rectangle  on screen
    x,y are coordinates of upper left corner
    alpha is angle counter-clockwise in radians
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


def showscore(score, screen):
    """
used to show score
    """
    SCORESIGN = bytes('score: ' + str(score), encoding='utf-8')
    img = font.render(SCORESIGN, True, BLACK)
    screen.blit(img, (20, 20))


OBJECTS = []  # list of missiles and targets
bullet = 0  # counts how many missiles were fired
targets = 0  # count how many targets on screen
max_targets = 2
score = 0
# counter for  the number of frames since target generation
wait_target = 0
max_wait_target = 60  # if previous counter gets here new target generated
# counter in frames how long gun is not active after hitting target
wait_gun = 0
max_wait_gun = 100  # if previous counter gets here gun activates
show_time = False  # is gun inactive and do we show BULLETSIGN


def showkill(screen):
    """
after player destroys a target  func.activates
for some time gun does not fire and BULLETSIGN is shown
    """

    global wait_gun, bullet, show_time
    if show_time:
        BULLETSIGN = bytes('You managed to destroy target  using ' +
                           str(bullet) + ' missiles', encoding='utf-8')
        img = font.render(BULLETSIGN, True, BLACK)
        screen.blit(img, (round(WIDTH / 2), 100))
        wait_gun += 1
    if wait_gun >= max_wait_gun:
        show_time = False
        wait_gun = 0
        bullet = 0


def calculateall():
    """
checks for collisions of target and missiles
get plus score, removes missile after hit
activates show_time

    """

    global targets, score, show_time
    for obj1 in OBJECTS:
        if obj1.type == 'missile':
            for obj2 in OBJECTS:
                if obj2.type == 'target' and obj1.hittest(obj2):
                    obj2.live = -1
                    targets -= 1
                    score += obj2.worth
                    OBJECTS.remove(obj1)
                    show_time = True


def targetgen():
    """
generates targets
    """
    global targets, wait_target
    if targets < max_targets:
        wait_target += 1
        if (wait_target >= max_wait_target):
            target = Target(screen)
            OBJECTS.append(target)
            targets += 1
            wait_target = 0


class Basecircle:
    """
Base class for Targets and Balls
    """

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (int(self.x), int(self.y)),
            int(self.r)
            )

    def destroy(self):
        if self.live < 0:
            OBJECTS.remove(object)

    
class Ball(Basecircle):

    def __init__(self, screen: pygame.Surface):
        """
        """
        self.type = 'missile'
        self.screen = screen
        # coordintes of the gun
        self.x = gun.x
        self.y = gun.y
        self.r = rnd(10, 20)
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 10  # how long ball lies on ground in frames

    def move(self):
        """
        """

        self.x += self.vx
        self.y -= self.vy
        self.vy += g_y  # grav
        # check for wall collisions
        if ((self.x + self.vx + self.r) >= WIDTH):
            self.vx = -self.vx
        if (self.y + self.r) >= HEIGHT:
            self.vy = - self.vy/2
            # check if ball has low speed and stop it on ground(kinda friction)
            if self.vy <= 2 * -g_y:  # magical number, used to stop bouncing
                self.vy = 0
                self.vx = 0
                self.live = self.live - 1
            self.y = HEIGHT - self.r

    def hittest(self, obj):
        """
Checks if ball collides with target(obj)
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2
                <= (self.r + obj.r) ** 2):
            return(True)
        else:
            return False


class Gun:

    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10  # min gun power
        self.f2_on = 0  # is gun loading
        self.an = 1  # angle in radians
        self.color = GREY 
        self.width = 10
        self.length = 10
        self.x = 20
        self.y = 450

    def fire2_start(self, event):
        """
        start loading the gun that player clicks
        """

        self.f2_on = 1

    def fire2_end(self, event):
        """
Then player frees button fires
        """
        global bullet
        bullet += 1
        ball = Ball(self.screen)
        self.an = math.atan2((event.pos[1]-ball.y),
                             (event.pos[0]-ball.x))  # angle in radians
        ball.vx = self.f2_power * math.cos(self.an)
        ball.vy = - self.f2_power * math.sin(self.an)
        OBJECTS.append(ball)
        self.f2_on = 0  # gun is now unload
        self.f2_power = 10  # min gunpower(start ball speed)

    def targetting(self, event):
        """
Orient gun by mouse  and change color
        """
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
        """
If player holds button down
becames longer anf more powerfull( faster missiles)
        """
        if self.f2_on:
            if self.f2_power < 20:
                self.f2_power += 1
                self.length = self.length + 1
            self.color = RED
        else:
            self.color = GREY
            self.length = 10


class Target(Basecircle):
    
    targets = 0
    
    def __init__(self, screen):

        self.type = 'target'
        self.screen = screen
        self.points = 10
        self.live = 1
        self.r = rnd(30, 50)
        self.color = RED
        self.worth = 1  # how many score for destroy

        self.x = rnd(self.r, WIDTH - self.r)
        self.vx = rnd(1, 10)
        self.y = rnd(self.r, HEIGHT - self.r)
        self.vy = rnd(1, 10)
      
    def move(self):
        """
        """
    
        self.x += self.vx
        self.y -= self.vy
        if (self.x + self.r) >= WIDTH:
            self.vx = -self.vx
            self.x = WIDTH - self.r
        if (self.x - self.r) <= 0:
            self.vx = -self.vx
            self.x = self.r
        if (self.y + self.r) >= HEIGHT:
            self.vy = -self.vy
            self.y = HEIGHT - self.r
        if (self.y - self.r) <= 0:
            self.vy = -self.vy
            self.y = self.r


pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

gun = Gun(screen)
finished = False
while not finished:

    screen.fill(WHITE)
    gun.draw()
    targetgen()
       
    for object in OBJECTS:
        object.destroy()
        object.draw()

    showscore(score, screen)
    showkill(screen)
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not show_time:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and not show_time:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for object in OBJECTS:
        object.move()

    calculateall()       
    gun.power_up()
    
 
pygame.quit()
