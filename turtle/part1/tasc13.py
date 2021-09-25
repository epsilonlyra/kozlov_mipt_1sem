import turtle as tt
import math 
tt.shape('turtle')
tt.speed(0)
def semicircle(R):
	for i in range(1, 101, 1):
		tt.forward(R * 1.8 / 180 * math.pi)
		tt.left(1.8)
		
def circle(R):
    for i in range(1, 201, 1):
        tt.forward(R * 1.8 / 180 * math.pi)
        tt.left(1.8)
def small_circle(r):
     for i in range(1, 10, 1):
        tt.forward(r * 36 / 180*math.pi)
        tt.left(36)
R=100
tt.begin_fill()
circle(R)
tt.color('yellow')
tt.end_fill()
tt.penup()

tt.goto (-R/2, 5/4*R)
tt.pendown()
tt.color('black')
tt.begin_fill()
tt.circle(R/7)
tt.color('green')
tt.end_fill()
tt.penup()

tt.goto (R/2, 5/4*R)
tt.pendown()
tt.color('black')
tt.begin_fill()
tt.circle(R/7)
tt.color('green')
tt.end_fill()
tt.penup()

tt.goto(0, 1.5*R)
tt.color('black')
tt.pendown()
tt.pensize(10)
tt.right(90)
tt.forward(R/2)
tt.penup()

tt.goto(-R/4, R/2)
tt.pendown()
tt.color('red')
semicircle(R/4)
tt.hide()

        

