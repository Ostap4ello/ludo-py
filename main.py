from random import randint


PLAYER_NAMES = ("M", "B", "C", "S")
NUMBER_OF_PLAYERS = 2

INDEX_X=0
INDEX_Y=1

#board INIT
def gensachovnicu(n): #draw nxn playing field

    if n%2 == 0:
        n+=1
    pole = []
    center = int(n/2) 

    for i in range(-1, n):

        pole.append([])
        
        for j in range(-1, n):
            if i == -1 and j == -1:
                insert = ' '
            elif i == -1:
                insert = str(j%10)
            elif j == -1:
                insert = str(i%10)
            elif abs(center-i)<=1 or abs(center-j)<=1:
                if i==0 or j==0 or j==n-1 or i==n-1:
                    insert ='*'
                elif i==center and j==center:
                    insert = 'X'
                elif i==center or j==center:
                    insert = 'D'
                else:
                    insert = '*'
            else:
                insert=' '
            
            pole[i+1].append(insert)
            #print(' %s' % insert, end='')
        #print()
                
    return pole

def tlacsachovnicu(pole, players=[]):
    for i in range(len(pole)):          #y
        for j in range(len(pole)):      #x
            out = pole[j][i]            #[j=x, i=y]
            for player in players:
                if player['ArrMoves'][player['MoveIndex']] == [j, i]:   #[j=x, i=y]
                    out = player['Name']
            print(' '+out, end='')
        print()
    print()

#player INIT
def initialisePlayers(pole, n):
    #create starting points and directions(first move)
    center = int(len(pole)/2)
    startArr = [[[center+1, 1], [center+1, 2]],
                [[center-1, len(pole)-1], [center-1, len(pole)-2]],
                [[1, center-1],[2, center-1]],
                [[len(pole)-1, center+1],[len(pole)-2, center+1]]]

    #create dicts with data for n players
    players = []
    for i in range(n):
        players.append({
            'Name': PLAYER_NAMES[i],
            'ArrMoves': startArr[i],
            'MoveIndex': 0
            })
        
        createArrMoves(pole, players[i])    

    return players

def createArrMoves(pole, player): #modify player

    going = True
    while going:
        currentpos_X = player['ArrMoves'][len(player['ArrMoves'])-1][INDEX_X]
        currentpos_Y = player['ArrMoves'][len(player['ArrMoves'])-1][INDEX_Y]
        lastpos = player['ArrMoves'][len(player['ArrMoves'])-2]

        for dx, dy in [[0,1],[1,0],[-1,0],[0,-1]]:
            if (currentpos_X+dx in range(1,len(pole))) and (currentpos_Y+dy in range(1,len(pole))):
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
            if (currentpos_X+dx in range(1,len(pole))) and (currentpos_Y+dy in range(1,len(pole))):
                if [currentpos_X+dx, currentpos_Y+dy] != lastpos:
                    if pole[currentpos_X+dx][currentpos_Y+dy] == 'X':
                        going = False
                    elif pole[currentpos_X+dx][currentpos_Y+dy] == 'D':
                        player['ArrMoves'].append([currentpos_X+dx, currentpos_Y+dy])

    # def move(players, player):
       
            
        
                



#game setup
# sizeOfBoard = int(input(''))

gameBoard = gensachovnicu(13)
tlacsachovnicu(gameBoard)

numberOfPlayers = 4

players = initialisePlayers(gameBoard, numberOfPlayers)


#game setup
playing = True
playerIndex = 0
while playing:

    # move(player)
    m = randint(0,7)
    players[playerIndex]['MoveIndex'] += m
    if players[playerIndex]['MoveIndex'] >= len(players[playerIndex]["ArrMoves"]):
        players[playerIndex]['MoveIndex'] = len(players[playerIndex]["ArrMoves"]) - 1
        playing = False
    elif m != 6:
        playerIndex += 1
        if playerIndex >= len(players):
            playerIndex = 0
         
    tlacsachovnicu(gameBoard, players)

print('end')
