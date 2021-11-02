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

# screen param(pixels)
WIDTH = 800
HEIGHT = 600

# list of ingame objects (missiles, player, enemyguns, targets)
OBJECTS = []


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
        if enough time(frames)  has passed return True
        """
        if self.time >= maxtime:
            return(True)
        else:
            return(False)

    def tick(self):
        """
        add 1  unit (frame )to time
        """

        self.time += 1

    def restart(self):
        """
        here we go again, change time to zero
        """
        self.time = 0


class Sign():
    """
    used for blitting text on screen for some time
    """
    def __init__(self, screen):
        self.screen = screen
        self.maxtime = 200000  # for how long sign will be seen(frames)
        # coordiates of upper left corner of sign
        self.x = 20
        self.y = 20
        self.timer2 = Timer()
        self.text = ''  # str

    def show(self):
        """
        if timer is not ready blit text on screen
        """
        global font, BLACK
        if not self.timer2.ready(self.maxtime):
            img = font.render(self.text, True, BLACK)
            screen.blit(img, (self.x, self.y))
            self.timer2.tick()  # add  1 to time


def updatesigns():
    """
    Used for updating text for examples of Sign
    """

    global INFO, SCORE, HEALTH
    # iszero function is used to determine if we use plural form or not
    INFO.text = ('You managed to destroy ' +
                 str(INFO.d_enemies) +
                 ' foe' + 's' * iszero(INFO.d_enemies - 1) +
                 ' using ' + str(INFO.used_bullets) +
                 ' missile' + 's' * iszero(INFO.used_bullets - 1))
    SCORE.text = 'score: ' + str(SCORE.score)
    HEALTH.text = 'Health: ' + str(player.live)


def calculateall():
    """
    checks for collisions of ingame objects with missiles
    get plus score, get minus health for objects
    """
    global OBJECTS, SCORE, INFO
    for obj1 in OBJECTS:
        if obj1.type == 'missile':
            for obj2 in OBJECTS:
                if not (obj1 == obj2) and obj1.hittest(obj2):
                    obj1.live -= 1  # minus health for missile
                    obj2.live -= 1  # get minus health for obj2
                    if obj2.live <= 0:
                        # if obj2 not (missile or player) will pass:
                        try:
                            SCORE.score += obj2.worth
                            GEN.enemies -= 1
                            INFO.d_enemies += 1  # destroy enemy
                            # Bullets used for that destruction equal to /
                            # released bullets
                            INFO.used_bullets = INFO.bullets
                            if INFO.timer2.ready(INFO.maxtime):
                                INFO.timer2.restart()
                        except AttributeError:
                            pass


class EnemyGener:
    """
    generates enemies in time intervals
    """
    def __init__(self):
        self.max = 3  # maximum amount of enemies on screen
        self.max_wait = 100  # time interwal beetween generations
        self.timer1 = Timer()
        self.enemies = 0  # current amount of enemies

    def spawn(self):
        """
        Add enemy to OBJECTS list if enough time since last spawn passed
        """
        global OBJECTS, screen
        if self.enemies < self.max:
            self.timer1.tick()
            if (self.timer1.ready(self.max_wait)):
                if rnd(1, 5) == 1:  # will spawn in 20 % cases
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
        self.vy = 0  # if positive moves up
        self.color = GREY

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (int(self.x), int(self.y)),
            int(self.r)
            )

    def destroy(self):
        """
        if hp of object is low destroyes it
        """
        if self.live <= 0:
            OBJECTS.remove(object)

    def move(self):
        """
        positive vx moving right
        postive vy moving up
        """
        self.x += self.vx
        self.y -= self.vy  # minus because y-axis in pygame looks down


class Missile(Basecircle):
    """
    Base class for all Missiles
    """
    def __init__(self, screen, gun, r):
        """
        gun is Gun class examplar
        r is radius of missile( its hitbox)
        """
        super().__init__(screen)
        # coordinates of the tip of gun
        self.x = gun.x + (gun.length + r) * math.cos(gun.an)
        self.y = gun.y + (gun.length + r) * math.sin(gun.an)
        # velocity of gun
        self.vx = gun.vx
        self.vy = gun.vy
        self.type = 'missile'

    def move(self):
        """
        check for wall collisions
        if object gets pass up or left border sets its life to zero
        """
        global WIDTH, HEIGHT
        super().move()
        if ((self.x + self.r) >= WIDTH):
            self.vx = -self.vx
        if (self.y + self.r) >= HEIGHT:
            self.vy = - self.vy / 2  # lose energy when hit on down wall
            self.y = HEIGHT - self.r

        if (self.x + 2 * self.r) <= 0:
            self.live = 0
        if (self.y + 2 * self.r) <= 0:
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
    Standart missile for player
    """

    def __init__(self, screen, gun):
        """
        gun is example of Gun
        """
        r = rnd(10, 20)  # ball radius
        super().__init__(screen, gun, r)
        self.r = r
        self.g_y = -1  # gravity
        self.color = choice(GAME_COLORS)
        self.timer0 = Timer()
        self.maxtime = 30  # maximun time to spend on  ground

    def move(self):
        """
        adds gravity
        checks if ball has low speed and stop it on ground
        if lies on ground for to long kills it
        """
        self.vy += self.g_y
        super().move()
        # if on ground
        if (self.y + self.r) >= HEIGHT:
            if self.vy <= abs(2 * self.g_y):
                # stop
                self.vy = 0
                self.vx = 0
                self.timer0.tick()
                # also destroy it in maxtime_frames
                if self.timer0.ready(self.maxtime):
                    self.live = 0


