# ...instead of readme.md 
# 
# LUDO - Človeče nehnevaj sa 
# by Ostap Pelekh, 1bc., API7
# 
# Game covers all 3 points of the project assignment.
#
# Program simulates The LUDO game.
# It begins with two prompts that ask you about size of board and number of players.
# After that it shows step-by-step simulation of game.
# !!! Please, read the prompts game shows !!!
#
# Differences or Points:
# 1. Next figure of player goes on board only after previous finishes (so each player have max. 1 figure on the board)
# 2. When two or more players are on the same field, they are displayed as number (for example, when 3 players meet, they are shown as 3)
# => Rules with 'blocking the field' and 'meeting on one field' are not implemented
#  
#  ... end of readme.md

#SETUP
from random import randint
from os import system, name

PLAYER_NAMES = ("A", "B", "C", "S")

#MAIN BODY
def main():
    
    #WELCOME FRAME
    #header
    clearScreen()
    print()
    print('----- LUDO: Človeče nehnevaj sa -----')
    print('by Ostap Pelekh')
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

    #players and board INITIALISATION
    gameBoard = gensachovnicu(sizeOfBoard)
    players = initialisePlayers(gameBoard, numberOfPlayers)

    print()
    print('---------- Game starns NOW! ----------')
    input('[press Enter to start]')
    
    #MAIN CYCLE
    playing = True

    playerTurn = 0 #start from first player in the list   
    turnInRowCount = 1
    while playing:

        clearScreen() #update GAME FRAME

        #header
        print()
        print('----- LUDO: Človeče nehnevaj sa -----')
        print('by Ostap Pelekh')
        print()

        player = players[playerTurn]

        diceValue = randint(1,6)

        if player['IsOnBoard']:
            # move(player)

            print('Dice: %s' % diceValue)
            print('Player %s takes %d step(s)!' % (player['Name'], diceValue))
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
        
        if (diceValue != 6 or turnInRowCount == 3) and playing:      #change player turn to next (when 3-turns-in-row or dice is not 6)
            turnInRowCount = 1
            playerTurn += 1
            if playerTurn >= len(players):
                playerTurn = 0
        else: #when 6 on dice
            turnInRowCount += 1
        
        
        tlacsachovnicu(gameBoard, players)
        
        if playing: 
            print('-----------[press Enter]-------------')
            input()
        else:
            print('Player %s Won!' % player['Name'])
            print('-------------- The End ---------------')
            print()

    #end of MAIN CYCLE



#FUNCTIONS/LIB

def clearScreen(): #clear screen function (as part of update)
    
    if name == 'nt': #for Windows
        system('cls')   
    else: #for Mac and Linux('posix')
        system('clear')


def gensachovnicu(size): #generate nxn playing field (y,x) - axises

    if size%2 == 0:
        size+=1
        print('Board must have odd length, so board %sx%s will be used instead. [press Enter to continue]' % (size,size))
        input()

    board = []
    center = int(size/2) 

    for y in range(0, size):

        board.append([])
        
        for x in range(0, size):
        
            if abs(center-x)<=1 or abs(center-y)<=1: #cross draw
                if x==0 or y==0 or y==size-1 or x==size-1:
                    insert ='*'
                elif x==center and y==center:
                    insert = 'X'
                elif x==center or y==center:
                    insert = 'D'
                else:
                    insert = '*'
            else:
                insert=' '
            
            board[y].append(insert)

    return board


def tlacsachovnicu(board, players=[]): #display nxn playing field (board)
    
    n = len(board)
    
    print() #top margin

    for y in range(-1, n):        
        for x in range(-1, n):

            if x == -1 and y == -1: #draw coordinates (edge)
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
                    insert = board[y][x]
                if len(insert) > 1:
                    insert = len(insert)

            print('%2s'  % insert, end='')
        
        print()

    print() #bottom margin


def initialisePlayers(pole, n): #player initialisation (creating data sets as dicts for each player)
    #create starting points and coordinates of first move
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
        createMovesArray(pole, players[i])  #create array of allowed moves for each player

    return players


def createMovesArray(pole, player): #create array that contains sequence of coordinates, which will be followed by player

    going = True    #detecting all '*', until the 'D'
    while going:
        currentPosition_X = player['MovesArray'][len(player['MovesArray'])-1][0]
        currentPosition_Y = player['MovesArray'][len(player['MovesArray'])-1][1]
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
        currentPosition_X = player['MovesArray'][len(player['MovesArray'])-1][0]
        currentPosition_Y = player['MovesArray'][len(player['MovesArray'])-1][1]
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

#GAME
main()