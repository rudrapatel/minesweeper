import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib.cm as cm
from random import randint
from obj import mine, inferenceProbability

def writeGridToFile(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if(grid[i][j] == -1):
                file.write(" M ")
            elif(grid[i][j] == -2):
                file.write(" ? ")
            else:
                file.write(" " + str((grid[i][j])) + " ")
        file.write('\n')
    file.write('\n\n')
   
def generateBoard(dim, n):
    grid = np.zeros([dim, dim], int)
    mineList = list()
    while (n > 0):
        x = randint(0 , dim-1)
        y = randint(0 , dim-1)
        if not grid[x][y] == -1:
            grid[x][y] = -1
            mineList.append((x,y))
            n -= 1


    return grid, mineList

'''
[x-1, y-1]  [x-1, y]  [x-1, y+1]  
[x, y-1]     [x,y]    [x, y +1]
[x+1, y-1] [x+1, y]  [x+1, y+1]
'''
def getNeighbors(node, dim):
    x,y = node
    neighbors = list()
    if x == 0 and y == 0 :                      # top left
        neighbors = [(0,1), (1,0), (1,1)]
    elif x == dim-1 and y ==0:                  # bottom left
        neighbors = [(x-1, y), (x, y+1), (x-1, y+1)]
    elif x == 0 and y == dim-1:                 # top right
        neighbors = [(x, y-1), (x+1, y), (x+1, y-1)]
    elif x == dim-1 and y == dim-1:             # bottom right
        neighbors = [(x, y-1), (x-1, y), (x-1, y-1)]
    elif x == 0:                                # top edge
        neighbors = [(x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1)]
    elif x == dim-1:                            # bottom edge
        neighbors = [(x, y-1), (x-1, y-1), (x-1, y), (x-1, y+1), (x, y+1)]
    elif y == 0:                                # left edge
        neighbors = [(x-1, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x+1, y)]
    elif y == dim-1:                            # right edge
        neighbors = [(x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y)]
    else:                                       # middle of the grid
        neighbors = [(x, y-1), (x-1, y-1), (x-1, y), (x-1, y +1), (x, y+1), (x+1, y+1), (x+1, y), (x+1, y-1)]
    mineCounter = 0
    for neighbor in neighbors:
        x,y  = neighbor
        if (referenceBoard[x,y] == -1):
            mineCounter += 1
    return neighbors, mineCounter
        

def allNodesIdentified(gameBoard):
    for i in range(len(gameBoard)):
        for j in range(len(gameBoard[0])):
            if (gameBoard[i][j] == -2):
                return False
    return True

def updateIterateNodes(iterateNodes, unknownNeighbor, probabilityBoard):
    index = 0
    while index < len(iterateNodes):
        x,y = iterateNodes[index]
        nX, nY = unknownNeighbor
        if (probabilityBoard[x][y].p > probabilityBoard[nX][nY].p):
            iterateNodes.insert(index,unknownNeighbor)
            return iterateNodes
        index += 1

    iterateNodes.insert(index,unknownNeighbor)
    return iterateNodes

    
def playMineSweeperAgent1(referenceBoard, dim, totalMines = None):
    # initialize a game
    newGame = np.full([dim,dim], -2)
    safeBoard = np.zeros([dim,dim]) # O(1) way to check if a node is safe or not, 0 is not known, 1 is safe, 2 not sure, 3 mine
    probabilityBoard = np.full([dim,dim], inferenceProbability(2.0, 0)) # setting bas probability as 2, should never happen as 0 <= p <= 1
    mineNodes = list() # list of mine nodes to send back
    iterateNodes = list()
    startX = randint(0, dim-1)
    startY = randint(0, dim-1)
    iterateNodes.append((startX, startY))
    visited = list()
    turn = 1
    while(not allNodesIdentified(newGame)):
        file.write("  ----- Turn " + str(turn) + " -----\n\n")
        file.write("total mines open: " + str(len(mineNodes)) + "\n\n")
        writeGridToFile(newGame)
        x= None
        y=None
        if (iterateNodes):
            x,y = iterateNodes.pop(0)
            visited.append((x,y))
        else:
            x = randint(0, dim-1)
            y = randint(0, dim-1)
            while (not newGame[x][y] == -2): # making sure the new one we go to is a non identified one
                x = randint(0, dim-1)
                y = randint(0, dim-1)
        
        # check if it is a mine:
        if (referenceBoard[x][y] == -1):
            safeBoard[x][y] = 3             # Update safeBoard
            newGame[x][y] = -1              # Update our actual game
            mineNode = mine((x,y), True)
            mineNodes.append(mineNode)
            if (totalMines):
                if (totalMines >= len(mineNodes)):
                    return newGame, mineNodes
        else:
            neighbors, mineCounter = getNeighbors((x,y), dim)
            safeBoard[x][y] = 1 # mark the element as safe
            newGame[x][y] = mineCounter #  number neighbors that are mine

            # if mineCounter is 0, we know all neighbors are safe, mark them in safe, and add them to be iterated with p of mine as 0
            if (mineCounter == 0):
                for neighbor in neighbors:
                    nX, nY = neighbor
                    probabilityBoard[nX][nY].p = 0
                    safeBoard[nX][nY] = 1
                    if(neighbor not in visited):
                        iterateNodes.insert(0, (neighbor))
            else:                                       #compute and infer the neighbors
                # first remove all the neighbors that have been known as either safe or as mines
                unknownNeighbors = list()
                for neighbor in neighbors:
                    nX, nY = neighbor
                    if (safeBoard[nX][nY] == 1):
                        continue
                        #dont add to unknown
                    elif (safeBoard[nX][nY] == 3):
                        mineCounter -= 1 #lower the counter as we already know about the mine and thus is not anything new
                    else:
                        unknownNeighbors.append(neighbor)
                        safeBoard[nX][nY] = 2
                if (len(unknownNeighbors) == mineCounter): #all the unknowns are mines and ca be identified
                    for unknownNeighbor in unknownNeighbors:
                        nX,nY = unknownNeighbor
                        safeBoard[nX][nY] = 3
                        newGame[nX][nY] = -1
                        mineNode = mine((nX,nY), False)
                        mineNodes.append(mineNode)
                        visited.append(unknownNeighbor)
                        if (unknownNeighbor in iterateNodes):
                            iterateNodes.remove(unknownNeighbor)
                        # removeFromIterateList(unknownNeighbor, iterateNodes)
                        if (totalMines):
                            if (totalMines >= len(mineNodes)):
                                return newGame, mineNodes
                else : # infer about them as we dont knwo what they might be
                    for unknownNeighbor in unknownNeighbors:
                        nX, nY = unknownNeighbor
                        if unknownNeighbor in iterateNodes:
                            iterateNodes.remove(unknownNeighbor)
                        safeBoard[nX][nY] = 2
                        p = probabilityBoard[nX][nY].p
                        numNeighbor = probabilityBoard[nX][nY].numNeighbor
                        probabilityBoard[nX][nY].p = (p*numNeighbor + mineCounter/len(unknownNeighbors))/(numNeighbor+1)
                        probabilityBoard[nX][nY].numNeighbor = numNeighbor+1
                        if(neighbor not in visited):
                            iterateNodes = updateIterateNodes(iterateNodes, unknownNeighbor, probabilityBoard)
        turn += 1




    return newGame, mineNodes
def isAMine(node, mineList):
    x,y = node
    for mine in mineList:
        nX, nY = mine
        if (x == nX) and (y == nY):
            return True

    return False

dim = int(input("What are the dimensions of the grid? "))
n = int(input("How many mines should there be?"))

referenceBoard, mineList = generateBoard(dim, n)
'''
logic for the minesweeper

1. start at a randon (x,y)
2. query and see if there is a mine, 
    if there is , acknowldge a new grid , put it in the mine list, check and remove if it is in the maybe list and then go to  new one,
    otherwise , get its neighbors, and the number of mines surrounding it,
    
3. check with the 'cleared' list to see to find out which neighbor we are certain and for which we arent, after which we add it to maybe list 
4. iterate first through the cleared list, then maybe, if both are empty then at random to the one that is not visited at all and start building the list, 

'''
file = open('output.txt', 'w')
file.write('  ----- Initial Grid -----\n\n')
writeGridToFile(referenceBoard)
file.write('Initial ' + str(n) + ' mines created \n\n')
for m in mineList:
    file.write(str(m))
    file.write('\n')
file.write('\n')
game, nlist = playMineSweeperAgent1(referenceBoard, dim)
file.write('  ----- Final Result -----\n\n')
writeGridToFile(game)
file.write('Mines \t Blown(Stepped on Mine)\n\n')
for discoveredMine in nlist:
    file.write(str(discoveredMine.node) + ' \t ' + str(discoveredMine.blown) )
    file.write('\n')
file.close()
# print (nlist)