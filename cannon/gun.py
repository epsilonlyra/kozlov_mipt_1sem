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
          
OBJECTS = []  # list of ingame objects



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
    y2 = y1 + length * sin

    x3 = x2 - width * sin
    y3 = y2 + width * cos

    x4 = x3 - length * cos
    y4 = y3 - length * sin
    
    pygame.draw.polygon(screen, color, ((x1, y1), (x2, y2),
                                        (x3, y3), (x4, y4)))


class Timer():

    def __init__(self):
        self.time = 0
    
    def ready(self, maxtime):
        if self.time >= maxtime:
            return(True)
        else:
            return(False)

    def tick(self):
        self.time += 1
    
    def restart(self):
        self.time = 0

   
class Sign():
    def __init__(self, screen):
        self.screen = screen
        self.maxtime = 200000
        self.x = 20
        self.y = 20
        self.is_seen = True
        self.timer2 = Timer()
        self.text = ''

    def show(self):
    
        """
        """
        if not self.timer2.ready(self.maxtime):
            img = font.render(self.text, True, BLACK)
            screen.blit(img, (self.x, self.y))
            self.timer2.tick()


class Score(Sign):

    def __init__(self, screen):
        super().__init__(screen)
        self.score = 0

    def change(self):
        self.text = 'score: ' + str(self.score)

    def show(self):
        Score.change(self)
        super().show()


class Health(Sign):
    def __init__(self, screen):
        global WIDTH
        super().__init__(screen)
        self.x = WIDTH - 100

    def change(self):
        self.text = 'Health: ' + str(player.live)

    def show(self):
        Health.change(self)
        super().show()
    

class Info(Sign):

    def __init__(self, screen):
        global WIDTH
        super().__init__(screen)
        self.x = round(WIDTH / 2)
        self.y = 100
        self.maxtime = 100
        self.d_targets = 0
        self.bullets = 0
        self.used_bullets = 0
        self.needupdate = False

    def change(self):
        if not self.timer2.ready(self.maxtime):
                self.text = ('You managed to destroy ' +
                             str(self.d_targets) +
                             ' target' + 's' * iszero(self.d_targets - 1) +
                             ' using ' + str(self.used_bullets) +
                             ' missile' +
                             's' * iszero(self.used_bullets - 1))

    def show(self):
        Info.change(self)
        super().show()


def calculateall():
    """
checks for collisions of target and missiles
get plus score, removes missile after hit
activates INFO
    """
    for obj1 in OBJECTS:
        if obj1.type == 'missile':
            for obj2 in OBJECTS:
                if obj2.type == 'target' and obj1.hittest(obj2):
                    obj1.live = 0
                    obj2.live -= 1
                    if obj2.live <= 0:
                        SCORE.score += obj2.worth
                        GEN.targets -= 1
                        INFO.d_targets += 1
                        INFO.used_bullets = INFO.bullets
                        if INFO.timer2.ready(INFO.maxtime):
                            INFO.timer2.restart()


