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

def tlacsachovnicu(pole):
    for i in pole:
        for j in i:
            print(' '+j, end='')
        print()

tlacsachovnicu(gensachovnicu(23))#test cmd