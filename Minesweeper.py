#Minesweeper!

from tkinter import *

#Tkinter Class

class MinesweeperMain():
    def __init__(self, xLength, yLength):
        self.root = Tk()
        self.root.title('Minesweeper')

        self.frame = Frame(self.root)
        self.frame.pack()

        buttonList = []
        buttonStringVarList = []

        xPos = 0
        yPos = 0

        for l in range(yLength):
            buttonStringVarList.append([])
            for p in range(xLength):
                buttonStringVarList[l].append(StringVar())

        for n in range(yLength):
            buttonList.append([])
            for m in range(xLength):
                buttonList[n].append('')

        for pos in range(0,xLength*yLength):
            
            if xPos == xLength:
                yPos += 1
                xPos = 0
            
            buttonList[yPos][xPos] = Button(self.frame, height=1, width=4, textvariable=buttonStringVarList[yPos][xPos])
            buttonList[yPos][xPos].grid(row=yPos,column=xPos)
            buttonList[yPos][xPos].bind('<ButtonRelease-1>', lambda e: self.revealSquare(xPos,yPos))
            buttonList[yPos][xPos].bind('<ButtonRelease-3>', lambda e: self.markSquare(xPos,yPos))
            buttonList[yPos][xPos].bind('<ButtonRelease-2>', lambda e: self.chordSquare(xPos,yPos))

            xPos += 1
