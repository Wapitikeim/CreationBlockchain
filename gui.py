import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import hashlib
from PIL import ImageTk
import os
from base64 import b64decode

from blockchain import *

from pdc import startBlenderAndStartTakingScreenshots
from pngTogif import createGifFromScreenshotsInFolder


class MainApplication(tk.Frame):
    #Labels
    usernameLabel = tk.Label
    passwordLabel = tk.Label
    loggedInUserLabel = tk.Label
    currentBlockchainLabel = tk.Label
    blockCountOfBlockchain = tk.Label 
    blockchainSizeInMb = tk.Label
    loadedScreenshot = tk.Label
    screenshotCommand = tk.Label
    topThreeCommands = tk.Label
    totalOfUniqueCommands = tk.Label
    #Entrys
    usernameEntry = tk.Entry
    passwordEntry = tk.Entry
    jumpEntry = tk.Entry
    #Buttons
    #-Login
    loginButton = tk.Button
    createNewUserButton = tk.Button
    #-LoadedUser
    logoffButton = tk.Button
    loadBlockchainButton = tk.Button
    createNewBlockchainButton = tk.Button
    #-LoadedBlockchain
    startBlenderButton = tk.Button
    createGifFromScreenshotsButton = tk.Button
    backFromActiveBlockchainButton = tk.Button
    checkIfBlockchainIsValidButton = tk.Button
    #-LoadedScreenshot
    refreshGuiButton = tk.Button
    nextScreenshotButton = tk.Button
    previousScreenshotButton = tk.Button
    jumpToBlockButton = tk.Button
    jumpNext10Button = tk.Button
    previous10Button = tk.Button
    
    #Frames
    global loginCreateFrame 
    global createLoadFrame
    global startBackFrame
    global infoFrame
    global imageFrame

    #UserData
    successfullyLoggedInUser = ""
    successfullyLoggedInUserHash = ""
    currentBlockchainName = "None"
    currentBlockchain = ""
    global loadedImage
    currentIndexOfLoadedImage = "-1"

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.addLogin()
    
    #Setup
    def configure_gui(self):
        self.master.title("Creation Blockchain")
        self.master.geometry("300x150")
    def createUIAfterLogin(self):
        self.master.geometry("1280x720")
        self.addInfoPanel()
        self.addLoadCreateBlockchainButtons()
    def start(self):
        self.master.mainloop()
    #Button Logic
    def validateLoginData(self):
        userID = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if( not userID or not password):
            return

        userHashString = str(userID)+str(password)
        userHash = hashlib.sha512(userHashString.encode()).hexdigest()
        
        UserDatabase = open("scripts/UserDatabase.txt")
        UserDatabaseLines = UserDatabase.read().splitlines()
        for entry in UserDatabaseLines:
            if(entry==userHash):
                self.successfullyLoggedInUser = userID
                self.successfullyLoggedInUserHash = userHash
                self.removeLogin()
                UserDatabase.close()
                self.createUIAfterLogin()
                return
        UserDatabase.close()   
    def askForBlockchainFile(self):
        filePath = filedialog.askopenfilename()
        if not filePath:
            return
        self.currentBlockchainName = os.path.basename(filePath)
        self.currentBlockchain = Blockchain(self.successfullyLoggedInUserHash, self.currentBlockchainName, True)
        if(self.currentBlockchain.allowedToModify == False):
            self.currentBlockchainName = "None"
            self.currentBlockchain = ""
            return
        self.removeInfoPanel()
        self.addInfoPanel()
        self.removeLoadCreateBlockchainButtons()
        self.addBlenderAndGifButtons()
        self.addImageDisplay(-1)
        #self.addBackFromActiveBlockchainButton()
    def createNewBlockchainFile(self):
        newBlockchainName = simpledialog.askstring("Create Blockchain", "Please enter a Name for the Blockchain")
        if not newBlockchainName:
            return 
        if newBlockchainName[-4:] != ".txt":
            newBlockchainName = newBlockchainName + ".txt"
        self.currentBlockchainName = newBlockchainName
        self.currentBlockchain = Blockchain(self.successfullyLoggedInUserHash, self.currentBlockchainName, False)

        self.removeInfoPanel()
        self.addInfoPanel()
        self.removeLoadCreateBlockchainButtons()
        self.addBlenderAndGifButtons()
        #self.addBackFromActiveBlockchainButton()
    def backFromActiveBlockchain(self):
        self.currentBlockchain = ""
        self.currentBlockchainName = "None"
        
        self.removeBlenderAndGifButtons()
        self.removeInfoPanel()
        self.removeImageDisplay()
        self.addInfoPanel()
        self.addLoadCreateBlockchainButtons()
    def logOffUser(self):
        self.successfullyLoggedInUser = ""
        self.removeInfoPanel()
        self.removeLoadCreateBlockchainButtons()
        self.addLogin()
        self.master.geometry("300x150")
    def createNewUserButtonLogic(self):
        self.usernameLabel.config(text="New User:")
        self.passwordLabel.config(text="New Password")
        self.loginButton.config(text="Create", command=self.createNewUser)
        self.createNewUserButton.config(text="Back",command=self.backFromCreateMenu)
    def backFromCreateMenu(self):
        self.removeLogin()
        self.addLogin() 
    def createNewUser(self):
        if self.checkIfGivenUserExists():
            userID = self.usernameEntry.get()
            password = self.passwordEntry.get()
            userHashString = str(userID)+str(password)
            userHash = hashlib.sha512(userHashString.encode()).hexdigest()
            UserDatabase = open("scripts/UserDatabase.txt", "a")
            UserDatabase.write(userHash)
            UserDatabase.write("\n")
            UserDatabase.close()
            print("Successfully created the User " + userID)
            self.backFromCreateMenu()
        else:
            return
    def nextScreenshot(self):
        if self.currentIndexOfLoadedImage == -1:
            return
        if self.currentIndexOfLoadedImage <= 0 | self.currentIndexOfLoadedImage >= self.currentBlockchain.getHighestIndex():
            return
        self.removeImageDisplay()
        self.addImageDisplay(self.currentIndexOfLoadedImage+1)
    def previousScreenshot(self):
        if self.currentIndexOfLoadedImage == -1:
            self.removeImageDisplay()
            self.addImageDisplay(int(self.currentBlockchain.getLatestBlock().block_Header.index)-1)
            return
        if self.currentIndexOfLoadedImage > 0 and self.currentIndexOfLoadedImage-1 != 0:
            self.removeImageDisplay()
            self.addImageDisplay(self.currentIndexOfLoadedImage-1)
    def refreshGUI(self):
        self.removeInfoPanel()
        self.removeImageDisplay()
        self.addInfoPanel()
        self.addImageDisplay(-1)
    def jumpToBlock(self):
        try:
            blockToJumpTo = int(self.jumpEntry.get())
        except ValueError:
            self.jumpEntry.delete(0, tk.END)
            return
        if(blockToJumpTo > 0 and blockToJumpTo <= self.currentBlockchain.getHighestIndex()):         
            self.removeImageDisplay()
            self.addImageDisplay(blockToJumpTo)
    def checkIfBlockchainIsValid(self):
        if(self.currentBlockchain.checkValidity()):
            messagebox.showinfo(title="Validity check",message="Blockchain is valid based on Hashes")
        else:
            messagebox.showerror(title="Validity check", message="Error Blockchain broke on Block: " + self.currentBlockchain.faultyBlock)
    def jumpInStepSize(self, stepsize):
        if self.currentIndexOfLoadedImage == -1:
            if self.currentBlockchain.getHighestIndex() > stepsize:
                if(self.currentBlockchain.getHighestIndex() + stepsize) > 0 and (self.currentBlockchain.getHighestIndex() + stepsize) <= self.currentBlockchain.getHighestIndex():
                    self.currentIndexOfLoadedImage = self.currentBlockchain.getHighestIndex() + stepsize
                    self.removeImageDisplay()
                    self.addImageDisplay(self.currentIndexOfLoadedImage)
                    return
                else:
                    return
            else:
                return
        if self.currentBlockchain.getHighestIndex() > stepsize:
                if(int(self.currentIndexOfLoadedImage) + stepsize) > 0 and (int(self.currentIndexOfLoadedImage) + stepsize) <= self.currentBlockchain.getHighestIndex():
                    self.currentIndexOfLoadedImage += stepsize
                    self.removeImageDisplay()
                    self.addImageDisplay(self.currentIndexOfLoadedImage)
                else:
                    return
        else:
            return
    #Buttons/Labels add
    def addBlenderAndGifButtons(self):
        self.startBackGifFrame = tk.Frame(self.master)
        self.startBackGifFrame.columnconfigure(2,weight=1)
        self.startBlenderButton = tk.Button(self.startBackGifFrame,height=3, width=14,bg="orange", text="StartBlender", command=lambda:startBlenderAndStartTakingScreenshots(self.currentBlockchain))
        self.createGifFromScreenshotsButton = tk.Button(self.startBackGifFrame, height=3, width=14, text="CreateGif", command=lambda:self.currentBlockchain.loadAllImagesFromBlockchainAndCreateGif(self.currentBlockchainName.strip(".txt")))
        self.checkIfBlockchainIsValidButton = tk.Button(self.startBackGifFrame, height=3, width=14, text="Check Blockchain",command=self.checkIfBlockchainIsValid)
        #self.createGifFromScreenshotsButton = tk.Button(self.startBackGifFrame, height=3, width=14, text="CreateGif", command=self.currentBlockchain.checkValidity)
        self.refreshGuiButton = tk.Button(self.startBackGifFrame, height=3, width=14, text="Refresh", command=self.refreshGUI)
        self.startBackGifFrame.pack(side="bottom",fill="both")
        self.createGifFromScreenshotsButton.grid(column=0,row=0,sticky="w")
        self.checkIfBlockchainIsValidButton.grid(column=1,row=0,sticky="w")
        self.refreshGuiButton.grid(column=3,row=0, sticky="e") 
        self.startBlenderButton.grid(column=4,row=0,sticky="e")
    def addLoadCreateBlockchainButtons(self):
        self.createLoadFrame = tk.Frame(self.master)
        self.createLoadFrame.columnconfigure(1,weight=1)
        self.loadBlockchainButton = tk.Button(self.createLoadFrame, text="Load Blockchain",height=3, width=14, command=self.askForBlockchainFile)
        self.createNewBlockchainButton = tk.Button(self.createLoadFrame, text="Create Blockchain",height=3, width=14, command=self.createNewBlockchainFile)
        self.createLoadFrame.pack(side="bottom", fill="both")
        self.createNewBlockchainButton.grid(column=2,row=0,sticky="e")
        self.loadBlockchainButton.grid(column=0,row=0,sticky="w")
    def addInfoPanel(self):
        self.infoFrame = tk.Frame(self.master)
        self.infoFrame.columnconfigure(index=1, weight=1)
        self.loggedInUserLabel = tk.Label(self.infoFrame, text="User:     " + self.successfullyLoggedInUser)
        self.currentBlockchainLabel = tk.Label(self.infoFrame, text="Blockchain:     " +self.currentBlockchainName)
        self.infoFrame.pack(side="top",fill="both")
        self.loggedInUserLabel.grid(column=2, row=0, sticky="ne")
        self.currentBlockchainLabel.grid(column=2, row=1, sticky="ne")
        if(self.currentBlockchainName != "None"):
            self.backFromActiveBlockchainButton = tk.Button(self.infoFrame, text="Back", command=self.backFromActiveBlockchain, height=3, width=14)
            self.blockCountOfBlockchain = tk.Label(self.infoFrame, text="Blocks:     " +str(self.currentBlockchain.getLatestBlock().block_Header.index))
            self.blockchainSizeInMb = tk.Label(self.infoFrame, text="Blockchain Size:     " + str(os.path.getsize("blockchains/" + self.currentBlockchainName)>>20) + "MB")
            self.backFromActiveBlockchainButton.grid(column=0,row=0,rowspan=4, sticky="nw")
            self.blockCountOfBlockchain.grid(column=2, row=2, sticky="ne")
            self.blockchainSizeInMb.grid(column=2,row=3,sticky="ne")
            topCommandsRef = getTheTop3MostUsedCommandsOfBlockchain(self.currentBlockchainName, int(self.currentBlockchain.getHighestIndex()))
            if(topCommandsRef):
                self.totalOfUniqueCommands = tk.Label(self.infoFrame, text="Total Of Unique Commands:     " + str(getUniqueCommandCountOfBlockchain(self.currentBlockchainName, int(self.currentBlockchain.getHighestIndex()))))
                self.topThreeCommands = tk.Label(self.infoFrame, text="Most used Commands: \n" + str(topCommandsRef[0]).strip("()") + "\n" + str(topCommandsRef[1]).strip("()") + "\n" + str(topCommandsRef[2]).strip("()"))
                self.totalOfUniqueCommands.grid(column=2,row=4,sticky="ne")
                self.topThreeCommands.grid(column=2,row=5,sticky="ne")
        else:
            self.logoffButton = tk.Button(self.infoFrame, text="Logoff", command=self.logOffUser, height=3, width=14)
            self.logoffButton.grid(column=0,row=0, rowspan=4, sticky="nw")
    def addLogin(self):
        self.loginCreateFrame = tk.Frame(self.master,borderwidth=1, relief="solid")
        self.usernameLabel = tk.Label(self.loginCreateFrame, text="Username:")
        self.passwordLabel = tk.Label(self.loginCreateFrame, text="Password:")
        self.usernameEntry = tk.Entry(self.loginCreateFrame)
        self.passwordEntry = tk.Entry(self.loginCreateFrame, show="*")
        self.loginButton = tk.Button(self.master, text="Login", command=self.validateLoginData, height=2,width=5)
        self.createNewUserButton = tk.Button(self.master, text="Create", command=self.createNewUserButtonLogic, height=2,width=5)

        self.usernameLabel.grid(column=0, row=0)
        self.passwordLabel.grid(column=0, row=1)
        self.usernameEntry.grid(column=1,row=0)
        self.passwordEntry.grid(column=1,row=1)
        
        self.loginCreateFrame.grid(column=0, row=0,columnspan=2)
        self.loginButton.grid(column=1, row=1, sticky="e")
        self.createNewUserButton.grid(column=0, row=1, sticky="w")
    def addImageDisplay(self, whatBlock):
        if self.currentBlockchain.getHighestIndex() == 0:
            return
        self.currentIndexOfLoadedImage = whatBlock
        self.imageFrame = tk.Frame(self.master, width=self.master.winfo_width()*0.75, height=self.master.winfo_height()*0.75)
        self.imageFrame.pack_propagate(0)
        self.imageFrame.pack()
        CurrentImage = Image.open(self.currentBlockchain.getBlock(self.currentIndexOfLoadedImage).block_Data.data1).resize((int(self.master.winfo_width()*0.5),int(self.master.winfo_height()*0.5)))
        CurrentImage.save("media/Screenshots/CurrentImage.png")
        CurrentImage.close()
        self.loadedImage = ImageTk.PhotoImage(file="media/Screenshots/CurrentImage.png")
        self.loadedScreenshot = tk.Label(self.imageFrame,image=self.loadedImage)
        blockInfo = "Block: " + str(self.currentBlockchain.getBlock(self.currentIndexOfLoadedImage).block_Header.index) + "     Command: " + self.currentBlockchain.getBlock(self.currentIndexOfLoadedImage).block_Data.data2 + "     Timestamp: " + str(self.currentBlockchain.getBlock(self.currentIndexOfLoadedImage).block_Header.timestamp)
        self.screenshotCommand = tk.Label(self.imageFrame, text=blockInfo)
        self.previousScreenshotButton = tk.Button(self.imageFrame,text="Previous",command=self.previousScreenshot)
        self.nextScreenshotButton = tk.Button(self.imageFrame,text="Next",command=self.nextScreenshot)
        self.jumpToBlockButton = tk.Button(self.imageFrame, text="Jump to Block: ", command=self.jumpToBlock)
        self.jumpNext10Button = tk.Button(self.imageFrame, text="Jump -> 10", command=lambda:self.jumpInStepSize(10))
        self.previous10Button = tk.Button(self.imageFrame, text="Jump <- 10", command=lambda:self.jumpInStepSize(-10))
        self.jumpEntry = tk.Entry(self.imageFrame)
        self.loadedScreenshot.grid(columnspan=3,row=0)
        self.previousScreenshotButton.grid(column=0, row=1, sticky="w")
        self.screenshotCommand.grid(column=1,row=1)
        self.nextScreenshotButton.grid(column=2,row=1,sticky="e")
        self.jumpNext10Button.grid(column=2, row=4, sticky="e")
        self.previous10Button.grid(column=0, row=4, sticky="w")
        self.jumpToBlockButton.grid(column=0, row=3,sticky="sw")
        self.jumpEntry.grid(column=1, row=3,sticky="w")
    #Buttons/Labels remove
    def removeBlenderAndGifButtons(self):
        self.startBackGifFrame.pack_forget()     
    def removeLoadCreateBlockchainButtons(self):
        self.createLoadFrame.pack_forget()
    def removeInfoPanel(self):
        self.infoFrame.pack_forget()
    def removeLogin(self):
        self.loginCreateFrame.grid_forget()
        self.loginButton.grid_forget()
        self.createNewUserButton.grid_forget()
    def removeImageDisplay(self):
        try:
            self.imageFrame.pack_forget()
        except AttributeError:
            pass
    #util
    def checkIfGivenUserExists(self) ->bool:
        userID = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if( not userID or not password):
            return False
        userHashString = str(userID)+str(password)
        userHash = hashlib.sha512(userHashString.encode()).hexdigest()
        
        UserDatabase = open("scripts/UserDatabase.txt")
        UserDatabaseLines = UserDatabase.read().splitlines()
        for entry in UserDatabaseLines:
            if(entry==userHash):
                UserDatabase.close()
                return False
        UserDatabase.close()
        return True
    def updateInfoPanel(self):
        self.blockCountOfBlockchain.config(text="Blocks: \n" +str(self.currentBlockchain.getLatestBlock().block_Header.index))
