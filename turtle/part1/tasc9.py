import turtle as tt
import math
tt.shape('turtle')
tt.speed(1)
def polyn(n):
	angle=360 / n
	tt.penup()
	tt.goto(0, 0)
	side=2 * 20 * (n - 1)* math.sin((angle/2) / 180 * math.pi)
	tt.goto(20 * (n - 1), 0)
	tt.pendown()
	tt.left(90 + angle/2)
	for i in range (1, n + 1, 1):
		tt.forward(side)
		tt.left(angle)
	tt.right(90 + angle/2)
for i in range (3, 14, 1):
	polyn(i)
x=input()
