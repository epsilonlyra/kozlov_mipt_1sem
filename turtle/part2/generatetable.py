
side=20


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
secretcodes = open('secretcodes.txt', 'w')
for t in range(len(Allnumbers)):
    for i in range (len(Allnumbers[t])):
        for g in range (2):
            print(Allnumbers[t][i][g], file = secretcodes,end = ' ')
    print(file = secretcodes)
secretcodes.close()







