from random import randint


PLAYER_NAMES = ("A", "B", "C", "S")

INDEX_X=0
INDEX_Y=1

#board INIT
def gensachovnicu(n): #generate nxn playing field (y,x)

    if n%2 == 0:
        n+=1
        print('Board must have odd length, so board %sx%s will be used instead' % (n,n))
    pole = []
    center = int(n/2) 

    for x in range(0, n):

        pole.append([])
        
        for y in range(0, n):
        
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
            
            pole[x].append(insert)

    return pole


def tlacsachovnicu(pole, players=[]):

    n = len(pole)
    
    print() #top margin
    for y in range(-1, n):        
        for x in range(-1, n):

            if x == -1 and y == -1: #draw borders-coords    
                insert = ' '
            elif x == -1:
                insert = str(y%10)
            elif y == -1:
                insert = str(x%10)
            
            else:
                insert = ''            
                
                for player in players:
                    if player['ArrMoves'][player['MoveIndex']] == [x, y]:   #[]
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
            'ArrMoves': startArr[i],
            'MoveIndex': 0
            })
        createArrMoves(pole, players[i])    #create array of allowed moves for each player

    return players

def createArrMoves(pole, player): #modify player

    going = True
    while going:
        currentpos_X = player['ArrMoves'][len(player['ArrMoves'])-1][INDEX_X]
        currentpos_Y = player['ArrMoves'][len(player['ArrMoves'])-1][INDEX_Y]
        lastpos = player['ArrMoves'][len(player['ArrMoves'])-2]

        for dx, dy in [[0,1],[1,0],[-1,0],[0,-1]]:
            if (currentpos_X+dx in range(len(pole))) and (currentpos_Y+dy in range(len(pole))):
                if pole[currentpos_X+dx][currentpos_Y+dy] == '*' and [currentpos_X+dx, currentpos_Y+dy] != lastpos:
                    if [currentpos_X+dx, currentpos_Y+dy] == player['ArrMoves'][0]:
                        going = False
                    else:
                        player['ArrMoves'].append([currentpos_X+dx, currentpos_Y+dy])
    
    going = True
    while going:
        currentpos_X = player['ArrMoves'][len(player['ArrMoves'])-1][INDEX_X]
        currentpos_Y = player['ArrMoves'][len(player['ArrMoves'])-1][INDEX_Y]
        lastpos = player['ArrMoves'][len(player['ArrMoves'])-2]

        for dx, dy in [[0,1],[1,0],[-1,0],[0,-1]]:
            if (currentpos_X+dx in range(len(pole))) and (currentpos_Y+dy in range(len(pole))):
                if [currentpos_X+dx, currentpos_Y+dy] != lastpos:
                    if pole[currentpos_X+dx][currentpos_Y+dy] == 'X':
                        going = False
                    elif pole[currentpos_X+dx][currentpos_Y+dy] == 'D':
                        player['ArrMoves'].append([currentpos_X+dx, currentpos_Y+dy])


#game startup

while True: #board size input
    try:
        sizeOfBoard = int(input('Size of Gameboard to be simulated: '))
    except:
        print('Please write a number!')
    else:
        if sizeOfBoard >= 4:
            break
        else:
            print('Please write a number bigger than 4')

while True: #player count input
    try:
        numberOfPlayers = int(input('Number of players should be simulated: '))
    except:
        print('Please write a number!')
    else:
        if numberOfPlayers in range(1, 5):
            break
        else:
            print('Please write a number between 0 and 5')

print()

gameBoard = gensachovnicu(sizeOfBoard)
tlacsachovnicu(gameBoard)

players = initialisePlayers(gameBoard, numberOfPlayers)

tlacsachovnicu(gameBoard, players)

playing = True
playerIndex = 0
while playing:

    # move(player)
    m = randint(0,7)
    print('Move: Player %s +%d steps' % (players[playerIndex]['Name'], m))
    players[playerIndex]['MoveIndex'] += m
    if players[playerIndex]['MoveIndex'] >= len(players[playerIndex]["ArrMoves"]):
        players[playerIndex]['MoveIndex'] = len(players[playerIndex]["ArrMoves"]) - 1
        playing = False
    elif m != 6:
        playerIndex += 1
        if playerIndex >= len(players):
            playerIndex = 0
         
    tlacsachovnicu(gameBoard, players)

print('Player %s Won!' % players[playerIndex]['Name'])
print('End!')
print()