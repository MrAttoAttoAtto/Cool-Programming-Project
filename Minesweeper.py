#Minesweeper!

from tkinter import *
import math

#Tkinter Class

class MinesweeperMain:
    def __init__(self, xLength, yLength):
        self.numOfBombs = math.floor(0.17*xLength*yLength)
        
        self.root = Tk()
        self.root.title('Minesweeper')

        self.frame = Frame(self.root)
        self.frame.pack()

        if xLength % 2 == 0:
            self.timeXPos = int(xLength/2-1)
            self.bombCountXPos = self.timeXPos + 1
        else:
            self.timeXPos = int(xLength/2-1.5)
            self.bombCountXPos = self.timeXPos + 1

        self.timeStrVar = StringVar()
        self.timeStrVar.set('00:00')
        self.timeClock = Label(self.frame, textvariable = self.timeStrVar)
        self.timeClock.grid(row=0,column=self.timeXPos)

        self.bombStrVar = StringVar()
        self.bombStrVar.set(str(self.numOfBombs))
        

        self.buttonList = []
        self.buttonStringVarList = []

        self.xPos = 0
        self.yPos = 0

        for l in range(yLength):
            self.buttonStringVarList.append([])
            
            for p in range(xLength):
                self.buttonStringVarList[l].append(StringVar())

        for n in range(yLength):
            self.buttonList.append([])
            
            for m in range(xLength):
                self.buttonList[n].append('')

        for o in range(0,xLength*yLength):          
            if self.xPos == xLength:
                self.yPos += 1
                self.xPos = 0
            
            self.buttonList[self.yPos][self.xPos] = Button(self.frame, height=1, width=4, textvariable=self.buttonStringVarList[self.yPos][self.xPos])
            self.buttonList[self.yPos][self.xPos].grid(row=self.yPos+1,column=self.xPos)
            self.buttonList[self.yPos][self.xPos].bind('<ButtonRelease-1>', lambda e: self.revealSquare(self.xPos,self.yPos))
            self.buttonList[self.yPos][self.xPos].bind('<ButtonRelease-3>', lambda e: self.markSquare(self.xPos,self.yPos))
            self.buttonList[self.yPos][self.xPos].bind('<ButtonRelease-2>', lambda e: self.chordSquare(self.xPos,self.yPos))

            self.xPos += 1
            
