import turtle as tt
import random as rnd
tt.shape('turtle')
tt.speed(10)
tt.screensize(2000, 1500)
while(True):
    tt.forward(rnd.randint(1, 100))
    tt.right(rnd.randint(0, 360))

