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

#  screen param(pixels)
WIDTH = 800
HEIGHT = 600
          
OBJECTS = []  # list of ingame objects(missiles, player, enemygun, target)



def iszero(x):
    """
    if x = 0 return 0, else return 1
    """
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
    """
    used for measuring ingame time intervals (in frames)
    """

    def __init__(self):
        self.time = 0  # frames since timer start
    
    def ready(self, maxtime):
        """
        if time more or equal to maxtime return True(enough time has passed)
        else return False
        """
        if self.time >= maxtime:
            return(True)
        else:
            return(False)

    def tick(self):
        self.time += 1
    
    def restart(self):
        self.time = 0

   
class Sign():
    """
    used for blitting text on screen
    """
    def __init__(self, screen):
        self.screen = screen
        self.maxtime = 200000  
        # coordiates of upper left
        self.x = 20
        self.y = 20
        self.timer2 = Timer()
        self.text = ''  # str

    def show(self):
    
        """
        if timer is not ready blit text on screen
        """
        if not self.timer2.ready(self.maxtime):
            img = font.render(self.text, True, BLACK)
            screen.blit(img, (self.x, self.y))
            self.timer2.tick() #  add  1 to time


class Score(Sign):
    """
    for showing player score
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.score = 0

    def change(self):
        """
        getting current score
        """
        self.text = 'score: ' + str(self.score)  

    def show(self):
        Score.change(self)
        super().show()


class Health(Sign):
    """
    for showing player health
    """
    def __init__(self, screen):
        global WIDTH
        super().__init__(screen)
        self.x = WIDTH - 100  # just for indent

    def change(self):
        self.text = 'Health: ' + str(player.live)

    def show(self):
        Health.change(self)
        super().show()
    

class Info(Sign):
    """
    for showing info destroyed enemies including enemygun and used_bullets
    then you destroy enemy activates and is actve for maxtime 
    """

    def __init__(self, screen):
        global WIDTH
        super().__init__(screen)
        self.x = round(WIDTH / 2) - 20  # just for indent
        self.y = 100
        self.maxtime = 100  # time visible
        self.d_enemies = 0  # destroyed enemies
        self.bullets = 0  # all used bullets
        self.used_bullets = 0  # equal to previous if target was killed

    def change(self):
        if not self.timer2.ready(self.maxtime):
                self.text = ('You managed to destroy ' +
                             str(self.d_enemies) +
                             ' foe' +
                             's' * iszero(self.d_enemies - 1) +
                             ' using ' + str(self.used_bullets) +
                             ' missile' +
                             's' * iszero(self.used_bullets - 1))

    def show(self):
        Info.change(self)
        super().show()


def calculateall():
    """
    checks for collisions of target and missiles
    get plus score, get minus health for objects
    activates INFO
    """
    for obj1 in OBJECTS:
        if obj1.type == 'missile':
            for obj2 in OBJECTS:
                if  not (obj1 == obj2) and  obj1.hittest(obj2):
                    obj1.live -= 1  # minus health for missile
                    obj2.live -= 1  # get minus health for obj2
                    if obj2.live <= 0:
                        # if obj2 not (missile or player) not error:
                        try:
                            SCORE.score += obj2.worth  
                            GEN.enemies -= 1
                            INFO.d_enemies += 1
                            INFO.used_bullets = INFO.bullets
                            if INFO.timer2.ready(INFO.maxtime):
                                INFO.timer2.restart()
                        except AttributeError:
                            pass
                       


class EnemyGen:
    """
    generates enemies in time intervals
    """
    def __init__(self):
        self.max = 2  # maximum amount of enemies on screen
        self.max_wait = 100  # time interwal beetween generations
        self.timer1 = Timer()
        self.enemies = 0  # current amount of enemies

    def spawn(self):
        global OBJECTS, screen
        if self.enemies < self.max:
            self.timer1.tick()
            if (self.timer1.ready(self.max_wait)):
                if rnd(1, 5) == 1:
                    target = EnemyGun(screen)
                else:
                    target = Target(screen)
                OBJECTS.append(target)
                self.enemies += 1
                self.timer1.restart()


class Basecircle:
    """
    Base class for inggame objects
    """

    def __init__(self, screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.r = 1
        self.live = 1
        self.vx = 0
        self.vy = 0
        self.color = GREY

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


class Missile(Basecircle):
    """

    """
    def __init__(self, screen, gun, r):
        super().__init__(screen)
        # coordinates of the tip of gun
        self.x = gun.x +  (gun.length + r) * math.cos(gun.an)
        self.y = gun.y +  (gun.length + r) * math.sin(gun.an)
        # velocity of gun
        self.vx = gun.vx
        self.vy = gun.vy
        self.type = 'missile'

    def move(self):
        super().move()
        # check for wall collisions
        if ((self.x + self.r) >= WIDTH):
            self.vx = -self.vx
        if (self.y + self.r) >= HEIGHT:
            self.vy = - self.vy / 2
            self.y = HEIGHT - self.r
        if (self.x +  2 * self.r) <= 0:
            self.live = 0
        if (self.y +  2 * self.r) <= 0:
            self.live = 0
        
    def hittest(self, obj):
        """
        Checks if missile collides with (obj)
        all ingame objects have circle hitboxes
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2
                <= (self.r + obj.r) ** 2):
            return(True)
        else:
            return(False)
        
