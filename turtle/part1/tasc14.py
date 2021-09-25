import turtle as tt
tt.shape('turtle')
tt.speed(1)

def star(n):
    for i in range(1, n+1, 1):
       tt.forward(100)
       tt.right(180 - 180 / n)
star(5)
tt.clear()
star(11)

