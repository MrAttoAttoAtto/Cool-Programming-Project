#Minesweeper!

from tkinter import *
import math

#Tkinter Class

class MinesweeperMain: #Initialising class
    def __init__(self, xLength, yLength):
        self.gameStarted = False
        
        self.numOfBombs = math.floor(0.17*xLength*yLength) #setting the number of bombs

        self.mapData = [] #creating the variable which holds the map data

        for q in range(yLength): #fills the data with empty strings
            self.mapData.append([])
            
            for r in range(xLength):
                self.mapData[q].append('')

        self.bombLocationsReserved = [] #creates a list that will hold the locations where no more bombs can be placed

        self.root = Tk()
        self.root.title('Minesweeper') #sets up the tkinter window

        self.frame = Frame(self.root)
        self.frame.pack()

        if xLength % 2 == 0:
            self.timeXPos = int(xLength/2-1) #sets the positions so they are in the middle
            self.bombCountXPos = self.timeXPos + 1
        else:
            self.timeXPos = int(xLength/2-1.5)
            self.bombCountXPos = self.timeXPos + 2

        self.timeLabel = Label(self.frame, text='Time') #puts the time and bomb count onto the tkinter window
        self.timeLabel.grid(row=0,column=self.timeXPos)

        self.bombLabel = Label(self.frame, text='Bombs')
        self.bombLabel.grid(row=0,column=self.bombCountXPos)

        self.timeStrVar = StringVar()
        self.timeStrVar.set('00:00')
        self.timeClock = Label(self.frame, textvariabl =self.timeStrVar)
        self.timeClock.grid(row=1,column=self.timeXPos)

        self.bombStrVar = StringVar()
        self.bombStrVar.set(str(self.numOfBombs))
        self.bombsLeftLabel = Label(self.frame, textvariable=self.bombStrVar)
        self.bombsLeftLabel.grid(row=1,column=self.bombCountXPos)

        self.buttonList = [] #lists to hold data for buttons
        self.buttonStringVarList = []

        self.xPos = 0 #sets the working positions of the button creation
        self.yPos = 0

        for l in range(yLength): #fills the stringvar list with stringvars
            self.buttonStringVarList.append([])
            
            for p in range(xLength):
                self.buttonStringVarList[l].append(StringVar())

        for n in range(yLength): #fills the button list with spaces that can be overwritten with buttons
            self.buttonList.append([])
            
            for m in range(xLength):
                self.buttonList[n].append('')

        for pos in range(0,xLength*yLength):  #creates all of the buttons required        
            if self.xPos == xLength:
                self.yPos += 1
                self.xPos = 0
            
            self.buttonList[self.yPos][self.xPos] = Button(self.frame, height=2, width=7, textvariable=self.buttonStringVarList[self.yPos][self.xPos])
            self.buttonList[self.yPos][self.xPos].grid(row=self.yPos+2,column=self.xPos)
            self.buttonList[self.yPos][self.xPos].bind('<ButtonRelease-1>', lambda e: self.revealSquare(self.xPos,self.yPos))
            self.buttonList[self.yPos][self.xPos].bind('<ButtonRelease-3>', lambda e: self.markSquare(self.xPos,self.yPos))
            self.buttonList[self.yPos][self.xPos].bind('<ButtonRelease-2>', lambda e: self.chordSquare(self.xPos,self.yPos))

            self.xPos += 1

    def revealSquare(self,xPos,yPos): #if a square is left-clicked...
        if not self.gameStarted:
        

test = MinesweeperMain(9,9)