class AnonBall(Missile):
    """
    Missile for EnemyGun
    Flies straight, has anonimus skin
    """
    def __init__(self, screen, gun):
        """
        gun is example of Gun
        """
        r = 20  # hitbox radius
        super().__init__(screen, gun, r)
        self.r = r
        self.anon_surf = pygame.transform.scale(
            pygame.image.load('pictures/smallanon.bmp'),
            (2 * self.r, 2 * self.r))

    def draw(self):
        global screen
        screen.blit(self.anon_surf, (self.x - self.r, self.y - self.r))


class SusBall(Missile):
    """
    Ball that is sus
    Alternative player missile
    Starts by going straight, after some time starts to
    Follow random object on screen, except missiles( begins acting sus)
    If  it follows player also has sus skin
    """
    def __init__(self, screen, gun):
        r = 20  # radius
        super().__init__(screen, gun, r)
        self.r = r
        self.color = choice(GAME_COLORS)
        self.sus_target = choice(OBJECTS)  # object which it follows
        self.sus_mode = 15  # time in frames from fire to acting sus
        self.sus_surf = pygame.transform.scale(
            pygame.image.load('pictures/sus.jpg'),
            (2 * self.r, 2 * self.r))
        self.timer0 = Timer()
        self.sus_speed = 10  # speed when acting sus

    def choose(self):
        """
        If choosed sus_target is not ok : it is missile or doesnt exist
        chooses again from OBJECTS, stops when chosen target is ok
        """
        while (OBJECTS.count(self.sus_target) == 0 or
               (self.sus_target.type == 'missile')):
            self.sus_target = choice(OBJECTS)

    def calcspeed(self):
        """
        If current target not ok (was destroyed) sets another
        If acting sus will move towards sus target
        """
        SusBall.choose(self)
        if self.timer0.ready(self.sus_mode):
            angle = math.atan2(
                (self.sus_target.y - self.y),
                (self.sus_target.x - self.x)
                )
            self.vx = self.sus_speed * math.cos(angle)
            self.vy = - self.sus_speed * math.sin(angle)

    def move(self):
        SusBall.calcspeed(self)
        super().move()

    def draw(self):
        """
        Standart ball
        If follows player adds amogus picture
        """
        super().draw()
        if (self.timer0.ready(self.sus_mode) and
                (self.sus_target == player)):
            self.sus_surf.set_colorkey((255, 255, 255))
            screen.blit(self.sus_surf, (self.x - self.r, self.y - self.r))
        self.timer0.tick()  # add  1 frame to time