class Targetgen:
    """
generates targets
    """
    def __init__(self):
        self.max = 0
        self.max_wait = 100
        self.timer1 = Timer()
        self.targets = 0

    def spawn(self):
        global OBJECTS, screen
        print(self.targets)
        if self.targets < self.max:
            self.timer1.tick()
            if (self.timer1.ready(self.max_wait)):
                target = Target(screen)
                OBJECTS.append(target)
                self.targets += 1
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
        self.r = rnd(10, 20)
        self.x = obj.x +  (obj.length +self.r) * math.cos(obj.an)
        self.y = obj.y +  (obj.length + self.r) * math.sin(obj.an)
        self.vx = obj.vx
        self.vy = obj.vy
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
        global WIDTH, HEIGHT
        self.live = 3
        self.type = 'target'
        self.screen = screen
        self.f2_power = 10  # min gun power
        self.f2_on = 0  # is gun loading
        self.an = 0  # angle in radians
        self.color = GREY 
        self.width = 10
        self.r = self. width
        self.length_base = 20
        self.length = 20
        self.x = rnd(self.r, WIDTH)
        self.y = rnd(self.r, HEIGHT)
        self.vx = 0
        self.vy = 0
        self.y = 450
        self.fire_speed = 20
        self.maxf2_power =  self.f2_power + 10
        self.timer3 = Timer()
        self.worth = 10
        
    def fire2_start(self):
        """
        start loading the gun that player clicks
        """
        if self.live > 0:
            if self.timer3.ready(self.fire_speed):
                self.f2_on = 1
                self.timer3.restart()

    def fire2_end(self, x_tar, y_tar):
        """
Then player frees button fires
        """
        if self.live > 0:
            if self.f2_on == 1:
                ball = Ball(self.screen, self)
                self.an = math.atan2((y_tar - ball.y),
                                     (x_tar - ball.x))  # angle in radians
                ball.vx += self.f2_power * math.cos(self.an)
                ball.vy += -1 *  self.f2_power * math.sin(self.an)
                OBJECTS.append(ball)
                self.f2_on = 0  # gun is now unload
                self.f2_power = 10  # min gunpower(start ball speed)

    def targetting(self, x_tar, y_tar):
        """
Orient gun by mouse  and change color
        """
        
        self.an = math.atan2((y_tar - self.y),
                                 (x_tar - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.circle(screen, GREY, (self.x, self.y), self.r)
        rectangleplus(screen, self.color, self.x, self.y,
                      self.width, self.length, self.an)
        print(self.length)
        self.timer3.tick()

    def power_up(self):
        """
If player holds button down
becames long and more powerfull(faster missiles)
        """
        if self.f2_on:
            if self.f2_power < self.maxf2_power:
                self.f2_power += 1
                self.length = self.length + 1
                self.color = RED
        else:
            self.color = GREY
            self.length = self.length_base


class PlayerTank(Gun):
    def __init__(self, screen):
        super().__init__(screen)
        self.type = 'target'
        self.speed = 10
        self.r = self.width
        self.W, self.A, self.S, self. D = False, False, False, False
        self.live = 10

    def fire2_end(self, x_tar, y_tar):
        if self.f2_on == 1:
            INFO.bullets += 1
        super().fire2_end(x_tar, y_tar)

    def start(self):
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
        
    def stop(self):
        if event.key == pygame.K_w:
            self.W = False
        if event.key == pygame.K_s:
            self.S = False
        if event.key == pygame.K_a:
            self.A = False
        if event.key == pygame.K_d:
            self.D = False

    def move(self):
        global HEIGHT, WIDTH
        if self.x >= WIDTH:
            self.x = 1
        if self.x <= 0:
            self.x = WIDTH
        
        if self.y >= HEIGHT:
            self.y = 1
        if self.y <= 0:
            self.y = HEIGHT
        PlayerTank.calcspeed(self)
        super().move()

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
HEALTH = Health(screen)
GEN = Targetgen()
ai = Gun(screen)
ai.fire_speed = 50
OBJECTS.append(ai)
player = PlayerTank(screen)
OBJECTS.append(player)

finished = False
while not finished:
    
    screen.fill(WHITE)
    for object in OBJECTS:
        object.destroy()
        object.draw()

    ai.fire2_start()
    ai.targetting(player.x, player.y)
    ai.fire2_end(player.x, player.y)
    HEALTH.show()
    SCORE.show()
    INFO.show()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            player.fire2_end(event.pos[0], event.pos[1])
        elif event.type == pygame.MOUSEMOTION:
            player.targetting(event.pos[0], event.pos[1])
        if event.type == pygame.KEYDOWN:
            player.start()
        if event.type == pygame.KEYUP:
            player.stop()
        
    calculateall()       
    player.power_up()
    ai.power_up()
    for object in OBJECTS:
        object.move()
    GEN.spawn()
pygame.quit()
