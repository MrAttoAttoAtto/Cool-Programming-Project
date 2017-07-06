#Minesweeper!

from tkinter import *
import random, time, math, vlc

#Tkinter Class

class MinesweeperMain: #Initialising class
    def __init__(self, xLength, yLength, percentOfBombs, caller=None):
        try: #kills the 'play again' host (if it exists)
            caller.root.destroy()
        except Exception:
            pass
        
        self.gameStarted = False
        self.failure = False
        self.vlc64bitInstalled = True

        try: #checks if the user has vlc
            import vlc
        except Exception:
            self.vlc64bitInstalled = False

        self.xLength = xLength #sets these variables to the object
        self.yLength = yLength

        self.numOfBombs = math.floor(percentOfBombs/100*self.xLength*self.yLength) #setting the number of bombs
        self.bombsLeftToReveal = self.numOfBombs #sets a variable that will allow for enough labels to be created
        
        if self.vlc64bitInstalled:
            self.explosionSound = vlc.MediaPlayer('explosion-sound.mp3') #loads the sound

        self.mapData = [] #creating the variable which holds the map data

        self.revealedSquareIds = [] #list so that, when the loss occurs and all tiles are revealed, already revealed squares are not affected

        for q in range(self.yLength): #fills the data with empty strings
            self.mapData.append([])
            
            for r in range(self.xLength):
                self.mapData[q].append('')

        self.bombLocationsReserved = [] #creates a list that will hold the locations where no more bombs can be placed

        self.root = Tk()
        self.root.title('Minesweeper') #sets up the tkinter window

        self.flagImage = PhotoImage(file='flag.png')
        self.bombImage = PhotoImage(file='mine2-11.png')
        self.explosionImage = PhotoImage(file='explosion.png') #sets up the images

        self.frame = Frame(self.root) #makes the frame widget
        self.frame.pack()

        self.labelFrameList = []

        for g in range(self.yLength): #fills the label frame list with spaces that can be overwritten with frames
            self.labelFrameList.append([])
            
            for h in range(self.xLength):
                self.labelFrameList[g].append(Frame(self.frame, height=55, width=66))
                self.labelFrameList[g][h].pack_propagate(0)

        self.bombLabelList = [] #list for storing the bomb pictures

        for i in range(self.numOfBombs):
            self.bombLabelList.append(Label(self.frame, image=self.bombImage)) #adds the right amount of bomb pictures to the list
            
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
            self.buttonList[self.yPos][self.xPos].bind('<Button-1>', lambda e, xPosLoc=xPosLoc, yPosLoc=yPosLoc: self.revealSquare(xPosLoc, yPosLoc)) #reveals the square if left-clicked
            self.buttonList[self.yPos][self.xPos].bind('<Button-3>', lambda e, xPosLoc=xPosLoc, yPosLoc=yPosLoc: self.markSquare(xPosLoc, yPosLoc)) #marks the square if right-clicked
            #self.buttonList[self.yPos][self.xPos].bind('<Button-2>', lambda e, xPosLoc=xPosLoc, yPosLoc=yPosLoc: self.chordSquare(xPosLoc, yPosLoc)) #get rid of this!

            self.xPos += 1

        self.root.mainloop() #mainloop!

    def generateBoard(self, xPos, yPos): #generating the board
        self.bombLocationsReserved.append(xPos+yPos*self.xLength) #reserving the 3x3 area around the button placed
        self.bombLocationsReserved.append(xPos+yPos*self.xLength-1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength+1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength-self.xLength)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength+self.xLength)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength-self.xLength-1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength-self.xLength+1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength+self.xLength-1)
        self.bombLocationsReserved.append(xPos+yPos*self.xLength+self.xLength+1)

        bombsLeftToPlace = self.numOfBombs #sets a helpful temporary variable

        while bombsLeftToPlace > 0:
            yPlace = 0
            bombPlacement = random.randint(0, self.xLength*self.yLength-1) #random square id

            placementValue = bombPlacement #another helpful variable

            while bombPlacement >= self.xLength: #figures out the x and y from that
                bombPlacement = bombPlacement - self.xLength
                yPlace += 1

            xPlace = bombPlacement

            if not placementValue in self.bombLocationsReserved: #checks the place isnt reserved
                self.mapData[yPlace][xPlace] = 'B' #updates the map
                bombsLeftToPlace = bombsLeftToPlace - 1 #self-explanatory
                self.bombLocationsReserved.append(placementValue) #reserves the place just taken

        for squareXPos in range(0, self.xLength): #for EVERY square...
            for squareYPos in range(0, self.yLength):
                bombsSurrounding = 0 #sets this to 0

                if self.mapData[squareYPos][squareXPos] == 'B': #if a bomb...
                    self.buttonStringVarList[squareYPos][squareXPos].set('B') #sets the strVar to B (debugging)
                    continue #goes back to the loop

                if squareXPos > 0: #all of this next part finds how many bombs surround a square (and makes sure that it does not wrap around or throw an error)
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

                #self.buttonStringVarList[squareYPos][squareXPos].set(bombsSurrounding) #shows the value of each NON-BOMB square (debugging)
                self.mapData[squareYPos][squareXPos] = bombsSurrounding #updates the mapData with the value of the square

    def revealSquare(self, xPos, yPos): #if a square is left-clicked...
        if not self.gameStarted: #is the game hasnt been generated yet...
            self.generateBoard(xPos, yPos) #generate it having been clicked ath xPos, yPos
            self.gameStarted = True #the board has been generated

        if xPos+yPos*self.xLength in self.revealedSquareIds or (self.buttonList[yPos][xPos]['image'] != '' and not self.failure): #if the id has already been revealed or the square if flagged...
            return #exit the function

        self.revealedSquareIds.append(xPos+yPos*self.xLength) #append the id to the revealed ids

        self.buttonList[yPos][xPos].destroy() #destroy the button

        if self.mapData[yPos][xPos] != 'B': #if it is NOT a bomb...
            self.labelFrameList[yPos][xPos].grid(column=xPos, row=yPos+2) #put the label frame in its place,

            self.labelList[yPos][xPos] = Label(self.labelFrameList[yPos][xPos], width=10, height=5, font=(None, 15), text=self.mapData[yPos][xPos]) #create a label for it,
            self.labelList[yPos][xPos].pack(fill=BOTH, expand=1)
            self.labelList[yPos][xPos].bind('<Button-2>', lambda e, xPos=xPos, yPos=yPos: self.chordSquare(xPos, yPos)) # and if middle-clicked, it will call chordSquare

        if not self.failure: #if the game hasn't been failed...
            self.root.update() #update the window (for nice looking 0 chan reactions)
        time.sleep(0.02) #sleep a bit

        if self.mapData[yPos][xPos] == 0 and not self.failure: #if it is a 0 and the game has not been lost...
            if xPos > 0: #reveal all round it (nice recursiveness)
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

        if self.mapData[yPos][xPos] == 'B': #if it's a bomb...
            self.bombLabelList[self.bombsLeftToReveal-1].grid(row=yPos+2,column=xPos) #put the pic in its place
            self.bombsLeftToReveal = self.bombsLeftToReveal-1 #self-explanatory

        if self.mapData[yPos][xPos] == 'B' and not self.failure: #if it is the bomb which made you lose...
            self.failure = True #you failed
            
            self.explosionLabel = Label(self.frame, image=self.explosionImage) #it becomes an explosion image
            self.explosionLabel.grid(row=yPos+2, column=xPos)# and is placed where it was

            if self.vlc64bitInstalled: #if vlc is installed...
                self.explosionSound.play() #play the sound

            self.root.update() #update to show the explosion
            for xFail in range(self.xLength*self.yLength): #open all squares
                yFail = 0
                while xFail >= self.xLength:
                    xFail = xFail - self.xLength
                    yFail += 1
                print(str(xFail)+':'+str(yFail))
                self.revealSquare(xFail, yFail)

            for yFail in range(self.yLength): #open the first column of squares again (tkinter is dodgy)
                if self.buttonList[yFail][0].winfo_exists() == 1: #make sure they can be changed again
                    self.revealedSquareIds.remove(yFail*self.xLength)
                print('0:'+str(yFail))
                self.revealSquare(0, yFail) #reveal it
                time.sleep(0.1) #sleep for a bit

            self.root.update() #update after all this is done
            
            gameOver = GameOverBox(self) #activate the game over dialog

    def markSquare(self, xPos, yPos):
        if self.buttonList[yPos][xPos]['image'] == '': #if the square is NOT flagged...
            self.buttonList[yPos][xPos].configure(image=self.flagImage, height=49, width=60) #flag it
            self.bombStrVar.set(int(self.bombStrVar.get())-1) #increment the bombs left

        else:
            self.buttonList[yPos][xPos].configure(image='', height=2, width=7) #get rid of the flag
            self.bombStrVar.set(int(self.bombStrVar.get())+1) #increment the bombs left

    def chordSquare(self, xPos, yPos):
        flagsSurrounding = 0
        flagsNeeded = self.mapData[yPos][xPos]
        
        if xPos > 0: #all of this next part finds how many flags surround a square (and makes sure that it does not wrap around or throw an error)
            if yPos > 0:
                try:
                    if self.buttonList[yPos-1][xPos-1]['image'] != '':
                        flagsSurrounding += 1
                except Exception:
                    pass

                try:
                    if self.buttonList[yPos][xPos-1]['image'] != '':
                        flagsSurrounding += 1
                except Exception:
                    pass

                try:
                    if self.buttonList[yPos+1][xPos-1]['image'] != '':
                        flagsSurrounding += 1
                except IndexError:
                    pass
                except Exception:
                    pass

        if yPos > 0:
            try:
                if self.buttonList[yPos-1][xPos]['image'] != '':
                    flagsSurrounding += 1
            except Exception:
                pass

        try:
            if self.buttonList[yPos+1][xPos]['image'] != '':
                flagsSurrounding += 1
        except IndexError:
            pass
        except Exception:
            pass

        if yPos > 0:
            try:
                if self.buttonList[yPos-1][xPos+1]['image'] != '':
                    flagsSurrounding += 1
            except IndexError:
                pass
            except Exception:
                pass

        try:
            if self.buttonList[yPos][xPos+1]['image'] != '':
                flagsSurrounding += 1
        except IndexError:
            pass
        except Exception:
            pass

        try:
            if self.buttonList[yPos+1][xPos+1]['image'] != '':
                flagsSurrounding += 1
        except IndexError:
            pass
        except Exception:
            pass

        if flagsSurrounding == flagsNeeded:
            if xPos > 0: #reveal all around it
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
            

class GameOverBox:
    def __init__(self, master):
        
        self.root = Tk()
        self.root.title('Game Over') #create the window

        self.frame = Frame(self.root) #create the frame
        self.frame.pack()

        self.label = Label(self.frame, text='You lost!', fg='red') #create the label
        self.label.grid(row=0, column=1)
        
        self.playAgainButton = Button(self.frame, text='Play Again', fg='green', command=lambda: self.restart(master)) #create the play again button
        self.playAgainButton.grid(row=1, column=0)

        self.exitButton = Button(self.frame, text='Exit', fg='red', command=lambda: self.exit(master))
        self.exitButton.grid(row=1,column=2)

    def restart(self, master): #the restart function
        master.root.destroy() #kill the MinesweeperMain window
        reopenMain(self) #re-call it

    def exit(self, master):
        master.root.destroy()
        self.root.destroy()
        
def reopenMain(caller): #restarts it outside of the class
    global minesweeper
    minesweeper = MinesweeperMain(16, 16, 17, caller)

minesweeper = MinesweeperMain(16, 16, 17) #the test!
