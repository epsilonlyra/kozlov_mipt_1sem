import turtle as tt
tt.shape('turtle')
tt.speed(10)
for i in range (1, 10, 1):
	tt.forward(i * 20)
	tt.left(90)
	tt.forward(i * 20)
	tt.left(90)
	tt.forward(i * 20)
	tt.left(90)
	tt.forward(i *20)
	tt.penup()
	tt.forward(10)
	tt.left(90)
	tt.backward(10)
	tt.pendown()

