import turtle as tt
tt.shape('turtle')
tt.speed(1)


# Movement from current position by vector v, given as a pair of numbers.
def govector(v): 
    tt.goto(tt.xcor() + v[0], tt.ycor() + v[1])


# Lists of numbers from a txt file, turtle starts at the top right corner,
# and leaves a trail, all numbers are drawn in two unitsquares,size=20 
secretcodes = open('secretcodes.txt', 'r')
codes = secretcodes.readlines()  
secretcodes.close()
for i in range(len(codes)):
    codes[i] = codes[i].split()
for i in range(len(codes)):
    for g in range(len(codes[i])):
        codes[i][g] = int(codes[i][g])
    
Allnumbers = [ ] #list of lists, which consist of pairs  of coordinates 
for i in range(len(codes)):
    Allnumbers.append([])

for i in range(len(codes)):
    for g in range(0, len(codes[i])-1, 2):
        Allnumbers[i].append([codes[i][g], codes[i][g+1]])

'''
Usernumbers = input().split()  # read numbers from keypad, 
for i in range(len(Usernumbers)):
    Usernumbers[i] = int(Usernumbers[i])
'''
Usernumbers = [1, 4, 1, 7, 0, 0]  #  draw sample numbers


distance = 20 + 10  # distanse beetween numbers horizontally


# For given user number in list,draws it ,when moves turtle  to the right 
for i in range(len(Usernumbers)):
    CurrentUsernumber = Usernumbers[i]
    for g in range(len(Allnumbers[CurrentUsernumber])):
        govector(Allnumbers[CurrentUsernumber][g])
    tt.penup()
    tt.goto((i + 1) * distance, 0)
    tt.pendown()

        