class Ball(Missile):
    """
    Missile class
    works in composition with Gun
    """

    def __init__(self, screen, gun):
        """
        obj is example of Gun
        """
        r = rnd(10, 20)  #  TRY TO THINK ABOUT IT to bad
        super().__init__(screen, gun, r)
        self.r = r
        self.g_y = -1
        self.color = choice(GAME_COLORS)
        self.timer0 = Timer()
        self.maxtime = 60  # time on ground

    def move(self):
        """
        """
        self.vy += self.g_y
        super().move()
        # check if ball has low speed and stop it on ground
        # magical number, used to stop bouncing
        if (self.y + self.r) >= HEIGHT:
            if self.vy <= abs(2 * self.g_y):  
                self.vy = 0
                self.vx = 0
                self.timer0.tick()
                # also destroy it in maxtime_frames
                if self.timer0.ready(self.maxtime):
                        self.live = 0
        
    


class AnonBall(Missile):
    """
    Missile for EnemyGun
    0-g, unique skin
    """
    def __init__(self, screen, obj):
        r = 20
        super().__init__(screen, obj, r)
        self.r = r
        self.anon_surf = pygame.transform.scale(
            pygame.image.load('pictures/smallanon.bmp'),
            (2 * self.r, 2 * self.r))
        

    def draw(self):
        global screen
        screen.blit(self.anon_surf, (self.x - self.r, self.y - self.r))


class SusBall(Missile):
    """
    """
    def __init__(self, screen, obj):
        r = 20
        super().__init__(screen, obj, r)
        self.r = r
        self.color = choice(GAME_COLORS)
        self.sus_target = choice(OBJECTS)
        self.sus_mode = 30
        self.sus_surf = pygame.transform.scale(
            pygame.image.load('pictures/sus.jpg'),
            (2 * self.r, 2 * self.r))
        self.timer0 = Timer()
        self.sus_speed = 10
        
    def calcspeed(self):
        if OBJECTS.count(self.sus_target) > 0:
            if self.timer0.ready(self.sus_mode):
                angle = math.atan2((self.sus_target.y - self.y),
                                     (self.sus_target.x - self.x))
                self.vx = self.sus_speed * math.cos(angle)
                self.vy = - self.sus_speed * math.sin(angle)

    def move(self):
        SusBall.calcspeed(self)
        super().move()

    def draw(self):
        super().draw()
        if (self.timer0.ready(self.sus_mode) and self.sus_target == player):
            self.sus_surf.set_colorkey((255, 255, 255))
            screen.blit(self.sus_surf,(self.x - self.r, self.y - self.r))
        self.timer0.tick()


class Gun(Basecircle):
    def __init__(self, screen):
        super(). __init__( screen)
        global WIDTH, HEIGHT
        self.f2_power = 20  # min gun power
        self.f2_on = 0  # is gun loading
        self.an = 0  # angle in radians
        self.width = 10
        self.length_base = 20  # base length of barrel
        self.length = 20  # current length
        self.fire_speed = 40  #  min possible frames beetwen shots
        self.maxf2_power =  self.f2_power + 10
        self.timer3 = Timer()
        
    def fire2_start(self):
        """
        start loading the gun that player clicks
        """
        if self.timer3.ready(self.fire_speed):
            self.f2_on = 1
            self.timer3.restart()

     
    def fire2_end(self, x_tar, y_tar, obj):
        """
Then player frees button fires
x_tar and y_tar set an angle of attack
obj is an
        """
        if self.f2_on == 1:
            ball = obj
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


class EnemyGun(Gun):
    def __init__(self, screen):
        super().__init__(screen)
        self.type = 'enemygun'
        self.live = 3
        self.r = self. width
        self.x = rnd(self.r, WIDTH)
        self.y = rnd(self.r, HEIGHT)
        self.worth = 10  # how much for destroying

    def fire2_start(self):
        if rnd(1, 10) == 1:
            super().fire2_start()

    def targetting(self):
        super().targetting(player.x , player.y)


    def fire2_end(self):
        global OBJECTS
        if rnd(1, 10) == 1:  # praing to omnissiah
            super().fire2_end(player.x, player.y, AnonBall(screen, self))


class PlayerTank(Gun):
    def __init__(self, screen):
        super().__init__(screen)
        self.r = self.width
        self.x = rnd(self.r, WIDTH)
        self.y = rnd(self.r, HEIGHT)
        self.type = 'player'
        self.fire_speed = 10
        self.speed = 10
        self.W, self.A, self.S, self. D = False, False, False, False
        self.M = False
        self.live = 3

    def targetting(self):
        super().targetting(event.pos[0], event.pos[1])
    
    def fire2_end(self):
        if  not self.M:
            type = Ball(screen ,self)
        else:
            type = SusBall(screen ,self)
        if self.f2_on == 1:
            INFO.bullets += 1
        super().fire2_end(event.pos[0], event.pos[1], type)

    def checkM(self):
        if event.key == pygame.K_m:
            if not self. M:
                self.M = True
            else:
                self.M = False
            
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
        self.r = rnd(20, 50)
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
GEN = EnemyGen()

# was used for game-testing

'''ai = EnemyGun(screen)
bebrovoz228 = EnemyGun(screen)
bebrovoz228.fire_speed = 50
OBJECTS.append(bebrovoz228)
ai.fire_speed = 50
OBJECTS.append(ai)'''

player = PlayerTank(screen)
OBJECTS.append(player)

finished = False
while not finished:
    if player.live <= 0:
        finished = True
    screen.fill(WHITE)
    for object in OBJECTS:
        object.destroy()
        object.draw()
        object.move()
        if object.type == 'enemygun':
            object.fire2_start()
            object.targetting()
            object.fire2_end()

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
            player.fire2_end()
        elif event.type == pygame.MOUSEMOTION:
            player.targetting()
        if event.type == pygame.KEYDOWN:
            player.checkM()
            player.start()
        if event.type == pygame.KEYUP:
            player.stop()
        
    calculateall()
    for object in OBJECTS:
        if object.type == 'player' or object.type == 'enemygun':
            object.power_up()

    GEN.spawn()
pygame.quit()
print('Game Over!')
