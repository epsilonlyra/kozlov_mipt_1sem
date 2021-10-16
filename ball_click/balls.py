import pygame
from pygame.draw import *
import random
from random import randint

def sign(x):
  
  """
if x>=0 returns 1
else returns -1
  """
  
  if (x>=0):
    return(1)
  else:
    return(-1)



#  if leaderboard file  doesnt exist, creates it
try:
    BESTPLAYERS = open('BESTPLAYERS.txt', 'x')
    BESTPLAYERS.close()
    already_exists = False
except:
    already_exists = True


BESTPLAYERS = open('BESTPLAYERS.txt', 'r')
#  list of strings: 'position, name, score, time'
AllPlayers = BESTPLAYERS.readlines()  
BESTPLAYERS.close()

Players=[]  #  list of lists of strings: 'position' 'name' 'score' 'time'
for player in AllPlayers:
    Players.append(player.split())

# list of lists [score, name, time]
# time and name are not activly used
ScoreNames=[] 
for player in Players:
    player[2] = int(player[2])  # score to int
    ScoreNames.append([player[2], player[1], player[3]])


print('What is Your Name, oh  New Great Hero?')
print('Press "Enter" if You Dont Want to Have Your Score on Leaderbord')

# checking if given name is possible
name_good = False
while not name_good:
    NAME = input('NAME:')  
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
        if len(NAME.split()) != 1:
            spaces_in_name = True
            
    if  not blank_name: 
        if (not spaces_in_name) and (not overlap_names):
            name_good = True
        elif (spaces_in_name):
            print("Do not Use Spaces in Name")
        elif (overlap_names):
            print("Name  already Taken")
    else:
      name_good = True
      print('Aнонимность Инкогнито Неузнаваемая Личность')
      print('Incognito mode activated\nYour Score Will Not be Saved')


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
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

        
class Ball():
     
    def __init__(self):
      
        self.GEN_RATE = 1000 #  time in ms beetwen ball generations
        self.MAX_AMOUNT = 10  #  maximum amount of ball on screen any time
        self.x = randint(100, width - 100)
        self.y = randint(100, height - 100)
        self.r = randint(30, 50)
        self.color = COLORS[randint(0, 5)]
        self.speed = 5 # abs of movement in unit time in x or y direction
        self.v_x = randint(-self.speed, self.speed)
        self.v_y = randint(-self.speed, self.speed)
        
    def create(self):
        """
draws a ball on screen
        """
        circle(screen, self.color, (self.x, self.y), self.r)
        
    def move_x(self):  
        """
movement in unit time in x direction
        """
        self.x = self.x + self.v_x
        
    def move_y(self):
        """
movement in unit time in y dircetion
        """
        self.y = self.y +  self.v_y

    def bounce_wall(self):
        """
checking if the ball reaches border in the next time moment
change velocity randomly, so it doesnt hit it
        """
            #  checking if on the next step ball touches x-border
        if (self.x + self.v_x + self.r >= width) or \
                (self.x  + self.v_x - self.r <= 0):     
            k = randint(1,self.speed)  
            self.v_x = -sign(self.v_x) * k  #  bounce away with x_speed!=0
        
            #  change v_y; if ball close to y-border change speed 
            #  it will change less, not to hit y-border 
            self.v_y = randint(-min(self.speed, self.y + self.r),
                               min(self.speed, height - self.r-self.y))
        
            #  checking if on the next step ball touches y-border        
        if (self.y + self.r + self.v_y >= height) or \
                    (self.y - self.r + self.v_y <= 0):
            k = randint(1, self.speed)
            self.v_y = -sign(self.v_y) * k  #  bounce away with y_speed!=0

            #  change v_x; if ball close to x-border 
            #  it will change less, not to hit x-border
            self.v_x = randint(-min(self.speed, self.x + self.r),
                               min(self.speed, width - self.r - self.x))


SCORE = 0
#  to give it to pyfont we use:
SCORESIGN = bytes('Score:' + str(SCORE), encoding = 'utf-8')

Balls = []
GENERATE_BALL = pygame.USEREVENT + 0
pygame.time.set_timer(GENERATE_BALL, Ball().GEN_RATE)

pygame.display.update()
clock = pygame.time.Clock()

TIME = 0
finished = False

START = pygame.time.get_ticks()
while not finished:
    clock.tick(FPS)
    TIME += clock.get_time()   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            
        if event.type == GENERATE_BALL and len(Balls) != Ball().MAX_AMOUNT:
            Balls.append(Ball())
                                             
        if event.type == pygame.MOUSEBUTTONDOWN:
            #  check if mouse click is inside the ball
            Mouse_coordinates = (pygame.mouse.get_pos())  
            for ball in Balls: 
                if ((Mouse_coordinates[0] - ball.x) **2 \
                      + (Mouse_coordinates[1] - ball.y) **2) \
                    <= (ball.r) **2:
                        Balls.remove(ball)
                        SCORE = SCORE + 1
                        SCORESIGN = bytes('Score:' + str(SCORE),
                                          encoding = 'utf-8')
                                                                            
    for ball in Balls:
        ball.bounce_wall()
        
    for ball in Balls:
        ball.move_x()
        ball.move_y()
        
    for ball  in Balls:
        ball.create()
        
    img = font.render(SCORESIGN, True, WHITE)
    screen.blit(img, (20, 20))
                                                                  
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()


TIME_PAS =  str(round(TIME/1000)) + 's'
if not blank_name:
    ScoreNames.append([SCORE, NAME, TIME_PAS])  #  adding current player
    ScoreNames.sort(reverse = True)  

BESTPLAYERS = open('BESTPLAYERS.txt', 'w')
for i in range (len(ScoreNames)):
    print(i + 1, ScoreNames[i][1], ScoreNames[i][0], ScoreNames[i][2],
          file  =  BESTPLAYERS)
BESTPLAYERS.close()
