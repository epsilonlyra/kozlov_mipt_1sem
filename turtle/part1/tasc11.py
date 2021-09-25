import turtle
turtle.shape('turtle')
def circle(R):
	for i in range(1, 101, 1):
		turtle.forward(R)
		turtle.left(3.6)
for i in range (1, 21, 1):
	circle(i)
	turtle.left(180)
	circle(i)
	turtle.left(180)
x=input()



