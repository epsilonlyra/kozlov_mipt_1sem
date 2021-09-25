import turtle as tt
tt.shape('turtle')
tt.speed(1)
# Movement from current position by vector v, given as a pair of numbers.
def govector(v): 
    tt.goto(tt.xcor() + v[0], tt.ycor() + v[1])

   
# Each number is drawn in two unit squares
side=20


# Lists of numbers, turtle starts at the top right corner and leaves a trail

number0 = [[0, -2 * side], [-side, 0], [0, 2 * side], [side, 0]]

number1 = [[-side, -side], [side, side], [0, -2*side]]

number2 = [[-side, 0], [side, 0], [0, -side], [-side, 0], [0, -side], [side, 0]]

number3 = [[-side, 0], [side, 0], [-side, -side], [side, 0], [-side, -side]]

number4 = [[0, -2 * side], [0, side], [-side, 0], [0, side]]

number5 = [[-side, 0], [0, -side], [side,0], [0, -side], [-side, 0]]

number6 = [[-side, -side], [side, 0], [0, -side], [-side, 0], [0, side]]

number7 = [[-side, 0], [side, 0], [-side, -side], [0,-side]]

number8 = [
          [0,-2 * side], [-side, 0], [0, side],
          [side,0], [-side, 0], [0, side], [side, 0]
          ]

number9 = [
          [-side, 0], [0, -side], [side, 0], [-side, -side],
          [side, side], [0, side]
          ]



Allnumbers = [
             number0, number1, number2, number3,
             number4, number5, number6,
             number7, number8, number9
             ]

'''
Usernumbers = input().split()  # read numbers from keypad
for i in range(len(Usernumbers)):
    Usernumbers[i] = int(Usernumbers[i])
'''
Usernumbers = [1, 4, 1, 7, 0, 0]


distance =s ide + 10  # distanse beetween numbers horizontally


# For given user number in list,draws it ,when moves turtle  to the right 
for i in range(len(Usernumbers)):
    CurrentUsernumber = Usernumbers[i]
    for g in range(len(Allnumbers[CurrentUsernumber])):
        govector(Allnumbers[CurrentUsernumber][g])
    tt.penup()
    tt.goto((i + 1) * distance, 0)
    tt.pendown()



