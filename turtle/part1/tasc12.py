import turtle as tt
tt.shape('turtle')
tt.speed(10)
def semicircle(R):
	for i in range(1, 101, 1):
		tt.forward(R)
		tt.left(1.8)
tt.left(90)
for i in range(1, 6, 1):
	semicircle(5)
	semicircle(1)
x=input()




