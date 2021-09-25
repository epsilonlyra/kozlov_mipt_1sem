import turtle as tt
tt.shape('circle')
tt.resizemode('user')
tt.shapesize(0.3, 0.3)
tt.speed(0)
tt.screensize(1500,1500)

def govector(deltax, deltay):  #  movement by vector (deltax,deltay)
    tt.goto(tt.xcor() + deltax, tt.ycor() + deltay)


#drawing floor line
tt.goto(1500,0)
tt.goto(-1500,0)
tt.goto(0,0)


tt.speed(10)
step = 0.05  #  timestep
vx = 10 
vy = 30
ax = -5
k = 0.9   #  yspeed after impact


while(True):
    if (tt.ycor() + (vy * step) < 0):  # cheking if  turtle will hit floor this step
        tt.goto(tt.xcor(), 0)
        vy = -k * vy
    else :
        govector(vx * step, vy * step)
        vy = vy + (ax * step)  
    
    
