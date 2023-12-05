# ...instead of readme.md 
# 
# LUDO - Človeče nehnevaj sa 
# by Ostap Pelekh, 1bc., API7
# 
# Program simulates The LUDO game.
# It begins with two prompts that ask you about size of board and number of players.
# After that it shows step-by-step simulation of game.
# !!! Please, read the prompts game shows !!!
#
# Differences:
# 1. Next figure of player goes on board only after previous finishes (so each player have max. 1 figure on the board)
# 2. When two players are on the same field, they are displayed, as both of letters (for example, when 'A' meets 'B', they are shown as 'AB')
# => Rules with 'blocking the field' and 'meeting on one field' are not implemented
#  
#  ... end of readme.md

from random import randint
from os import system, name

PLAYER_NAMES = ("A", "B", "C", "S")

INDEX_X=0
INDEX_Y=1



 
# define our clear function
def clearScreen():
 
    # for windows
    if name == 'nt':
        a = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        a = system('clear')

#board INIT
def gensachovnicu(n): #generate nxn playing field (y,x) - axis

    if n%2 == 0:
        n+=1
        print('Board must have odd length, so board %sx%s will be used instead. [press Enter to continue]' % (n,n))
        input()

    pole = []
    center = int(n/2) 

    for y in range(0, n):

        pole.append([])
        
        for x in range(0, n):
        
            if abs(center-x)<=1 or abs(center-y)<=1: #cross draw
                if x==0 or y==0 or y==n-1 or x==n-1:
                    insert ='*'
                elif x==center and y==center:
                    insert = 'X'
                elif x==center or y==center:
                    insert = 'D'
                else:
                    insert = '*'
            else:
                insert=' '
            
            pole[y].append(insert)

    return pole


def tlacsachovnicu(pole, players=[]):
    
    n = len(pole)
    
    print() #top margin before printing

    for y in range(-1, n):        
        for x in range(-1, n):

            if x == -1 and y == -1: #draw coordinates
                insert = ' '
            elif x == -1:
                insert = str(y%10)
            elif y == -1:
                insert = str(x%10)
            
            else:                   #draw board
                insert = ''            
                
                for player in players:  #if x,y are coords of any player -> draw player
                    if player['IsOnBoard']:
                        if player['MovesArray'][player['MoveIndex']] == [x, y]:   #[]
                            insert += player['Name']
                
                if insert == '':
                    insert = pole[y][x]

            print(' '+insert, end='')
        
        print()

    print() #bottom margin


#player INIT
def initialisePlayers(pole, n):
    #create starting points and directions(first move)
    center = int(len(pole)/2)
    startArr = [[[center+1, 0], [center+1, 1]],
                [[center-1, len(pole)-1], [center-1, len(pole)-2]],
                [[0, center-1],[1, center-1]],
                [[len(pole)-1, center+1],[len(pole)-2, center+1]]]

    #create dicts with data for n players
    players = []
    for i in range(n):
        players.append({
            'Name': PLAYER_NAMES[i],
            'IsOnBoard': False,
            'MoveIndex': 0,
            'PlayerCount': (len(pole)-3)/2,
            'MovesArray': startArr[i],
            })
        createMovesArray(pole, players[i])    #create array of allowed moves for each player

    return players

