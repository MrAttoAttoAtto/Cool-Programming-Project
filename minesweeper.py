#Minesweeper!

from tkinter import *
import random, time, math, threading, os.path, os

#Tkinter Class

class MinesweeperMain: #Initialising class
    def __init__(self, xLength, yLength, percentOfBombs, caller=None, winChoice=True):
        try: #kills the 'play again' host (if it exists)
            caller.root.destroy()
        except TclError:
            pass

        self.gameStarted = False #makes the necessary variables
        self.gameOver = False
        self.vlc64bitInstalled = True
        self.squaresRevealed = 0

        try: #checks if the user has vlc
            import vlc
        except OSError:
            self.vlc64bitInstalled = False

        self.xLength = xLength #sets these variables to the object
        self.yLength = yLength

        self.percentOfBombs = percentOfBombs #sets the variable

        self.numOfBombs = math.floor(self.percentOfBombs/100*self.xLength*self.yLength) #setting the number of bombs
        self.bombsLeftToReveal = self.numOfBombs #sets a variable that will allow for enough labels to be created

        if self.vlc64bitInstalled:
            self.explosionSound = vlc.MediaPlayer(os.path.join('sounds', 'explosion-sound.mp3')) #loads the sounds

            self.winChoice = winChoice

            if self.winChoice: #chooses the sound to load
                self.winSound = vlc.MediaPlayer(os.path.join('sounds', 'win-sound.mp3'))
            else:
                self.winSound = vlc.MediaPlayer(os.path.join('sounds', 'win-sound.wav'))

        self.mapData = [] #creating the variable which holds the map data

        self.revealedSquareIds = [] #list so that, when the loss occurs and all tiles are revealed, already revealed squares are not affected

        self.bombLocationsReserved = [] #creates a list that will hold the locations where no more bombs can be placed

        self.root = Tk()
        self.root.title('Minesweeper') #sets up the tkinter window

        self.listOfNumberImages = [] #sets up this list for holding the images of the numbers

        for x in range(9):
            self.listOfNumberImages.append(PhotoImage(file='numbers'+os.sep+str(x)+'.PNG')) #fills said list

        self.transImage = PhotoImage(file=os.path.join('pictures', 'transparent.png'))
        self.flagImage = PhotoImage(file=os.path.join('pictures', 'flag.png'))
        self.bombImage = PhotoImage(file=os.path.join('pictures', 'mine2-11.png'))
        self.explosionImage = PhotoImage(file=os.path.join('pictures', 'explosion.png')) #sets up the rest of the images

        self.frame = Frame(self.root) #makes the frame widget
        self.frame.pack()

        self.bombLabelList = [] #list for storing the bomb pictures

        for i in range(self.numOfBombs): #adds all the necessary bomb picture labels
            self.bombLabelList.append(Label(self.frame, image=self.bombImage, width=62, height=51)) #adds the right amount of bomb pictures to the list

        if self.xLength % 2 == 0:
            timeXPos = int(self.xLength/2-1) #sets the positions so they are in the middle
            bombCountXPos = timeXPos + 1
        else:
            timeXPos = int(self.xLength/2-1.5)
            bombCountXPos = timeXPos + 2

        self.timeSecs = 0 #sets these time variables
        self.timeMins = 0

        self.timeLabel = Label(self.frame, text='Time') #puts the time and bomb count onto the tkinter window
        self.timeLabel.grid(row=0, column=timeXPos)

        self.bombLabel = Label(self.frame, text='Bombs')
        self.bombLabel.grid(row=0, column=bombCountXPos)

        self.timeStrVar = StringVar()
        self.timeStrVar.set('00:00')
        self.timeClock = Label(self.frame, textvariable=self.timeStrVar)
        self.timeClock.grid(row=1, column=self.timeXPos)

        self.bombStrVar = StringVar()
        self.bombStrVar.set(str(self.numOfBombs))
        self.bombsLeftLabel = Label(self.frame, textvariable=self.bombStrVar)
        self.bombsLeftLabel.grid(row=1, column=self.bombCountXPos)

        self.buttonList = [] #lists to hold data for buttons/labels
        self.buttonStringVarList = []
        self.labelList = []
        self.isFlaggedList = []

        self.mapData = [] #creating the variable which holds the map data

        for l in range(self.yLength): #fills the lists with their required starting data
            self.buttonStringVarList.append([])
            self.buttonList.append([])
            self.labelList.append([])
            self.isFlaggedList.append([])
            self.mapData.append([])

            for p in range(self.xLength):
                self.buttonStringVarList[l].append(StringVar())
                self.buttonList[l].append('')
                self.labelList[l].append('')
                self.isFlaggedList[l].append(False)
                self.mapData[l].append('')

        self.xPos = 0 #sets the working positions of the button creation
        self.yPos = 0


        for pos in range(0, self.xLength*self.yLength): #creates all of the buttons required
            if self.xPos == self.xLength:
                self.yPos += 1
                self.xPos = 0

            xPosLoc = self.xPos
            yPosLoc = self.yPos

            self.buttonList[self.yPos][self.xPos] = Button(self.frame, height=49, width=60, textvariable=self.buttonStringVarList[self.yPos][self.xPos], image=self.transImage)
            self.buttonList[self.yPos][self.xPos].grid(row=self.yPos+2, column=self.xPos)
            self.buttonList[self.yPos][self.xPos].bind('<Button-1>', lambda e, xPosLoc=xPosLoc, yPosLoc=yPosLoc: self.revealSquare(xPosLoc, yPosLoc)) #reveals the square if left-clicked
            self.buttonList[self.yPos][self.xPos].bind('<Button-3>', lambda e, xPosLoc=xPosLoc, yPosLoc=yPosLoc: self.markSquare(xPosLoc, yPosLoc)) #marks the square if right-clicked

            self.xPos += 1

        self.timerCode() #starts the timer

        self.root.mainloop() #mainloop!

    def timerCode(self):
        try:
            if self.gameOver or self.root.winfo_exists() == 0: #if the game is over or the window has been closed, exit this loop of the timer
                return
        except RuntimeError: #if the window has been forcefully ended
            return

        timerThread = threading.Timer(1.0, self.timerCode) #when started, in one second, run this program again
        timerThread.daemon = True #makes it nicer to end
        timerThread.start() #starts the 1 second timer

        self.timeSecs += 1 #increments the seconds

        if self.timeSecs == 60: #if it is a minute...
            self.timeSecs = 0 #change the seconds to 0 and add 1 to the mins
            self.timeMins += 1

        if self.timeSecs < 10: #if either is lower than 10, make sure it has a 0 in front of the number
            self.timeSecs = '0'+str(self.timeSecs)

        if self.timeMins < 10:
            self.timeMins = '0'+str(self.timeMins)

        self.timeStrVar.set(str(self.timeMins)+':'+str(self.timeSecs)) #sets the visual time

        self.timeSecs = int(self.timeSecs) #turns them back into ints (just in case they were converted into strings to add 0s to the front of them)
        self.timeMins = int(self.timeMins)

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

                self.mapData[squareYPos][squareXPos] = bombsSurrounding #updates the mapData with the value of the square

    def revealSquare(self, xPos, yPos): #if a square is left-clicked...
        if not self.gameStarted: #is the game hasnt been generated yet...
            self.generateBoard(xPos, yPos) #generate it having been clicked at xPos, yPos
            self.gameStarted = True #the board has been generated

        if xPos+yPos*self.xLength in self.revealedSquareIds or (self.isFlaggedList[yPos][xPos] and not self.gameOver): #if the id has already been revealed or the square if flagged...
            return #exit the function

        self.squaresRevealed += 1 #increments the squares revealed

        self.revealedSquareIds.append(xPos+yPos*self.xLength) #append the id to the revealed ids

        self.buttonList[yPos][xPos].destroy() #destroy the button

        if self.mapData[yPos][xPos] != 'B': #if it is NOT a bomb...
            self.labelList[yPos][xPos] = Label(self.frame, width=62, height=51, image=self.listOfNumberImages[self.mapData[yPos][xPos]]) #create a label for it,
            self.labelList[yPos][xPos].grid(row=yPos+2, column=xPos)
            self.labelList[yPos][xPos].bind('<Button-2>', lambda e, xPos=xPos, yPos=yPos: self.chordSquare(xPos, yPos)) # and if middle-clicked, it will call chordSquare

        if not self.gameOver: #if the game hasn't been failed...
            self.root.update() #update the window (for nice looking 0 chain reactions)
        time.sleep(0.02) #sleep a bit

        if self.mapData[yPos][xPos] == 0 and not self.gameOver: #if it is a 0 and the game has not been lost...
            if xPos > 0: #reveal all round it (nice recursiveness)
                if yPos > 0:
                    try:
                        self.revealSquare(xPos-1, yPos-1)
                    except Exception:
                        pass

                try:
                    self.revealSquare(xPos-1, yPos)
                except Exception:
                    pass

                try:
                    self.revealSquare(xPos-1, yPos+1)
                except Exception:
                    pass

            if yPos > 0:
                try:
                    self.revealSquare(xPos, yPos-1)
                except Exception:
                    pass

            try:
                self.revealSquare(xPos, yPos+1)
            except Exception:
                pass

            if yPos > 0:
                try:
                    self.revealSquare(xPos+1, yPos-1)
                except Exception:
                    pass

            try:
                self.revealSquare(xPos+1, yPos)
            except Exception:
                pass

            try:
                self.revealSquare(xPos+1, yPos+1)
            except Exception:
                pass

        if self.mapData[yPos][xPos] == 'B': #if it's a bomb...
            self.bombLabelList[self.bombsLeftToReveal-1].grid(row=yPos+2, column=xPos) #put the pic in its place
            self.bombsLeftToReveal = self.bombsLeftToReveal-1 #self-explanatory

        if self.mapData[yPos][xPos] == 'B' and not self.gameOver: #if it is the bomb which made you lose...
            self.gameOver = True #you failed

            print('Working...')

            self.explosionLabel = Label(self.frame, width=62, height=51, image=self.explosionImage) #it becomes an explosion image
            self.explosionLabel.grid(row=yPos+2, column=xPos)# and is placed where it was

            if self.vlc64bitInstalled: #if vlc is installed...
                self.explosionSound.play() #play the sound

            self.root.update() #update to show the explosion
            for xFail in range(self.xLength*self.yLength): #open all squares
                yFail = 0
                while xFail >= self.xLength:
                    xFail = xFail - self.xLength
                    yFail += 1
                self.revealSquare(xFail, yFail)

            self.root.update() #update after all this is done

            print('Done!')

            gameOver = GameOverBox(self, 'loss') #activate the game over dialog

        if self.squaresRevealed == self.xLength*self.yLength-self.numOfBombs and not self.gameOver: #if you have revealed all of the non-bomb squares and not failed...
            self.gameOver = True

            print('Working...')

            if self.vlc64bitInstalled: #if vlc is installed...
                self.winSound.play() #play the win sound

            bombLocIds = self.bombLocationsReserved[8:] #give the bomb ids

            for bombId in bombLocIds: #iterate through them
                yLocBomb = 0

                while bombId >= self.xLength: #turn the ids into coordinates
                    bombId = bombId - self.xLength
                    yLocBomb += 1

                xLocBomb = bombId

                self.revealSquare(xLocBomb, yLocBomb) #reveal those coords

            print('Done!')

            gameOver = GameOverBox(self, 'win') #open the win dialog box

    def markSquare(self, xPos, yPos): #flagging
        if not self.isFlaggedList[yPos][xPos]: #if the square is NOT flagged...
            self.buttonList[yPos][xPos].configure(image=self.flagImage, height=49, width=60) #flag it
            self.bombStrVar.set(int(self.bombStrVar.get())-1) #increment the bombs left
            self.isFlaggedList[yPos][xPos] = True

        else:
            self.buttonList[yPos][xPos].configure(image=self.transImage, height=49, width=60) #get rid of the flag
            self.bombStrVar.set(int(self.bombStrVar.get())+1) #increment the bombs left
            self.isFlaggedList[yPos][xPos] = False

    def chordSquare(self, xPos, yPos): #chording
        flagsSurrounding = 0
        flagsNeeded = self.mapData[yPos][xPos]

        if xPos > 0: #all of this next part finds how many flags surround a square (and makes sure that it does not wrap around or throw an error)
            if yPos > 0:
                try:
                    if self.isFlaggedList[yPos-1][xPos-1]:
                        flagsSurrounding += 1
                except Exception:
                    pass

            try:
                if self.isFlaggedList[yPos][xPos-1]:
                    flagsSurrounding += 1
            except Exception:
                pass

            try:
                if self.isFlaggedList[yPos+1][xPos-1]:
                    flagsSurrounding += 1
            except IndexError:
                pass
            except Exception:
                pass

        if yPos > 0:
            try:
                if self.isFlaggedList[yPos-1][xPos]:
                    flagsSurrounding += 1
            except Exception:
                pass

        try:
            if self.isFlaggedList[yPos+1][xPos]:
                flagsSurrounding += 1
        except IndexError:
            pass
        except Exception:
            pass

        if yPos > 0:
            try:
                if self.isFlaggedList[yPos-1][xPos+1]:
                    flagsSurrounding += 1
            except IndexError:
                pass
            except Exception:
                pass

        try:
            if self.isFlaggedList[yPos][xPos+1]:
                flagsSurrounding += 1
        except IndexError:
            pass
        except Exception:
            pass

        try:
            if self.isFlaggedList[yPos+1][xPos+1]:
                flagsSurrounding += 1
        except IndexError:
            pass
        except Exception:
            pass

        if flagsSurrounding == flagsNeeded: #if there are enough, but not too many flags...
            if xPos > 0: #reveal all around it
                if yPos > 0:
                    try:
                        self.revealSquare(xPos-1, yPos-1)
                    except Exception:
                        pass

                try:
                    self.revealSquare(xPos-1, yPos)
                except Exception:
                    pass

                try:
                    self.revealSquare(xPos-1, yPos+1)
                except Exception:
                    pass

            if yPos > 0:
                try:
                    self.revealSquare(xPos, yPos-1)
                except Exception:
                    pass

            try:
                self.revealSquare(xPos, yPos+1)
            except Exception:
                pass

            if yPos > 0:
                try:
                    self.revealSquare(xPos+1, yPos-1)
                except Exception:
                    pass

            try:
                self.revealSquare(xPos+1, yPos)
            except Exception:
                pass

            try:
                self.revealSquare(xPos+1, yPos+1)
            except Exception:
                pass


