import pygame
from pygame.draw import *
from random import randint


def sign(x):
    """
    if x>=0 returns 1
    else returns -1
    """
    if (x >= 0):
        return(1)
    else:
        return(-1)


#  if leaderboard file  doesnt exist, creates it
try:
    BESTPLAYERS = open('BESTPLAYERS.txt', 'x')
    BESTPLAYERS.close()
except FileExistsError:
    pass

BESTPLAYERS = open('BESTPLAYERS.txt', 'r')
#  list of strings: 'position, name, score, time'
AllPlayers = BESTPLAYERS.readlines()
BESTPLAYERS.close()

Players = []  # list of lists of strings: 'position' 'name' 'score' 'time'
for player in AllPlayers:
    Players.append(player.split())

# list of lists [score, name, time]
# time and name are not activly used
ScoreNames = []
for player in Players:
    player[2] = float(player[2])  # score to float
    ScoreNames.append([player[2], player[1], player[3]])


print('What is Your Name, oh  New Great Hero?')
print('Press "Enter" if You Dont Want to Have Your Score on Leaderbord')

# checking if given name is possible
name_good = False
while not name_good:
    NAME = input('NAME:')
    NAME = str(NAME)
    if NAME == '':
        blank_name = True  # incognito mode activation
    else:
        blank_name = False

        overlap_names = False
        for scorename in ScoreNames:
            if (NAME != scorename[1]):
                continue
            overlap_names = True

        spaces_in_name = False
        for letter in NAME.split(sep=' '):
            if (letter != ''):
                continue
            spaces_in_name = True

    if not blank_name:
        if (not spaces_in_name) and (not overlap_names):
            name_good = True
        elif (spaces_in_name):
            print("Do not Use Spaces in Name")
        elif (overlap_names):
            print("Name already Taken")
    else:
        name_good = True
        print('Aнонимность Инкогнито Неузнаваемая Личность')
        print('Incognito mode activated\nYour Score Will Not be Saved')


pygame.init()

FPS = 30
width = 1200
height = 900
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont(None, 24, False, True, None)

ANON_surf = pygame.image.load('pictures/anon.bmp')  # background incognito
ANON_surf = pygame.transform.scale(ANON_surf, (width, height))

anon_surf = pygame.image.load('pictures/smallanon.bmp')  # enemy skin
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE]


class Ball():
    """
    Colorfull Ball, random bounce
    """
    def __init__(self):

        self.GEN_RATE = 1000  # time in ms beetwen ball generations
        self.color = COLORS[randint(0, 5)]
        self.value = 1   # worth in points
        self.speed = 10  # abs of maxmovement in unit time in x/y direction
        self.r = randint(30, 50)

        self.x = randint(100, width - 100)
        self.y = randint(100, height - 100)
        self.v_x = randint(-self.speed, self.speed)
        self.v_y = randint(-self.speed, self.speed)

    def create(self):
        """
        draws a ball on screen
        """
        circle(screen, self.color, (self.x, self.y), self.r)

    def bounce_wall(self):
        """
        checking if the ball reaches border in the next time moment
        change velocity randomly, so it doesnt hit it
        """
        #  checking if on the next step ball touches left-right border
        if (self.x + self.v_x + self.r >= width) or \
                (self.x + self.v_x - self.r <= 0):
            k = randint(1, self.speed)
            self.v_x = -sign(self.v_x) * k  # bounce away with x_speed!=0

            #  change v_y
            self.v_y = randint(-self.speed, self.speed)

            #  checking if on the next step ball touches up -down border
        if (self.y + self.r + self.v_y >= height) or \
           (self.y - self.r + self.v_y <= 0):
            k = randint(1, self.speed)
            self.v_y = -sign(self.v_y) * k  # bounce away y_speed!=0

            #  change v_x; if ball close to left- right border
            #  it will change less, not to hit left-right border
            self.v_x = randint(-min(self.speed, self.x + self.r),
                               min(self.speed, width - self.r - self.x))

    def check_click(self, Mouse_coordinates):
        """
        checks if mouse in hitbox,
        1 if hit, 0 if not
        """
        if ((Mouse_coordinates[0] - self.x) ** 2 +
            (Mouse_coordinates[1] - self.y) ** 2) \
                <= (self.r) ** 2:
            return(1)
        else:
            return(0)


