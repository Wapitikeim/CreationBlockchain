import tkinter as tk
import hashlib

from pdc import startBlenderAndStartTakingScreenshots
from pngTogif import createGifFromScreenshotsInFolder


class MainApplication(tk.Frame):
    #Labels
    usernameLabel = tk.Label
    passwordLabel = tk.Label
    loggedInUserLabel = tk.Label
    currentBlockchainLabel = tk.Label
    #Entrys
    usernameEntry = tk.Entry
    passwordEntry = tk.Entry
    #Buttons
    loginButton = tk.Button
    startBlenderButton = tk.Button
    createGifFromScreenshotsButton = tk.Button

    loadBlockchainButton = tk.Button
    createNewBlockchainButton = tk.Button

    #UserData
    successfullyLoggedInUser = ""
    currentBlockchain = "None"

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.createLoginWindow()
    
    def configure_gui(self):
        self.master.title("Creation Blockchain")
        self.master.geometry("500x500")
    
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
                self.cleanupLogin()
                UserDatabase.close()
                self.createUIAfterLogin()
                return
        UserDatabase.close()

    def cleanupLogin(self):
        self.usernameLabel.pack_forget()
        self.passwordLabel.pack_forget()
        self.usernameEntry.pack_forget()
        self.passwordEntry.pack_forget()
        self.loginButton.pack_forget()
    
    def createLoginWindow(self):
        self.usernameLabel = tk.Label(self.master, text="Username:")
        self.passwordLabel = tk.Label(self.master, text="Password:")
        self.usernameEntry = tk.Entry(self.master)
        self.passwordEntry = tk.Entry(self.master, show="*")
        self.loginButton = tk.Button(self.master, text="Login", command=self.validateLoginData)

        self.usernameLabel.pack()
        self.passwordLabel.pack()
        self.usernameEntry.pack()
        self.passwordEntry.pack()
        self.loginButton.pack()

    def createUIAfterLogin(self):
        trimmedLoggedInUserStr = self.successfullyLoggedInUser[0] + self.successfullyLoggedInUser[1] + self.successfullyLoggedInUser[2] + self.successfullyLoggedInUser[3]
        self.loggedInUserLabel = tk.Label(self.master, text="User: \n" + trimmedLoggedInUserStr)
        self.loggedInUserLabel.pack(side="top", anchor="ne")
        #self.loggedInUserLabel.grid(row=4, column=0)
        self.currentBlockchainLabel = tk.Label(self.master, text="Blockchain: \n" +self.currentBlockchain)
        #self.currentBlockchainLabel.grid(row=4, column=0)
        self.currentBlockchainLabel.pack(side="top", anchor="ne")
        
        self.startBlenderButton = tk.Button(self.master, text="StartBlender", command=startBlenderAndStartTakingScreenshots, height=3, width=12, bg="orange")
        self.startBlenderButton.pack(side="bottom", anchor="se", expand=False)
        #self.startBlenderButton.grid(row=4, column=4)
        self.createGifFromScreenshotsButton = tk.Button(self.master, text="CreateGif", command=createGifFromScreenshotsInFolder, height=3, width=12)
        #self.createGifFromScreenshotsButton.grid(row=4, column=4)
        self.createGifFromScreenshotsButton.pack(side="bottom", anchor="se", expand=False)

        self.loadBlockchainButton = tk.Button(self.master, text="Load Blockchain",height=3, width=12)
        #self.loadBlockchainButton.grid(row=0, column=4)
        self.loadBlockchainButton.pack(side="bottom", anchor="sw", expand=False)
        self.createNewBlockchainButton = tk.Button(self.master, text="Create Blockchain",height=3, width=12)
        self.createNewBlockchainButton.pack(side="bottom", anchor="sw", expand=False)

        