def createMovesArray(pole, player): #create array that contains sequence of coordinates, which will be followed by player

    going = True    #detecting all '*', until the 'D'
    while going:
        currentPosition_X = player['MovesArray'][len(player['MovesArray'])-1][INDEX_X]
        currentPosition_Y = player['MovesArray'][len(player['MovesArray'])-1][INDEX_Y]
        lastPosition = player['MovesArray'][len(player['MovesArray'])-2]

        for dx, dy in [[0,1],[1,0],[-1,0],[0,-1]]:  #check for '*' in each direction except for last position and outer positions
            checkPosition_X = currentPosition_X + dx
            checkPosition_Y = currentPosition_Y + dy
            
            if (checkPosition_X in range(len(pole))) and (checkPosition_Y in range(len(pole))):
                if pole[checkPosition_Y][checkPosition_X] == '*' and [checkPosition_X, checkPosition_Y] != lastPosition:
                    if [checkPosition_X, checkPosition_Y] == player['MovesArray'][0]: #finish, when next pos is start, which means that 'D's should be scanned now
                        going = False
                    else:
                        player['MovesArray'].append([checkPosition_X, checkPosition_Y])
    
    going = True
    while going:      #detecting all '*', until the 'D'
        currentPosition_X = player['MovesArray'][len(player['MovesArray'])-1][INDEX_X]
        currentPosition_Y = player['MovesArray'][len(player['MovesArray'])-1][INDEX_Y]
        lastPosition = player['MovesArray'][len(player['MovesArray'])-2]

        for dx, dy in [[0,1],[1,0],[-1,0],[0,-1]]: #check for 'D' in each direction except for last position and outer positions
            checkPosition_X = currentPosition_X + dx
            checkPosition_Y = currentPosition_Y + dy
            
            if (checkPosition_X in range(len(pole))) and (checkPosition_Y in range(len(pole))):
                if [checkPosition_X, checkPosition_Y] != lastPosition:
                    if pole[checkPosition_Y][checkPosition_X] == 'X':  #finish, when next pos is 'X', which means the end of array
                        going = False
                    elif pole[checkPosition_Y][checkPosition_X] == 'D':
                        player['MovesArray'].append([checkPosition_X, checkPosition_Y])


#game startup

def main(): #MAIN BODY
    
    #header
    clearScreen()
    print()
    print('----- LUDO: Človeče nehnevaj sa -----')
    print('by ostap4ello__')
    print()
    print('Setup:')

    while True: #board size input
        try:
            sizeOfBoard = int(input('Size of Gameboard to be simulated: '))
        except:
            print('Please write a number!')
        else:
            if sizeOfBoard > 4:
                break
            else:
                print('Please write a number bigger than 4!')

    while True: #player count input
        try:
            numberOfPlayers = int(input('Number of players should be simulated: '))
        except:
            print('Please write a number!')
        else:
            if numberOfPlayers in range(1, 5):
                break
            else:
                print('Please write a number between 0 and 5!')

    print()

    #players and board initialisation
    gameBoard = gensachovnicu(sizeOfBoard)

    players = initialisePlayers(gameBoard, numberOfPlayers)

    #MAIN CYCLE
    print('---------- Game starns NOW! ----------')
    input('[press Enter to start]')
    playing = True

    playerTurn = 0 #start from first player in the list   
    while playing:

        clearScreen()

        #header
        print()
        print('----- LUDO: Človeče nehnevaj sa -----')
        print('by ostap4ello__')
        print()

        player = players[playerTurn]

        diceValue = randint(1,6)

        if player['IsOnBoard']:
            # move(player)

            print('Roll a dice!')
            print('Player %s moves by %d steps!' % (player['Name'], diceValue))
            player['MoveIndex'] += diceValue

            if player['MoveIndex'] >= len(player["MovesArray"]) - 1: #player finishes his way
                player['MoveIndex'] = len(player["MovesArray"]) - 1
                
                if player['PlayerCount'] == 0: 
                    playing = False     #end of game

                else:
                    player['IsOnBoard'] = False             #prepare for next iterration
                    lastCoord = player['MovesArray'].pop(player['MoveIndex'])
                    gameBoard[lastCoord[1]][lastCoord[0]] = player['Name'] #draw player permanently

                    player['MoveIndex'] = 0

                    print('Player %s will go to next figure...' % player['Name'], end = '')
        
        else:

            print('Player %s rolls a dice in order to get on the board...' % (player['Name']))
            if diceValue == 6:
                print('%s - Player %s goes on board!' % (diceValue, player['Name']))
                player['IsOnBoard'] = True
                player['PlayerCount'] -= 1
            else:
                print('%s - Sadly, but player %s waits...' % (diceValue, player['Name']))
            #draw cube untill get 6, else skip move
        
        if diceValue != 6 and playing:      #change player turn to next? except when dice was 6 and game is still on
            playerTurn += 1
            if playerTurn >= len(players):
                playerTurn = 0
        
        
        tlacsachovnicu(gameBoard, players)
        if playing: 
            print('-----------[press Enter]-------------')
            input()

        #end of MAIN CYCLE


    print('Player %s Won!' % player['Name'])
    print('-------------- The End ---------------')
    print()
    
    #end of MAIN BODY


#haha that's all the game
main()