GENERATE_BALL = pygame.USEREVENT + 0
pygame.time.set_timer(GENERATE_BALL, Ball().GEN_RATE)


class Rect():
    """
    Colorfull Rectangle(height>width),
    bounces from whals randomly
    """

    def __init__(self):

        self.GEN_RATE = 1700  # time in ms beetwen rect generations
        self.color = COLORS[randint(0, 5)]
        self.value = 1.5  # worth in points
        self.speed = 5  # abs of movement in unit time in x or y direction
        self.a = randint(60, 100)  # rect width
        self.b = randint(self.a + 10, 120)  # rect height

        self.x = randint(110, width - 119)
        self.y = randint(120, height - 120)
        self.v_x = randint(-self.speed, self.speed)
        self.v_y = randint(-self.speed, self.speed)

    def create(self):
        """
        draws a rect on screen
        """
        rect(screen, self.color, (self.x, self.y, self.a, self.b))

    def bounce_wall(self):
        """
        checking if the ball reaches border in the next time moment
        change velocity randomly, so it doesnt hit it
        """
        #  checking if on the next step rect touches left-right border
        if (self.x + self.v_x + self.a >= width) or \
                (self.x + self.v_x <= 0):
            k = randint(1, self.speed)
            self.v_x = -sign(self.v_x) * k  # bounce away with x_speed!=0

            #  change v_y
            self.v_y = randint(-self.speed, self.speed)

            #  checking if on the next step ball touches up-down border
        if (self.y + self.v_y + self.b >= height) or \
           (self.y + self.v_y <= 0):
            k = randint(1, self.speed)
            self.v_y = -sign(self.v_y) * k  # bounce away with y_speed!=0

            #  change v_x; if ball close to left-right border
            #  it will change less, not to left-right border
            self.v_x = randint(-min(abs(self.speed), self.x),
                               min(abs(self.speed), width - self.a - self.x))

    def check_click(self, mouse_coordinates):
        """
        checks if mouse in hitbox
        1 if hit, 0 if not
        """
        if (mouse_coordinates[0] - self.x >= 0) and \
           (mouse_coordinates[0] - self.x <= self.a) and \
           (mouse_coordinates[1] - self.y >= 0) and \
           (mouse_coordinates[1] - self.y <= self.b):
            return(1)
        else:
            return(0)


GENERATE_RECT = pygame.USEREVENT + 1
pygame.time.set_timer(GENERATE_RECT, Rect().GEN_RATE)


class Susqr():
    """
    Square, bounces from walls normally
    if mouse to close tries to run away
    if mouse and border are close teleports in the center
    if mode = 0 is red, of mode = 1 is anon skin
    """
    def __init__(self):

        self.GEN_RATE = 3000  # time in ms beetwen sqr generations
        self.color = RED
        self.value = 2  # worth in points
        self.speed = 8  # abs of maxmovement in unit time in x or y direction
        self.b = randint(50, 100)  # square length
        self.mindist = 100  # from what dist. from center run away stars
        self.mode = 0

        self.x = randint(100, width - 100)
        self.y = randint(100, height - 100)
        self.v_x = randint(-self.speed, self.speed)
        self.v_y = randint(-self.speed, self.speed)

        self.anon_surf = pygame.transform.scale(anon_surf, (self.b, self.b))

    def create(self):
        """
        draws a square on screen
        if mode = 0 color = red
        if mode = 1 anon skin
        """
        if self.mode == 0:
            rect(screen, self.color, (self.x, self.y, self.b, self.b))
        if self.mode == 1:
            screen.blit(self.anon_surf, (self.x, self.y))

    def run_away(self, Mouse_coordinates):
        """
        if mouse closer than self.mindist
        speed of center  is away from the cursor;
        if in this situation touches border
        teleports to the center
        """
        x_distance = (self.x - Mouse_coordinates[0] + self.b/2)
        y_distance = (self.y - Mouse_coordinates[1] + self.b/2)
        distance = (x_distance ** 2 + y_distance ** 2) ** (1/2)
        if (distance <= self.mindist):
            #  checking if on the next step rect touches left-right border
            if (self.x + self.v_x + self.b >= width) or \
               (self.x + self.v_x <= 0) or \
               (self.y + self.v_y + self.b >= height) or \
               (self.y + self.v_y <= 0):
                #  teleport
                self.x = round(width / 2)
                self.y = round(height / 2)
            try:
                cos = (x_distance / distance)
                sin = (y_distance / distance)
            except ZeroDivisionError:
                cos = 0
                sin = 1
            v = (self.v_x ** 2 + self.v_y ** 2) ** (1/2)
            self.v_x = round(cos * v)
            self.v_y = round(sin * v)

    def bounce_wall(self):
        """
        checking if the ball reaches border in the next time moment
        change velocity as  in elastic collisions
        """
        #  checking if on the next step rect touches left-right border
        if (self.x + self.v_x + self.b >= width) or \
           (self.x + self.v_x <= 0):
            self.v_x = -(self.v_x)   # bounce away with same speed

        #  checking if on the next step ball touches up-down border
        if (self.y + self.v_y + self.b >= height) or \
           (self.y + self.v_y <= 0):
            self.v_y = -(self.v_y)  # bounce away with same speed

    def check_click(self, mouse_coordinates):
        """
        checks if mouse in hitbox,
        1 if hit, 0 if not
        """
        if (mouse_coordinates[0] - self.x >= 0) and \
           (mouse_coordinates[0] - self.x <= self.b) and \
           (mouse_coordinates[1] - self.y >= 0) and \
           (mouse_coordinates[1] - self.y <= self.b):
            return(1)
        else:
            return(0)


