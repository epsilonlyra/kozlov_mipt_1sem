from random import randint
import turtle  as tt


#  move some turtle by vector (deltax,deltay)
def govector(deltax, deltay, turtle):  
    turtle.goto(turtle.xcor() + deltax, turtle.ycor() + deltay)

# Drawing the container  
tt.speed(0)
tt.penup()
tt.goto(-300, -300)
tt.pendown()
for i in range(4):
    tt.forward(600)
    tt.left(90)
tt.ht()

#Number of turtles, timestep
N = 10
step = 0.1


# Each turtle(clon[i]) is randomly put in some spot
clon = []
for i in range(N):
    clon.append(0)
for i in range(N):
    clon[i] = tt.Turtle()
    clon[i].shape('circle')
    clon[i].resizemode('user')
    clon[i].shapesize(0.3, 0.3)
    clon[i].speed(3)
for i in range(N):
    clon[i].penup()
    clon[i].goto(randint(-250, 250), randint(-250, 250))


#Each turtle gets random speed components
speedx=[]
speedy=[]
for i in range(N):
    speedx.append(randint(-20, 20))
    speedy.append(randint(-20, 20))


while(True):
    for i in range(N):
        # cheking if turtle will hit left or right wall next step
        if (abs(clon[i].xcor() + (speedx[i] * step)) >= 300):  
            speedx[i]=-speedx[i]
        # cheking if turtle will hit floor or bottom wall
        if (abs(clon[i].ycor() + (speedy[i] * step)) >= 300):  
            speedy[i]=-speedy[i]

        govector(speedx[i] * step, speedy[i] * step, clon[i])


