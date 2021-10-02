import pygame
from pygame.draw import *

YELLOW = (255, 255, 0)
OLIVEGREEN = (40, 40, 2)
TAN = (210, 180, 140) #  colour of upper windows
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 255, 255)
DARKRED = (50, 0, 0)
GREY = (128, 128, 128)
DARKGREY = (105, 105, 105)
LIGHTGREY = (220, 220,220,  (20))
DARKERGREY = (80, 80, 80)
DARKESTGREY = (40, 40 ,40) #  we still have 45 to go))

pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 1000))

rect(screen, GREY, (0, 0, 800, 500)) # draw sky

circle(screen, WHITE, (700, 70), (60)) # draw moon


def littleghost(x ,y, orientation,):
    
    '''
draws a transperent little ghost
x,y are the coorfinates of his head
orientation is the way he looks(0 for left, 1 for right)
his body is taken from a hand-drawn  bmp file

    '''

    surf = pygame.Surface.copy(screen)
    body_surf = pygame.image.load('ghostbody.bmp')
    body_surf.set_colorkey((255, 255, 255))
    body_surf = pygame.transform.scale(
    body_surf,(body_surf.get_width() //2,
               body_surf.get_height() //2))
    
    if orientation == 1:
        body_surf = pygame.transform.flip(
                body_surf, True, False)
        surf.blit(body_surf, (x - 190, y))
        
    elif orientation == 0:
        surf.blit(body_surf, (x-10, y))

    
    circle(surf, LIGHTGREY, (x,y), (15)) #  head
        
    circle(surf, BLUE, (x - 10, y), (6)) #  left eye
    circle(surf, BLACK,(x - 10, y), (3))
    ellipse(surf, WHITE, (x - 10, y, 6, 1))

    circle(surf, BLUE, (x + 10, y), (6)) #right eye
    circle(surf, BLACK,(x + 10, y), (3))
    ellipse(surf, WHITE, (x + 10, y, 6, 1))

    pygame.Surface.set_alpha(surf,100)
    
    screen.blit(surf, (0,0))


def cloud(x, y, COLOR, visibility, width,length):

    '''

draws a cloud(filled ellipse)
x,y are the coordinates of left upper corner of coresponding rectangle
visibilty is alpha parameter( from 0- to 255)

    '''
    
    surf = pygame.Surface.copy(screen)

    ellipse(surf, COLOR, (x, y, length, width))
    
    pygame.Surface.set_alpha(surf, visibility)
    screen.blit(surf, (0, 0))



def house(x, y):

    '''

x,y - coordinates of upper left corner

    '''
    surf = pygame.Surface.copy(screen)

    rect(surf, OLIVEGREEN, (x, y, 200, 300)) #  body

    for i in range(2): # down windows
        rect(surf, DARKRED, ((x + 10 + 75 * i), y + 230, 25, 50))
    rect(surf, YELLOW, ((x + 10 + 75 * (i+1)), y + 230, 25, 50))

    for i in range(4): #  upper windows
        rect(surf, TAN, ((x + 10 + 50 * i), y, 25, 125))

    #  balcony
    rect(surf, DARKESTGREY, (x - 20, y + 125, 40 + 200, 15))
    for i in range(10): #  railing
        rect(surf, DARKESTGREY,
             ((x - 20 + (40 + 200 - 5) / 9 * i), y + 125 - 25 , 5, 25))
    rect(surf, DARKESTGREY,
         ((x - 20 + (40 + 200 - 5) / 9), y + 125 - 25, (40 + 200) * 7 / 9, 10))

    # roof
    polygon(surf, BLACK, ((x - 20, y), (x, y - 10),
                          (x + 200, y-10), (x + 200 + 20, y)))

    # pipes
    rect(surf, DARKERGREY, (x, y - 20, 5, 10))
    rect(surf, DARKERGREY, (x + 50 , y - 30, 5, 20))
    rect(surf, DARKERGREY, (x + 190 , y - 45, 10, 40))
        
    screen.blit(surf, (0, 0))



'''

now we begin actuall drawing

'''

#  drawing sky clouds
cloud(0, 150, BLACK, 50, 80, 500)
cloud(300, 100, DARKERGREY,255,60,700)
cloud(350, 20, DARKESTGREY, 200, 40, 350)

#  drawing houses
house(500, 400)
house(100, 300)

#  drawing ground clouds
cloud(350, 350, DARKESTGREY, 100, 50, 350)
cloud(150, 500, DARKGREY, 150, 100, 400)

#  drawing little_ghosts

littleghost(200 ,600, 1)
littleghost(210, 680, 0)
littleghost(220, 800, 1)
littleghost(400, 800, 0)


# drawing big_ghost

body_surf = pygame.image.load('ghostbody.bmp')
body_surf.set_colorkey((255, 255, 255))

screen.blit(body_surf, (580, 700))

circle(screen, LIGHTGREY, (600, 700), (30))

#  eyes
circle(screen, BLUE, (580, 700), (8))
circle(screen, BLACK,(580, 700), (3))
ellipse(screen, WHITE, (580, 700, 8, 1))

circle(screen, BLUE, (620, 700), (8))
circle(screen, BLACK,(620, 700), (3))
ellipse(screen, WHITE, (620, 700, 8, 1))



pygame.display.update()
clock = pygame.time.Clock()
finished = False

print("Used Functions: {'cloud'  'littleghost'  'house'}")
print("You Can Look Through Documentation After You Close Pygames Window")

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()


answer = input ("Want to Know More? 'y/n':")

while(answer == 'y'): #  documentation module
    f_call = input('Enter Function Name:') 
    if f_call in locals():
        print(locals()[f_call].__doc__)
    else:
        print('Function', f_call, 'Does Not Exist, Please Try Again')
        print("Valid Functions:  {'cloud'  'littleghost'  'house'}")
        
    answer= input ("Anything Else? 'y/n':")