class GameOverBox: #end of game dialog
    def __init__(self, master, state):
        if state == 'loss': #if you lost
            self.title = 'Game Over' #set these variables
            self.message = 'You Lost!'
            self.color = 'red'
        else: #if you won
            self.title = 'Congratulations' #set these variables
            self.message = 'You Won, Well Done! It took you '+master.timeStrVar.get()+'!'
            self.color = 'green'

        self.root = Tk()
        self.root.title(self.title) #create the window

        self.frame = Frame(self.root) #create the frame
        self.frame.pack()

        self.label = Label(self.frame, text=self.message, fg=self.color) #create the label
        self.label.grid(row=0, column=1)

        self.playAgainButton = Button(self.frame, text='Play Again', fg='green', command=lambda: self.restart(master)) #create the play again button
        self.playAgainButton.grid(row=0, column=0)

        self.exitButton = Button(self.frame, text='Exit and Close', fg='red', command=lambda: self.exit(master)) #create the exit button
        self.exitButton.grid(row=0, column=2)

        self.playOtherButton = Button(self.frame, text='Play another configuration', command=lambda: self.playOther(master)) #create the 'play another config' button
        self.playOtherButton.grid(row=1, column=1)

        self.root.mainloop() #Mainloop!

    def restart(self, master): #the restart function
        try:
            master.root.destroy() #kill the MinesweeperMain window
        except Exception:
            pass
        openMain(self, master=master) #re-call it

    def exit(self, master): #exit func
        try:
            master.root.destroy() #kill the MinesweepreMain window
        except Exception:
            pass
        self.root.destroy() #kill the end of game dialog

    def playOther(self, master):
        global start

        try:
            master.root.destroy() #kill the MinesweeperMain window
        except Exception:
            pass
        start = StartBox(self) #start the Start Box

