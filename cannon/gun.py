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


def iszero(x):
    if x == 0:
        return(0)
    else:
        return(1)


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


class Timer():

    def __init__(self):
        self.time = 0
    
    def ready(self,maxtime):
        self.time += 1
        if self.time >= maxtime:
            self.time = 0
            return(True)
        
        
class Sign():

     def __init__(self, screen):
        self.screen = screen
        self.timeactive = 0
        self.maxtime =  2000000
        self.x = 20
        self.y = 20
        self.is_seen = True
     def show(self):
    
        """
        """
        if self.is_seen:
            img = font.render(self.text, True, BLACK)
            screen.blit(img, (self.x, self.y))
            self.timeactive += 1
        if self.timeactive >= self.maxtime:
            self.is_seen = False
            self.timeactive = 0
            

    

class Score(Sign):
    global score
    def __init__(self, screen):
        super().__init__(screen)
        self.text = 'score: ' + str(score)


class Info(Sign):
    global bullets, used_bullets
    def __init__(self, screen):
        super().__init__(screen)
        self.x = round(WIDTH / 2)
        self.y = 100
        self.maxtime = 100
        self.is_seen = False
        self.d_targets = 1
        self.used_bullets = 0
        self.needupdate = False

    def change(self):
        global bullets, used_bullets
        if self.is_seen:
            self.text = ('You managed to destroy ' +
                     str(self.d_targets) +
                     ' target' + 's' * iszero(self.d_targets - 1) +
                     ' using ' + str(bullets) +
                     ' missile' + 's' * iszero(bullets - 1))
        else:
            self.d_targets = 1
            self.used_bullets = bullets - self.used_bullets
    def update(self):
        global bullets, used_bullets
        if self.needupdate:
            self.d_targets += 1
            self.used_bullets = bullets - used_bullets
            self.needupdate = False

            
OBJECTS = []  # list of missiles and targets
bullets = 0
used_bullets = 0
targets = 0  # count how many targets on screen
max_targets = 4
score = 0
# counter for  the number of frames since target generation
wait_target = 0
max_wait_target = 60  # if previous counter gets here new target generated



def calculateall():
    """
checks for collisions of target and missiles
get plus score, removes missile after hit
activates show_time

    """

    global targets, score, bullets, used_bullets
    for obj1 in OBJECTS:
        if obj1.type == 'missile':
            for obj2 in OBJECTS:
                if obj2.type == 'target' and obj1.hittest(obj2):
                    if targets >= 1:
                        targets -= 1
                    score += obj2.worth
                    obj1.live = 0
                    obj2.live -= 1
                    if INFO.is_seen:
                        INFO.needupdate = True
                    else:
                        INFO.is_seen = True
                        bullets = 1
    

timer1 = Timer()
class Targetgen:
    """
generates targets
    """
    def __init__(self):
        self.max = 4
        self.max_wait = 100

    def spawn(self):
        global targets, OBJECTS, screen
        if targets < self.max:
            if (timer1.ready(self.max_wait)):
                target = Target(screen)
                OBJECTS.append(target)
                targets += 1



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
        if self.live <= 0:
            OBJECTS.remove(object)


class Ball(Basecircle):

    def __init__(self, screen: pygame.Surface, x, y):
        """
        """
        self.type = 'missile'
        self.screen = screen
        # coordintes of the gun
        self.x = x
        self.y = y
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
            self.vy = - self.vy / 2
            # check if ball has low speed
            # and stop it on ground(kinda friction)
            # magical number, used to stop bouncing
            if self.vy <= 2 * -g_y:  
                self.vy = 0
                self.vx = 0
                self.live = self.live - 1
            self.y = HEIGHT - self.r

    def hittest(self, obj):
        """
Checks if missile collides with target(obj)
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2
                <= (self.r + obj.r) ** 2):
            return(True)
        else:
            return(False)


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
        self.isready = 0
        self.fire_speed = 10

    def fire2_start(self, event):
        """
        start loading the gun that player clicks
        """
        if self.isready >= self.fire_speed:
            self.f2_on = 1
            self.isready = 0

    def fire2_end(self, event):
        """
Then player frees button fires
        """
        global bullets
        if self.f2_on == 1:
            bullets += 1
            ball = Ball(self.screen, self.x, self.y)
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
            self.an = math.atan2((event.pos[1] - self.y),
                                 (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        rectangleplus(screen, self.color, self.x, self.y,
                      self.width, self.length, self.an)
        self.isready += 1

    def power_up(self):
        """
If player holds button down
becames long and more powerfull(faster missiles)
        """
        if self.f2_on:
            if self.f2_power < 1000:
                self.f2_power += 1
                self.length = self.length + 1
            self.color = RED
        else:
            self.color = GREY
            self.length = 20


class Tank(Gun):
    
    def __init__(self, screen):
        super().__init__(screen)
        self.speed = 10
        self.W, self.A, self.S, self.D = False, False, False, False
        self.r = self.width
    def draw(self):
        # gun and body
        rectangleplus(screen, self.color, self.x, self.y,  
                      self.width, self.length, self.an)
        pygame.draw.circle(screen, GREY, (self.x, self.y), self.r)
        self.isready += 1

    def start(self, event):
        if event.key == pygame.K_w:
            self.W = True
        if event.key == pygame.K_s:
            self.S = True
        if event.key == pygame.K_a:
            self.A = True
        if event.key == pygame.K_d:
            self.D = True

    def move(self):
        if self.W:
            self.y -= self.speed
        if self.S:
            self.y += self.speed
        if self.A:
            self.x -= self.speed
        if self.D:
            self.x += self.speed

    def stop(self, event):
        if event.key == pygame.K_w:
            self.W = False
        if event.key == pygame.K_s:
            self.S = False
        if event.key == pygame.K_a:
            self.A = False
        if event.key == pygame.K_d:
            self.D = False


class Target(Basecircle):

    def __init__(self, screen):

        self.type = 'target'
        self.screen = screen
        self.live = 1
        self.r = rnd(30, 50)
        self.color = RED
        self.worth = 1  # how many score for destroying

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

INFO = Info(screen)
SCORE = Score(screen)
GEN =Targetgen()
player = Tank(screen)
finished = False
while not finished:

    screen.fill(WHITE)
    player.draw()
    for object in OBJECTS:
        object.destroy()
        object.draw()

    
    SCORE.show()
    INFO.update()
    INFO.change()
    INFO.show()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            player.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            player.targetting(event)
        if event.type == pygame.KEYDOWN:
            player.start(event)
        if event.type == pygame.KEYUP:
            player.stop(event)
        
    for object in OBJECTS:
        object.move()

    calculateall()       
    player.power_up()
    player.move()
    GEN.spawn()


pygame.quit()
