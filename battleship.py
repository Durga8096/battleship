"""
Battleship Project
Name: Jayakrishna Dasari
Roll No: 2023501010
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["numberOfRows"]=10
    data["numberOfCols"]=10
    data["boardSize"]=500
    data["cellSize"]=50
    data["numberOfShips"]=5
    data["userBoard"]=emptyGrid(data["numberOfRows"],data["numberOfCols"])
    data["computerBoard"]=emptyGrid(data["numberOfRows"],data["numberOfCols"])
    
    data["computerBoard"]=addShips(data["computerBoard"],data["numberOfShips"])
    data["tempShip"]=[]
    
    data["noOfUserShips"]=0
    data["winner"]=None
    
    data["maxNoOfTurns"]=50
    data["noOfTurns"]=0
    
    return data


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data, userCanvas,data["userBoard"],True)
    # drawGrid(data, userCanvas, test.testGrid(),True)   # To test user grid
    drawGrid(data, compCanvas,data["computerBoard"],False)
    
    drawShip(data, userCanvas,data["tempShip"])
    # drawShip(data, userCanvas, test.testShip())   # For testing
    drawGameOver(data,userCanvas)
    return

'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    print(event)
    if event.keysym=="Return":
        makeModel(data)
    pass


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winner"]==None:
        row,col=getClickedCell(data, event)
        if board=="user":
            clickUserBoard(data,row,col)
            
        if board=="comp" and data["noOfUserShips"]==5:
            runGameTurn(data,row,col)
    return

#### STAGE 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid=[]
    for i in range(rows):
        temp=[]
        for j in range(cols):
            temp.append(1)
        grid.append(temp)
    return grid


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    ship=[]
    row=random.randint(1,8)
    col=random.randint(1,8)
    orientation=random.randint(0,1)
    if orientation==0:                  # vertical
        ship.append([row-1,col])
        ship.append([row,col])
        ship.append([row+1,col])
    else:                               #Horizontal
        ship.append([row,col-1])
        ship.append([row,col])
        ship.append([row,col+1])
    return ship

'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    for coordinate in ship:
        if grid[coordinate[0]][coordinate[1]]!=EMPTY_UNCLICKED:
            return False
    return True


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    shipCount=0
    while(shipCount<numShips):
        ship=createShip()
        if checkShip(grid,ship)==True:
            for coordinate in ship:
                grid[coordinate[0]][coordinate[1]]=SHIP_UNCLICKED
            shipCount+=1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for row in range(data["numberOfRows"]):
        topSq = row*data["cellSize"]
        bottomSq = topSq+data["cellSize"]
        for col in range(data["numberOfCols"]):
            leftSq = col*data["cellSize"]
            rightSq = leftSq+data["cellSize"]
            color = "blue"
            if grid[row][col]==SHIP_UNCLICKED and showShips==False:
                color = "blue"
            elif grid[row][col]==SHIP_UNCLICKED:
                color = "yellow"
            elif grid[row][col]==SHIP_CLICKED:
                color = "red"
            elif grid[row][col]==EMPTY_CLICKED:
                color = "white"                
            canvas.create_rectangle(leftSq, topSq,rightSq,bottomSq,fill=color,outline="red",width=1)
    return


### STAGE 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    ship=sorted(ship)
    if (ship[0][0]+1 == ship[1][0] == ship[2][0]-1) and (ship[0][1] == ship[1][1] == ship[2][1]):
        return True
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    ship=sorted(ship)
    if (ship[0][1]+1 == ship[1][1] == ship[2][1]-1) and (ship[0][0] == ship[1][0] == ship[2][0]):
        return True
    return False


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    row=event.y//50
    col=event.x//50
    return [row,col]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i in range(len(ship)):
        topSq = ship[i][0]*data["cellSize"]
        bottomSq = topSq+data["cellSize"]
        leftSq = ship[i][1]*data["cellSize"]
        rightSq = leftSq+data["cellSize"]             
        canvas.create_rectangle(leftSq, topSq,rightSq,bottomSq,fill="white",outline="red",width=1)
    # print(data["userBoard"])


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship)==3 and checkShip(grid,ship) and (isVertical(ship) or isHorizontal(ship)):
        return True   
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["userBoard"],data["tempShip"]):
        for coordinate in data["tempShip"]:
            data["userBoard"][coordinate[0]][coordinate[1]]=SHIP_UNCLICKED
        data["noOfUserShips"]+=1
        data["tempShip"]=[]
    else:
        print("Temporary ship is NOT valid")
        data["tempShip"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["noOfUserShips"]==5:
        return
    for coordinate in data["tempShip"]:
        if coordinate==[row,col]:
            return
    data["tempShip"].append([row,col])
    if len(data["tempShip"])==3:
        placeShip(data)
    if data["noOfUserShips"]==5:
        print("Start Playing")
    return


### STAGE 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col]==SHIP_UNCLICKED:
        board[row][col]=SHIP_CLICKED
    elif board[row][col]==EMPTY_UNCLICKED:
        board[row][col]=EMPTY_CLICKED
    if isGameOver(board):
        data["winner"]=player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["computerBoard"][row][col]==SHIP_CLICKED or data["computerBoard"][row][col]==EMPTY_CLICKED:
        return
    updateBoard(data,data["computerBoard"],row,col,"user")
    row,col=getComputerGuess(data["userBoard"])
    updateBoard(data,data["userBoard"],row,col,"comp")
    data["noOfTurns"]+=1
    if data["maxNoOfTurns"]==data["noOfTurns"]:
        data["winner"]="draw"
    return

 
'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    while(True):
        row=random.randint(0,9)
        col=random.randint(0,9)
        if board[row][col]==EMPTY_UNCLICKED or board[row][col]==SHIP_UNCLICKED:
            return [row,col]
    return


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in board:
        for cell in row:
            if cell==SHIP_UNCLICKED:
                return False
    return True


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"]!=None:
        if data["winner"]=="user":
           canvas.create_text(250,250,fill="green",font="Times 20 italic bold",text="Congratulations, You won!\n Press Enter to play again") 
        elif data["winner"]=="comp":
            canvas.create_text(250,250,fill="green",font="Times 20 italic bold",text="Sorry, You lost!\n Press Enter to play again") 
        else:
            canvas.create_text(250,250,fill="green",font="Times 20 italic bold",text="Draw, Reached max turns!\n Press Enter to play again")
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":

    print("\n" + "#"*15 + " STAGE 1 TESTS " +  "#" * 16 + "\n")
    test.stage1Tests()

    ## Uncomment these for STAGE 2 ##
    
    print("\n" + "#"*15 + " STAGE 2 TESTS " +  "#" * 16 + "\n")
    test.stage2Tests()
    

    ## Uncomment these for STAGE 3 ##
    
    print("\n" + "#"*15 + " STAGE 3 TESTS " +  "#" * 16 + "\n")
    test.stage3Tests()
    

    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