class StartBox:
    def __init__(self, caller=None):
        try:
            caller.root.destroy() #try killing the play again box (if it exists)
        except Exception:
            pass

        self.choice = True #choice defaults to true

        self.root = Tk() #creates the window
        self.root.title('Start Minesweeper')

        self.frame = Frame(self.root) #creates the frame
        self.frame.pack()

        self.xLabel = Label(self.frame, text='Enter the width of the minesweeper board')
        self.xLabel.grid(row=0, column=0) #creates the xLabel

        self.xLengthStrVar = StringVar()
        self.xInput = Entry(self.frame, width=5, textvariable=self.xLengthStrVar)
        self.xInput.grid(row=1, column=0) #creates the x entry box

        self.yLabel = Label(self.frame, text='Enter the height of the minesweeper board')
        self.yLabel.grid(row=3, column=0) #etc

        self.yLengthStrVar = StringVar()
        self.yInput = Entry(self.frame, width=5, textvariable=self.yLengthStrVar)
        self.yInput.grid(row=4, column=0) #etc

        self.bombPercentLabel = Label(self.frame, text='Enter the percentage of the squares you would like to be bombs')
        self.bombPercentLabel.grid(row=6, column=0) #etc

        self.bombPercentStrVar = StringVar()
        self.bombPercentInput = Entry(self.frame, width=5, textvariable=self.bombPercentStrVar)
        self.bombPercentInput.grid(row=7, column=0) #etc

        self.winChoiceLabel = Label(self.frame, text='Select either the orchestral or vocal win event')
        self.winChoiceLabel.grid(row=9, column=0) #creates the win choice label

        self.vocalWinButton = Button(self.frame, text='Change to vocal', command=lambda: self.setWin(True))
        self.orchestralWinButton = Button(self.frame, text='Change to orchestral', command=lambda: self.setWin(False))
        self.orchestralWinButton.grid(row=10, column=0) #creates both win choice buttons and activates the orchestral one

        self.winChoiceChoiceStrVar = StringVar()
        self.winChoiceChoiceStrVar.set('The vocal win event is selected')
        self.winChoiceChoiceLabel = Label(self.frame, textvariable=self.winChoiceChoiceStrVar)
        self.winChoiceChoiceLabel.grid(row=10, column=1) #creates the StringVar which will tell you which choice you have selected

        self.submitButton = Button(self.frame, text='Submit', fg='green', command=self.completeRequest)
        self.submitButton.grid(row=12, column=0) #submit button

        self.cancelButton = Button(self.frame, text='Cancel and Exit', fg='red', command=self.root.destroy)
        self.cancelButton.grid(row=12, column=1) #exit button

        self.root.mainloop() #Mainloop!

    def setWin(self, choice):
        self.choice = choice #sets the variable

        if self.choice:
            self.vocalWinButton.grid_forget() #updates which buttons you can press and the stringvar
            self.orchestralWinButton.grid(row=10, column=0)
            self.winChoiceChoiceStrVar.set('The vocal win event is selected')

        else:
            self.orchestralWinButton.grid_forget() #see above
            self.vocalWinButton.grid(row=10, column=0)
            self.winChoiceChoiceStrVar.set('The orchestral win event is selected')

    def completeRequest(self): #completes the request
        try:
            self.xLen = int(self.xLengthStrVar.get()) #tries to make them ints/floats
            self.yLen = int(self.yLengthStrVar.get())
            self.bombPercent = float(self.bombPercentStrVar.get())

            if not (self.xLen*self.yLen)-(self.xLen*self.yLen*self.bombPercent/100) >= 9: #if 9 squares cannot be reserved for the first click, dont allow them to play
                error = ErrorBox('The percentage of bombs is too high, the game will not generate')
                return

            openMain(self, self.xLen, self.yLen, self.bombPercent, self.choice) #opens the opener

        except ValueError:
            error = ErrorBox('One or more values you have entered is invalid (all have to be numbers but the percentage does not have to be an integer)') #these have to be numbers!
            pass

class ErrorBox:
    def __init__(self, error):
        self.error = error #sets the error

        self.root = Tk() #creates the window
        self.root.title('Error')

        self.frame = Frame(self.root) #creates the frame
        self.frame.pack()

        self.label = Label(self.frame, text=error, fg='red') #shows the error
        self.label.grid(row=0, column=0)

        self.button = Button(self.frame, text='Ok', command=self.root.destroy) #button to kill the error box
        self.button.grid(row=1, column=0)

        self.root.mainloop() #Mainloop!

def openMain(caller, xLength=None, yLength=None, percentOfBombs=None, winChoice=None, master=None): #restarts it outside of the class
    global minesweeper

    if master != None: #if it has been called from the play again box...
        minesweeper = MinesweeperMain(master.xLength, master.yLength, master.percentOfBombs, caller, master.winChoice) #use the old configs

    else: #else
        minesweeper = MinesweeperMain(xLength, yLength, percentOfBombs, caller, winChoice) #use the new configs

if __name__ == '__main__':
    start = StartBox()
    minesweeper = None
