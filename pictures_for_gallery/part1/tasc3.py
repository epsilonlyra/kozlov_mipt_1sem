import pygame
from pygame.draw import *

pygame.init()

#setting colors
YELLOW = (255, 255, 0)
OLIVEGREEN = (40, 40, 2)
TAN = (210, 180, 140) 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 255, 255)
DARKRED = (50, 0, 0)
GREY = (128, 128, 128)
DARKGREY = (105, 105, 105)
LIGHTGREY = (220, 220, 220,  (20))
DARKERGREY = (80, 80, 80)
DARKESTGREY = (40, 40, 40)

#setting screen
FPS = 30
screen = pygame.display.set_mode((800, 1000))

rect(screen, GREY, (0, 0, 800, 500))  # draw sky
circle(screen, WHITE, (700, 70), (60))  # draw moon

def ghost(surface, orientation, alpha, x, y, scale):
    
    '''
draws a little ghost on the given surface. 

Usage:
litteghost(surface, x, y, orientation, alpha)

Parameters:
surface is a pygame.surface object to be drawn on
x,y are integers for the coordinates of the center of the ghost's head
orientation is the way the ghost looks(0 for left, 1 for right, default = 0)
alpha is the alpha parameter of the cloud(from 0 to 255)
scale is the scale of the ghost's bounding box:
with scale=1, width is 402, height is 388
Ghost's body is taken from a hand-drawn .bmp file
    '''
    
    if alpha < 0:
        alpha = 0
    if alpha > 255:
        alpha = 255

    surf = pygame.Surface.copy(surface)
    body_surf = pygame.image.load('ghostbody.bmp')
    body_surf.set_colorkey((255, 255, 255))
    body_surf = pygame.transform.scale(body_surf, (round(body_surf.get_width()*scale), round(body_surf.get_height()*scale)))
    if orientation == 1:
        body_surf = pygame.transform.flip(
                body_surf, True, False)
        surf.blit(body_surf, (x - 380*scale, y))

    elif orientation == 0:
        surf.blit(body_surf, (x-20*scale, y))

    circle(surf, LIGHTGREY, (x, y), (int(30*scale)))  #  head

    circle(surf, BLUE, (x - int(20*scale), y), int(12*scale))  #  left eye
    circle(surf, BLACK, (x - int(20*scale), y), int(6*scale))
    ellipse(surf, WHITE, (x - int(20*scale), y, int(12*scale), int(2*scale)))

    circle(surf, BLUE, (x + int(20*scale), y), int(12*scale))  #  right eye
    circle(surf, BLACK, (x + int(20*scale), y), int(6*scale))
    ellipse(surf, WHITE, (x + int(20*scale), y, int(12*scale), int(2*scale)))

    pygame.Surface.set_alpha(surf, alpha)

    surface.blit(surf, (0, 0))

def cloud(surface, COLOR, alpha, x, y, width, length):

    '''
draws a cloud(filled ellipse) on the given surface

Usage:
cloud(surface, x, y, COLOR, visibility, width, length)

Parameters:
surface is a pygame.surface object to be drawn on
x,y are the coordinates of left upper corner of the bounding box of the cloud
COLOR is the color of the cloud
alpha is the alpha parameter of the cloud(from 0 to 255)
any visibility higher than 255 is treated as 255 and any lower than 0 is treated as 0
width and length are corresponding width and length of the bounding box of the cloud
    '''

    if alpha < 0:
        alpha = 0
    if alpha > 255:
        alpha = 255
        
    surf = pygame.Surface.copy(surface)

    ellipse(surf, COLOR, (x, y, length, width))

    pygame.Surface.set_alpha(surf, alpha)
    surface.blit(surf, (0, 0))

def house(surface, x, y, width, length):

    '''
draws a house on the given surface

Usage:
house(surface, x, y, width, length)

Parameters:
surface is a pygame.surface object to be drawn on
x,y are the coordinates of left upper corner of the house
width and length are the corresponding width and length of the house
recommended proportions x:y = 2:3
    '''
    
    surf = pygame.Surface.copy(surface)
    
    rect(surf, OLIVEGREEN, (x, y, width, length))  #  body

    (200, 300)

    for i in range(2):  # lower windows
        rect(surf, DARKRED, ((x + width/20 + width*3/8 * i), y + length*23/30, width/8, length/4))
    rect(surf, YELLOW, (x + width/20 + width*3/8*(i+1), y + length*23/30, width/8, length/4))

    for i in range(4):  #  upper windows
        rect(surf, TAN, ((x + width/20 + width/4 * i), y, width/8, length*5/12))

    #  balcony
    rect(surf, DARKESTGREY, (x - width/10, y + length*5/12, width*6/5, length/20))
    for i in range(10):  #  railing
        rect(surf, DARKESTGREY, ((x - width/10 + width*(235/200)/9 * i), y + length*4/12, width/40, length/8))
    rect(surf, DARKESTGREY, ((x - width/10 + width*(235/200)/9), y + length*4/12, width*14/15, length/30))

    # roof
    polygon(surf, BLACK, ((x - width/10, y), (x, y - 10), (x + width, y - length/30), (x + width*11/10, y)))

    # pipes
    rect(surf, DARKERGREY, (x, y - length/15, 5, length/30))
    rect(surf, DARKERGREY, (x + width/4, y - length/10, width/40, length/15))
    rect(surf, DARKERGREY, (x + width*19/20, y - length*3/20, width/20, length/7.5))
     
    surface.blit(surf, (0, 0))


#  drawing sky clouds
cloud(screen, BLACK, 50, 0, 150, 80, 500)
cloud(screen, DARKERGREY, 255, 300, 100, 60, 700)
cloud(screen, DARKESTGREY, 200, 350, 20, 40, 350)

#  drawing houses
house(screen, 500, 400, 200, 300)
house(screen, 100, 300, 200, 300)

#  drawing ground clouds
cloud(screen, DARKESTGREY, 100, 350, 350, 50, 350)
cloud(screen, DARKGREY, 150, 150, 500, 100, 400)

#  drawing little_ghosts

ghost(screen, 1, 100, 200, 600, 0.5)
ghost(screen, 0, 100, 210, 680, 0.5)
ghost(screen, 1, 100, 220, 800, 0.5)
ghost(screen, 0, 100, 400, 800, 0.5)

# drawing the big_ghost
ghost(screen, 0, 200, 580, 700, 1)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

print("Used Functions: {'cloud'  'ghost'  'house'}")
print("You Can Look Through Documentation After You Close Pygames Window")

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()

answer = input("Want to Know More? 'y/n':")

while(answer == 'y'):  #  documentation module
    f_call = input('Enter Function Name:')
    if f_call in locals():
        print(locals()[f_call].__doc__)
    else:
        print('Function', f_call, 'Does Not Exist, Please Try Again')
        print("Valid Functions:  {'cloud'  'ghost'  'house'}")
       
    answer = input("Anything Else? 'y/n':")

