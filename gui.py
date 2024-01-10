import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import hashlib

import os

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
    #Entrys
    usernameEntry = tk.Entry
    passwordEntry = tk.Entry
    #Buttons
    loginButton = tk.Button
    startBlenderButton = tk.Button
    createGifFromScreenshotsButton = tk.Button
    backFromActiveBlockchainButton = tk.Button

    loadBlockchainButton = tk.Button
    createNewBlockchainButton = tk.Button

    #UserData
    successfullyLoggedInUser = ""
    currentBlockchainName = "None"
    currentBlockchain = ""

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.addLogin()
    
    #Setup
    def configure_gui(self):
        self.master.title("Creation Blockchain")
        self.master.geometry("500x500")
    def createUIAfterLogin(self):
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
                self.successfullyLoggedInUser = userHash
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
        self.currentBlockchain = Blockchain(self.successfullyLoggedInUser, self.currentBlockchainName, True)
        if(self.currentBlockchain.allowedToModify == False):
            self.currentBlockchainName = "None"
            self.currentBlockchain = ""
            return
        self.removeInfoPanel()
        self.addInfoPanel()
        self.removeLoadCreateBlockchainButtons()
        self.addBlenderAndGifButtons()
        self.addBackFromActiveBlockchainButton()
    def createNewBlockchainFile(self):
        newBlockchainName = simpledialog.askstring("Create Blockchain", "Please enter a Name for the Blockchain")
        if not newBlockchainName:
            return 
        if newBlockchainName[-4:] != ".txt":
            newBlockchainName = newBlockchainName + ".txt"
        self.currentBlockchainName = newBlockchainName
        self.currentBlockchain = Blockchain(self.successfullyLoggedInUser, self.currentBlockchainName, False)

        self.removeInfoPanel()
        self.addInfoPanel()
        self.removeLoadCreateBlockchainButtons()
        self.addBlenderAndGifButtons()
        self.addBackFromActiveBlockchainButton()
    def backFromActiveBlockchain(self):
        self.currentBlockchain = ""
        self.currentBlockchainName = "None"
        
        self.removeBackFromActiveBlockchainButton()
        self.removeBlenderAndGifButtons()
        self.removeInfoPanel()
        self.addInfoPanel()
        self.addLoadCreateBlockchainButtons()

    #Buttons/Labels add
    def addLogin(self):
        self.usernameLabel = tk.Label(self.master, text="Username:")
        self.passwordLabel = tk.Label(self.master, text="Password:")
        self.usernameEntry = tk.Entry(self.master)
        self.passwordEntry = tk.Entry(self.master, show="*")
        self.loginButton = tk.Button(self.master, text="Login", command=self.validateLoginData)

        self.usernameLabel.pack(side="top", anchor="nw")
        self.usernameEntry.pack(side="left", anchor="nw")
        self.passwordLabel.pack(side="top",anchor="nw")
        self.passwordEntry.pack(side="left", anchor="nw")
        self.loginButton.pack()
    def addBlenderAndGifButtons(self):
        self.startBlenderButton = tk.Button(self.master, text="StartBlender", command=lambda:startBlenderAndStartTakingScreenshots(self.currentBlockchain), height=3, width=12, bg="orange")
        self.startBlenderButton.pack(side="bottom", anchor="se", expand=False)
        self.createGifFromScreenshotsButton = tk.Button(self.master, text="CreateGif", command=lambda:self.currentBlockchain.loadAllImagesFromBlockchainAndCreateGif(), height=3, width=12)
        self.createGifFromScreenshotsButton.pack(side="bottom", anchor="se", expand=False) 
    def addLoadCreateBlockchainButtons(self):
        self.loadBlockchainButton = tk.Button(self.master, text="Load Blockchain",height=3, width=12, command=self.askForBlockchainFile)
        self.loadBlockchainButton.pack(side="bottom", anchor="sw", expand=False)
        self.createNewBlockchainButton = tk.Button(self.master, text="Create Blockchain",height=3, width=12, command=self.createNewBlockchainFile)
        self.createNewBlockchainButton.pack(side="bottom", anchor="sw", expand=False)
    def addInfoPanel(self):
        trimmedLoggedInUserStr = self.successfullyLoggedInUser[0] + self.successfullyLoggedInUser[1] + self.successfullyLoggedInUser[2] + self.successfullyLoggedInUser[3]
        self.loggedInUserLabel = tk.Label(self.master, text="User: \n" + trimmedLoggedInUserStr)
        self.loggedInUserLabel.pack(side="top", anchor="ne")
        self.currentBlockchainLabel = tk.Label(self.master, text="Blockchain: \n" +self.currentBlockchainName)
        self.currentBlockchainLabel.pack(side="top", anchor="ne")
        """ if (self.currentBlockchainName != "None"):
            self.blockCountOfBlockchain = tk.Label(self.master, text="Blockcount: \n" + str(self.currentBlockchain.getHighestIndex()+1))
            self.blockCountOfBlockchain.pack(side="top", anchor="ne") """
    def addBackFromActiveBlockchainButton(self):
        self.backFromActiveBlockchainButton = tk.Button(self.master, text="Back", command=self.backFromActiveBlockchain, height=3, width=12)
        self.backFromActiveBlockchainButton.pack(side="bottom", anchor="se", expand=False)
    #Buttons/Labels remove
    def removeBlenderAndGifButtons(self):
        self.startBlenderButton.forget()
        self.createGifFromScreenshotsButton.forget()     
    def removeLoadCreateBlockchainButtons(self):
        self.loadBlockchainButton.forget()
        self.createNewBlockchainButton.forget()
    def removeInfoPanel(self):
        self.loggedInUserLabel.forget()
        self.currentBlockchainLabel.forget()
        """ if self.blockCountOfBlockchain.winfo_ismapped(self):
            self.blockCountOfBlockchain.forget() """
    def removeBackFromActiveBlockchainButton(self):
        self.backFromActiveBlockchainButton.forget()
    def removeLogin(self):
        self.usernameLabel.pack_forget()
        self.passwordLabel.pack_forget()
        self.usernameEntry.pack_forget()
        self.passwordEntry.pack_forget()
        self.loginButton.pack_forget()