GENERATE_SUSQR = pygame.USEREVENT + 2
pygame.time.set_timer(GENERATE_SUSQR, Susqr().GEN_RATE)


def check_click(enemy, mouse_coordinates):
    return(enemy.check_click(mouse_coordinates))


def create(enemy):
    enemy.create()


def bounce_wall(enemy):
    enemy.bounce_wall()


def move(enemy):
    """
    changes x,y by v_x and v_y - distances travelled in unit time
    """
    enemy.x = enemy.x + enemy.v_x
    enemy.y = enemy.y + enemy.v_y


def run_away(enemy, Mouse_coordinates):
    enemy.run_away(Mouse_coordinates)


SCORE = 0
TIME = 0  # time from start of game
ENEMIES = []  # array which holds things you can click on
MAX_ENEMIES = 10   # maximum amount of enemies on  the screen


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    TIME += clock.get_time()
    Mouse_coordinates = (pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        if len(ENEMIES) != MAX_ENEMIES:
            if event.type == GENERATE_BALL:
                ENEMIES.append(Ball())
            if event.type == GENERATE_RECT:
                ENEMIES.append(Rect())
            if event.type == GENERATE_SUSQR:
                ENEMIES.append(Susqr())
                if SCORE >= 10:  # changing mode, to use anon skin
                    ENEMIES[-1].mode = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            #  check if  inside the enemy hitbox and get plus score
            for enemy in ENEMIES:
                if check_click(enemy, Mouse_coordinates) == 1:
                    ENEMIES.remove(enemy)
                    SCORE = SCORE + enemy.value
                                                              
    for enemy in ENEMIES:
        try:
            run_away(enemy, Mouse_coordinates)
        except AttributeError:
            pass
        bounce_wall(enemy)
        move(enemy)
        create(enemy)

    #  using SCORESIGN to render pygame font
    SCORESIGN = bytes('Score:' + str(SCORE), encoding='utf-8')
    img = font.render(SCORESIGN, True, WHITE)
    screen.blit(img, (20, 20))

    pygame.display.update()
    if not blank_name or SCORE < 10:
        screen.fill(BLACK)
    else:  # enter anonimus mode
        screen.blit(ANON_surf, (0, 0))

pygame.quit()


TIME_PAS = str(round(TIME / 1000)) + 's'
if not blank_name:
    ScoreNames.append([SCORE, NAME, TIME_PAS])  # adding current player
    ScoreNames.sort(reverse=True)

BESTPLAYERS = open('BESTPLAYERS.txt', 'w')
for i in range(len(ScoreNames)):
    print(i + 1, ScoreNames[i][1], ScoreNames[i][0], ScoreNames[i][2],
          file=BESTPLAYERS)
BESTPLAYERS.close()