class Gun(Basecircle):
    """
    Base class for PlayerTank and EnemyGun
    EnemyGun imitates player clicks
    """
    def __init__(self, screen):
        super(). __init__(screen)
        global WIDTH, HEIGHT
        self.f2_power = 10  # current gun power (missile speed)
        self.f2_on = 0  # is gun loading
        self.an = 0  # angle barrel with X-axis (clockwise)
        self.width = 10
        self.length_base = 20  # base length of barrel
        self.length = 20  # current length
        self.fire_speed = 40  # min possible frames beetwen shots
        self.maxf2_power = self.f2_power + 10
        self.timer3 = Timer()  # to control speed of fire

    def fire2_start(self):
        """
        start loading the gun that player clicks
        if player clicks to fast will not work
        """
        if self.timer3.ready(self.fire_speed):
            self.f2_on = 1
            self.timer3.restart()

    def fire2_end(self, x_tar, y_tar, missile):
        """
        Then player frees mousebutton fires
        x_tar and y_tar set an angle of attack
        missile is subclass of Missile
        """
        if self.f2_on == 1:  # if gun was loaded
            missile.vx += self.f2_power * math.cos(self.an)
            missile.vy += - self.f2_power * math.sin(self.an)
            OBJECTS.append(missile)
            self.f2_on = 0  # gun is now unload
            self.f2_power = 10  # gun power back to normal

    def targetting(self, x_tar, y_tar):
        """
        Orient gun by mouse
        """
        self.an = math.atan2(
            (y_tar - self.y),
            (x_tar - self.x)
            )

    def draw(self):
        # hitbox( grey circle)
        pygame.draw.circle(screen, GREY, (self.x, self.y), self.r)
        rectangleplus(screen, self.color, self.x, self.y,  # barrel
                      self.width, self.length, self.an)
        self.timer3.tick()

    def power_up(self):
        """
        If player holds button down
        becames longer  and more powerfull(faster missiles)
        and changes barrel color
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
    """
    Enemy, fires directly  at player with AnonBalls
    Simulates clicks in order to fire
    Is killable gives points for destruction
    """
    def __init__(self, screen):
        super().__init__(screen)
        self.type = 'enemygun'
        self.live = 3
        self.r = self. width  # hitbox
        # random start position
        self.x = rnd(self.r, WIDTH)
        self.y = rnd(self.r, HEIGHT)
        self.worth = 10  # how much score for destroying

    def fire2_start(self):
        """
        Each call(frame) "clicks" with probability 0.1
        """
        if rnd(1, 10) == 1:
            super().fire2_start()

    def targetting(self):
        """
        looks exactly at player, simulates mouse_moution
        """
        super().targetting(player.x, player.y)

    def fire2_end(self):
        """
        If gun loaded each frame "frees mouse" with prob 1/10
        Fires with AnonBall
        """
        global OBJECTS
        if self.f2_on == 1:  # if gun loaded
            if rnd(1, 10) == 1:  # praing to omnissiah
                super().fire2_end(player.x, player.y,
                                  AnonBall(screen, self))


class PlayerTank(Gun):
    def __init__(self, screen):
        super().__init__(screen)
        self.r = self.width
        self.x = rnd(self.r, WIDTH)
        self.y = rnd(self.r, HEIGHT)
        self.type = 'player'
        self.fire_speed = 10
        self.speed = 10  # speed for horizonatal-vertical movement
        # are W, A, S, D on key_board pressed down
        self.W, self.A, self.S, self. D = False, False, False, False
        # if using Balls == False, if using SusBalls == True
        self.changed = False
        self.live = 2  # if equal to zero game ends

    def targetting(self):
        """
        Event is mouse movement
        sets angle if mouse is moved
        """
        super().targetting(event.pos[0], event.pos[1])

    def fire2_end(self):
        """
        Charges gun with one of two types of player missiles
        updates INFo bullets, fires
        """
        global INFO
        if not self.changed:
            type = Ball(screen, self)
        else:
            type = SusBall(screen, self)
        if self.f2_on == 1:
            INFO.bullets += 1
        super().fire2_end(event.pos[0], event.pos[1], type)

    def changeammo(self):
        """
        event is keyboard button down
        if player pushes r changes missile type
        if player pushes r afain changes is back
        """
        if event.key == pygame.K_r:
            if not self.changed:
                self.changed = True
            else:
                self.changed = False

    def start(self):
        """
        check if any of buttons have been pressed
        event is keyboard button down
        """
        if event.key == pygame.K_w:
            self.W = True
        if event.key == pygame.K_s:
            self.S = True
        if event.key == pygame.K_a:
            self.A = True
        if event.key == pygame.K_d:
            self.D = True

    def calcspeed(self):
        """
        calculate speed using info which buttons are pressed
        if orders conflict (on some axis) stay still
        """
        if self.W and not self.S:
            self.vy = self.speed
        elif self.S and not self.W:
            self.vy = - self.speed
        else:
            self.vy = 0

        if self.A and not self.D:
            self.vx = -self.speed
        elif self.D and not self.A:
            self.vx = self.speed
        else:
            self.vx = 0

    def stop(self):
        """
        check of any buttons have benn freed
        event is pygame key up
        """
        if event.key == pygame.K_w:
            self.W = False
        if event.key == pygame.K_s:
            self.S = False
        if event.key == pygame.K_a:
            self.A = False
        if event.key == pygame.K_d:
            self.D = False

    def move(self):
        """
        standart movement, except if gets out of border
        gets back on the other side
        """
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

        # random velosity(positive) and position
        self.x = rnd(self.r, WIDTH - self.r)
        self.vx = rnd(1, 10)
        self.y = rnd(self.r, HEIGHT - self.r)
        self.vy = rnd(1, 10)

    def move(self):
        """
        if touches border reverse velocity
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


