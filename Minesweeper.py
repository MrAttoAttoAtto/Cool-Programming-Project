#Minesweeper!

from tkinter import *
import math
import random, time

#Tkinter Class

class MinesweeperMain: #Initialising class
    def __init__(self, xLength, yLength, percentOfBombs):
        self.gameStarted = False

        self.xLength = xLength #sets these variables to the object
        self.yLength = yLength

        self.numOfBombs = math.floor(percentOfBombs/100*self.xLength*self.yLength) #setting the number of bombs

        self.mapData = [] #creating the variable which holds the map data

        self.revealedSquareIds = []

        for q in range(self.yLength): #fills the data with empty strings
            self.mapData.append([])
            
            for r in range(self.xLength):
                self.mapData[q].append('')

        self.bombLocationsReserved = [] #creates a list that will hold the locations where no more bombs can be placed

        self.root = Tk()
        self.root.title('Minesweeper') #sets up the tkinter window

        self.frame = Frame(self.root)
        self.frame.pack()

        if self.xLength % 2 == 0:
            self.timeXPos = int(self.xLength/2-1) #sets the positions so they are in the middle
            self.bombCountXPos = self.timeXPos + 1
        else:
            self.timeXPos = int(self.xLength/2-1.5)
            self.bombCountXPos = self.timeXPos + 2

        self.timeLabel = Label(self.frame, text='Time') #puts the time and bomb count onto the tkinter window
        self.timeLabel.grid(row=0,column=self.timeXPos)

        self.bombLabel = Label(self.frame, text='Bombs')
        self.bombLabel.grid(row=0,column=self.bombCountXPos)

        self.timeStrVar = StringVar()
        self.timeStrVar.set('00:00')
        self.timeClock = Label(self.frame, textvariable =self.timeStrVar)
        self.timeClock.grid(row=1,column=self.timeXPos)

        self.bombStrVar = StringVar()
        self.bombStrVar.set(str(self.numOfBombs))
        self.bombsLeftLabel = Label(self.frame, textvariable=self.bombStrVar)
        self.bombsLeftLabel.grid(row=1,column=self.bombCountXPos)

        self.buttonList = [] #lists to hold data for buttons/labels
        self.buttonStringVarList = []
        self.labelList=[]

        self.xPos = 0 #sets the working positions of the button creation
        self.yPos = 0

        for l in range(self.yLength): #fills the stringvar list with stringvars
            self.buttonStringVarList.append([])
            
            for p in range(self.xLength):
                self.buttonStringVarList[l].append(StringVar())

        for n in range(self.yLength): #fills the button list with spaces that can be overwritten with buttons
            self.buttonList.append([])
            
            for m in range(self.xLength):
                self.buttonList[n].append('')

        for c in range(self.yLength): #fills the button list with spaces that can be overwritten with buttons
            self.labelList.append([])
            
            for d in range(self.xLength):
                self.labelList[c].append('')

        for pos in range(0, self.xLength*self.yLength):  #creates all of the buttons required        
            if self.xPos == self.xLength:
                self.yPos += 1
                self.xPos = 0

            xPosLoc = self.xPos
            yPosLoc = self.yPos

            self.buttonList[self.yPos][self.xPos] = Button(self.frame, height=2, width=7, textvariable=self.buttonStringVarList[self.yPos][self.xPos])
            self.buttonList[self.yPos][self.xPos].grid(row=self.yPos+2, column=self.xPos)
            self.buttonList[self.yPos][self.xPos].bind('<Button-1>', lambda e, xPosLoc=xPosLoc, yPosLoc=yPosLoc: self.revealSquare(xPosLoc, yPosLoc))
            self.buttonList[self.yPos][self.xPos].bind('<Button-3>', lambda e, xPosLoc=xPosLoc, yPosLoc=yPosLoc: self.markSquare(xPosLoc, yPosLoc))
            self.buttonList[self.yPos][self.xPos].bind('<Button-2>', lambda e, xPosLoc=xPosLoc, yPosLoc=yPosLoc: self.chordSquare(xPosLoc, yPosLoc))

            self.xPos += 1

        self.root.mainloop()

    def generateBoard(self, xPos, yPos): #generating the board
        self.bombLocationsReserved.append(xPos+yPos*self.xLength)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength-1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength+1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength-self.xLength)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength+self.xLength)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength-self.xLength-1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength-self.xLength+1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength+self.xLength-1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength+self.xLength+1)

        bombsLeftToPlace = self.numOfBombs

        while bombsLeftToPlace > 0:
            yPlace = 0
            bombPlacement = random.randint(0, self.xLength*self.yLength-1)

            placementValue = bombPlacement

            while bombPlacement >= self.xLength:
                bombPlacement = bombPlacement - self.xLength
                yPlace += 1

            xPlace = bombPlacement

            if not placementValue in self.bombLocationsReserved:
                self.mapData[yPlace][xPlace] = 'B'
                bombsLeftToPlace = bombsLeftToPlace - 1
                self.bombLocationsReserved.append(placementValue)

        for squareXPos in range(0, self.xLength):
            for squareYPos in range(0, self.yLength):
                bombsSurrounding = 0

                if self.mapData[squareYPos][squareXPos] == 'B':
                    self.buttonStringVarList[squareYPos][squareXPos].set('B')
                    continue

                if squareXPos > 0:
                    if squareYPos > 0:
                        if self.mapData[squareYPos-1][squareXPos-1] == 'B':
                            bombsSurrounding += 1

                    if self.mapData[squareYPos][squareXPos-1] == 'B':
                        bombsSurrounding += 1

                    try:
                        if self.mapData[squareYPos+1][squareXPos-1] == 'B':
                            bombsSurrounding += 1
                    except IndexError:
                        pass

                if squareYPos > 0:
                    if self.mapData[squareYPos-1][squareXPos] == 'B':
                        bombsSurrounding += 1

                try:
                    if self.mapData[squareYPos+1][squareXPos] == 'B':
                        bombsSurrounding += 1
                except IndexError:
                    pass

                if squareYPos > 0:
                    try:
                        if self.mapData[squareYPos-1][squareXPos+1] == 'B':
                            bombsSurrounding += 1
                    except IndexError:
                        pass

                try:
                    if self.mapData[squareYPos][squareXPos+1] == 'B':
                        bombsSurrounding += 1
                except IndexError:
                    pass

                try:
                    if self.mapData[squareYPos+1][squareXPos+1] == 'B':
                        bombsSurrounding += 1
                except IndexError:
                    pass

                #self.buttonStringVarList[squareYPos][squareXPos].set(bombsSurrounding)
                self.mapData[squareYPos][squareXPos] = bombsSurrounding

    def revealSquare(self, xPos, yPos, failure=False): #if a square is left-clicked...
        if not self.gameStarted:
            self.generateBoard(xPos, yPos)
            self.gameStarted = True

        if xPos+yPos*self.xLength in self.revealedSquareIds:
            return

        self.revealedSquareIds.append(xPos+yPos*self.xLength)

        self.buttonList[yPos][xPos].destroy()

        self.labelList[yPos][xPos] = Label(self.frame, width=3, height=1, font=(None, 15), text=self.mapData[yPos][xPos])
        self.labelList[yPos][xPos].grid(column=xPos, row=yPos+2)
        self.labelList[yPos][xPos].bind('<Button-2>', lambda e, xPos=xPos, yPos=yPos: self.chordSquare(xPos, yPos))

        if not failure:
            self.root.update()
        time.sleep(0.02)

        if self.mapData[yPos][xPos] == 0:
            if xPos > 0:
                if yPos > 0:
                    try:
                        self.revealSquare(xPos-1, yPos-1)
                    except Exception:
                        pass

                try:
                    self.revealSquare(xPos-1,yPos)
                except Exception:
                    pass

                try:
                    self.revealSquare(xPos-1,yPos+1)
                except Exception:
                    pass

            if yPos > 0:
                try:
                    self.revealSquare(xPos,yPos-1)
                except Exception:
                    pass

            try:
                self.revealSquare(xPos,yPos+1)
            except Exception:
                pass
            
            if yPos > 0:
                try:
                    self.revealSquare(xPos+1,yPos-1)
                except Exception:
                    pass

            try:
                self.revealSquare(xPos+1,yPos)
            except Exception:
                pass

            try:
                self.revealSquare(xPos+1,yPos+1)
            except Exception:
                pass

        if self.mapData[yPos][xPos] == 'B' and not failure:
            for xFail in range(self.xLength*self.yLength):
                yFail = 0
                while xFail >= self.xLength:
                    xFail = xFail - self.xLength
                    yFail += 1
                print(str(xFail)+':'+str(yFail))
                self.revealSquare(xFail,yFail,True)
            for yFail in range(self.yLength):
                if self.buttonList[yFail][0].winfo_exists() == 1:
                    self.revealedSquareIds.remove(yFail*self.xLength)
                print(str(xFail)+':'+str(yFail))
                self.revealSquare(0, yFail, True)
                time.sleep(0.2)


test = MinesweeperMain(16, 16, 17)
