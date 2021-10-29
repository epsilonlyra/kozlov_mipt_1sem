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

g_y = -1 # gravity
          
OBJECTS = []  # list of missiles and targets
bullets = 0
used_bullets = 0
targets = 0  # count how many targets on screen
score = 0


def iszero(x):
    if x == 0:
        return(0)
    else:
        return(1)


def rectangleplus(screen, color, x, y, width, length, alpha):
    """
    draws a turned rectangle  on screen
    x,y are coordinates of  left center
    alpha is angle clockwise in radians
    """
    cos = math.cos(alpha)
    sin = math.sin(alpha)
    x1 = x + width / 2 * sin
    y1 = y - width / 2 * cos

    x2 = x1 + length * cos
    y2 = y1 +  length * sin

    x3 = x2 -  width * sin
    y3 = y2 + width * cos

    x4 = x3 - length * cos
    y4 = y3 - length * sin
    
    pygame.draw.polygon(screen, color, ((x1, y1), (x2, y2),
                                        (x3, y3), (x4, y4)))


class Timer():

    def __init__(self):
        self.time = 0
    
    def ready(self, maxtime):
        self.time += 1
        if self.time >= maxtime:
            return(True)
        else:
            return(False)

    def restart(self):
        self.time = 0

   
class Sign():
    def __init__(self, screen):
        self.screen = screen
        self.maxtime =  2000000
        self.x = 20
        self.y = 20
        self.is_seen = True
        self.timer2 = Timer()
        self.text = ''


    def show(self):
    
        """
        """
        if  not self.timer2.ready(self.maxtime):
            img = font.render(self.text, True, BLACK)
            screen.blit(img, (self.x, self.y))


class Score(Sign):
    global score
    def __init__(self, screen):
        super().__init__(screen)

    def change(self):
        self.text = 'score: ' + str(score)
    


class Info(Sign):
    global bullets, used_bullets
    def __init__(self, screen):
        super().__init__(screen)
        self.x = round(WIDTH / 2)
        self.y = 100
        self.maxtime = 100
        self.d_targets = 0
        self.used_bullets = 0
        self.needupdate = False

    def change(self):
        global bullets, used_bullets
        if  not self.timer2.ready(self.maxtime):
            self.text = ('You managed to destroy ' +
                     str(self.d_targets) +
                     ' target' + 's' * iszero(self.d_targets - 1) +
                     ' using ' + str(self.used_bullets) +
                     ' missile' + 's' * iszero(self.used_bullets - 1))

    '''def update(self):
        global bullets, used_bullets
        if self.needupdate:
            self.d_targets += 1
            self.needupdate = False
            self.wasupdated = True'''



def calculateall():
    """
checks for collisions of target and missiles
get plus score, removes missile after hit
activates show_time

    """

    global targets, score, bullets
    for obj1 in OBJECTS:
        if obj1.type == 'missile':
            for obj2 in OBJECTS:
                if obj2.type == 'target' and obj1.hittest(obj2):
                    if targets >= 1:
                        targets -= 1
                    score += obj2.worth
                    obj1.live = 0
                    obj2.live -= 1
                    INFO.d_targets += 1
                    INFO.used_bullets = bullets
                    if   INFO.timer2.ready(INFO.maxtime):
                        INFO.timer2.restart()


class Targetgen:
    """
generates targets
    """
    def __init__(self):
        self.max = 4
        self.max_wait = 100
        self.timer1 = Timer()

    def spawn(self):
        global targets, OBJECTS, screen
        if targets < self.max:
            if (self.timer1.ready(self.max_wait)):
                target = Target(screen)
                OBJECTS.append(target)
                targets += 1
                self.timer1.restart()



class Basecircle:
    """
Base class for everything
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

    def move(self):
        self.x += self.vx
        self.y -= self.vy


class Ball(Basecircle):

    def __init__(self, screen: pygame.Surface, obj):
        """
        """
        self.type = 'missile'
        self.screen = screen
        # coordintes of the gun
        self.x = obj.x
        self.y = obj.y
        self.r = rnd(10, 20)
        self.vx = obj.vx
        self.vy =  - obj.vy
        self.color = choice(GAME_COLORS)
        self.live = 10  

    def move(self):
        """
        """
        super().move()
        self.vy += g_y  # grav
        # check for wall collisions
        if ((self.x + self.vx + self.r) >= WIDTH):
            self.vx = -self.vx
        if (self.y + self.r) >= HEIGHT:
            self.vy = - self.vy / 2
            # check if ball has low speed
            # and stop it on ground (kinda friction)
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


class Gun(Basecircle):
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10  # min gun power
        self.f2_on = 0  # is gun loading
        self.an = 0  # angle in radians
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
        if self.f2_on == 1:
            ball = Ball(self.screen, self)
            self.an = math.atan2((event.pos[1]-ball.y),
                                 (event.pos[0]-ball.x))  # angle in radians
            ball.vx += self.f2_power * math.cos(self.an)
            ball.vy += -  self.f2_power * math.sin(self.an)
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
            if self.f2_power < 20:
                self.f2_power += 1
                self.length = self.length + 1
            self.color = RED
        else:
            self.color = GREY
            self.length = 20


class PlayerTank(Gun):
    global bullets 
    def __init__(self, screen):
        super().__init__(screen)
        self.speed = 10
        self.vx = 0
        self.vy = 0
        self.r = self.width
        self.W, self.A, self.S, self. D = False, False, False, False

    def fire2_end(self, event):
        global bullets
        if self.f2_on ==1:
            bullets += 1
        super().fire2_end(event)

    def draw(self):
        # gun and body
        super().draw()
        pygame.draw.circle(screen, GREY, (self.x, self.y), self.r)

    
    def start(self, event):
        if event.key == pygame.K_w:
            self.W = True
        if event.key == pygame.K_s:
            self.S = True
        if event.key == pygame.K_a:
            self.A = True
        if event.key == pygame.K_d:
            self.D = True

    def calcspeed(self):
        if self.W and not self.S:
            self.vy = self.speed
        elif self.S and not self.W:
            self.vy = -self.speed
        else:
            self.vy  = 0

        if self.A and not self.D:
            self.vx = -self.speed
        elif self.D  and not self.A:
            self.vx = self.speed
        else:
            self.vx  = 0
        
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
    
        super().move()
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
INFO.timer2.time = INFO.maxtime
SCORE = Score(screen)
GEN =Targetgen()
player = PlayerTank(screen)

finished = False
while not finished:
    
    screen.fill(WHITE)
    player.draw()
    for object in OBJECTS:
        object.destroy()
        object.draw()

    SCORE.change()
    SCORE.show()
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
    player.calcspeed()
    player.move()
    GEN.spawn()


pygame.quit()