screen = pygame.display.set_mode((WIDTH, HEIGHT))  # pygame screen
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)  # font for all  examples of Sign

# Initializing signs, texts are managed by updatesign function

INFO = Sign(screen)
INFO.timer2.time = INFO.maxtime  # at start INFO is not visible
# indent
INFO.x = round(WIDTH / 2) - 20
INFO.y = 100
INFO.maxtime = 100  # time visible
INFO.d_enemies = 0  # destroyed enemies
INFO.bullets = 0  # all used bullets by player
# equal to previous if enemy was exterminated (INFO is seen on screen)
INFO.used_bullets = 0

SCORE = Sign(screen)
SCORE.score = 0

HEALTH = Sign(screen)
HEALTH.health = 0  # player health
HEALTH.x = WIDTH - 100  # for indent

# sign which is shown at the end of game
END = Sign(screen)
END.maxtime = 200
END.text = 'GAME OVER!'
END.x = round(WIDTH / 2) - 40
END.y = round(HEIGHT / 2)

SIGNS = [SCORE, HEALTH, INFO]  # signs can bee seen than game goes on

GEN = EnemyGener()

# used for game-testing
'''
ai = EnemyGun(screen)
bebrovoz228 = EnemyGun(screen)
bebrovoz228.fire_speed = 5
OBJECTS.append(bebrovoz228)
ai.fire_speed = 50
OBJECTS.append(ai)
'''
player = PlayerTank(screen)
OBJECTS.append(player)

finished = False
while not finished:
    screen.fill(WHITE)

    for object in OBJECTS:
        object.destroy()
        object.draw()
        object.move()
        if object.type == 'enemygun':
            object.fire2_start()
            object.targetting()
            object.fire2_end()

    for sign in SIGNS:
        sign.show()

    if player.live <= 0:  # end game
        screen. fill(WHITE)
        END.show()
        # enough time passed - shut down
        if END.timer2.ready(END.maxtime):
            finished = True
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():  # looking for event
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            player.fire2_end()
        elif event.type == pygame.MOUSEMOTION:
            player.targetting()
        elif event.type == pygame.KEYDOWN:
            player.changeammo()
            player.start()
        elif event.type == pygame.KEYUP:
            player.stop()
       
    GEN.spawn()
    updatesigns()
    calculateall()
    for object in OBJECTS:
        if object.type == 'player' or object.type == 'enemygun':
            object.power_up()

pygame.quit()
print('Game Over!')
