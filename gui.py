import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import hashlib
from PIL import ImageTk
import os
from base64 import b64decode
import shutil

from publicKeyUtil import write_Signature_To_File
from publicKeyUtil import get_SHA256_Hash_from_File

from blockchainValidationClient import * 

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
    createSignatureForBlockchainButton = tk.Button
    #-LoadedScreenshot
    refreshGuiButton = tk.Button
    nextScreenshotButton = tk.Button
    previousScreenshotButton = tk.Button
    jumpToBlockButton = tk.Button
    jumpNext10Button = tk.Button
    previous10Button = tk.Button
    
    #BlockchainValidator
    blockchainValdidatorButton = tk.Button
    backFromBlockchainValidatorButton = tk.Button
    blockcainToVerifyButton = tk.Button
    uploadCertificateToServerButton = tk.Button
    pingServerButton = tk.Button
    verifyBlockchainWithPublicKeyButton = tk.Button
    uploadedBlockchainLabel = tk.Label
    uploadedCertificateLabel = tk.Label
    userWhoSignedTheCertificateLabel  = tk.Label
    userWhoSignedTheCertificateEntry  = tk.Entry
    loadedPublicKeyPath = "None"
    loadedPublicKeyPathLabel = tk.Label
    blockchainToVerifyPath = "None"
    blockchainToVerifyLabel = tk.Label

    #Frames
    global loginCreateFrame 
    global createLoadFrame
    global startBackFrame
    global infoFrame
    global imageFrame
    global validationServerFrame

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
        if not os.access("scripts/blenderStart.bat", os.R_OK):
            self.checkOnBlenderStartBat()
         
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
    def checkOnBlenderStartBat(self):
        messagebox.showinfo(title="Blender Path", message="Please set the folder to where your Blender installation is located. \n Normally found under \"C:/ProgrammFiles/BlenderFoundation\"")
        filePath = filedialog.askdirectory(initialdir="C:/Program Files/Blender Foundation/")
        if not filePath:
            messagebox.showerror(message="Please enter a valid FilePath!")
            raise Exception("Please enter a valid FilePath!") 
        if not os.access(f"{filePath}/blender.exe", os.R_OK):
            messagebox.showerror(message="This is not a valid folder. Could not find blender.exe")
            raise Exception("This is not a valid folder. Could not find blender.exe")
        batCreator = open("scripts/blenderStart.bat", "w")
        batCreator.write("@echo off \n")
        if filePath[0] != "C":
            batCreator.write(f"{filePath[0]}:\n")
        batCreator.write(f"cd {filePath}/ \n")
        workingDic = os.path.abspath(os.getcwd())
        batCreator.write(f"blender --log \"*operator*\" --log-file \"{workingDic}/scripts/Log.txt\" --log-level 1 --python-use-system-env --python \"{workingDic}/scripts/blenderControl.py\" \n")
        batCreator.close()

        #Adjust blenderControl.py
        fin = open("scripts/blenderControlRef.py")
        fout = open("scripts/blenderControl.py", "w")
        for line in fin:
            fout.write(line.replace("INSERTPATH",os.path.abspath(os.getcwd()).replace("\\", "/")))
        fin.close()
        fout.close()

    #Button Logic
    def validateLoginData(self):
        userID = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if( not userID or not password):
            return

        userHashString = str(userID)+str(password)
        userHash = hashlib.sha512(userHashString.encode()).hexdigest()
        if not os.access("scripts/UserDatabase.txt", os.R_OK):
            print("Userbase not found - creating")
            createUserDB = open("scripts/UserDatabase.txt", "w")
            createUserDB.close()
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
        filePath = filedialog.askopenfilename(initialdir=f"{os.path.abspath(os.getcwd())}/blockchains/")
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
        self.addImageDisplay(-1)
        #self.addBackFromActiveBlockchainButton()
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
        if not os.access("scripts/UserDatabase.txt", os.R_OK):
            print("Userbase not found - creating")
            createUserDB = open("scripts/UserDatabase.txt", "w")
            createUserDB.close()
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
    #Validation Server
    def pingServer(self):
        client = blockchainClient()
        if client.ping_Server():
            messagebox.showinfo(message="Server active")
        else:
            messagebox.showerror(message="Can't reach Server")
    def uploadPublicKeyToServer(self):
        client = blockchainClient()
        if not client.ping_Server():
            messagebox.showerror(message="Cannot reach Server")
            return
        if not client.check_if_file_exists_on_server('keys/'+self.successfullyLoggedInUser+'Public.pem'):
            client.upload_key_File('keys/'+self.successfullyLoggedInUser+'Public.pem')
            messagebox.showinfo(message="Public key succsessfully uploaded")
        else:
            messagebox.showinfo(message="Public key already uploaded")
    def getPublicKeyFromServer(self):
        filePath = filedialog.askopenfilename(initialdir=f"{os.path.abspath(os.getcwd())}/blockchains/")
        if not filePath:
            return
        reader = open(filePath, "r")
        lines = reader.read().splitlines()
        hash = lines[2]
        reader.close()
        client = blockchainClient()
        if not client.ping_Server():
            messagebox.showerror(message="Cannot reach Server")
            return
        answer = client.get_Public_Key_From_Server(hash)
        if answer == "Error":
            messagebox.showerror(message=f"Error couldnt find corresponding Public Key to {os.path.basename(filePath)} on Server")
        else:
            self.loadedPublicKeyPath = answer
            self.blockchainToVerifyPath = filePath
            messagebox.showinfo(message=f"Successfully loaded Public key to corresponding Blockchain {os.path.basename(filePath)} from Server")
        self.removeValidationServer()
        self.addValidationServer()
    def validateBlockchainWithPublicKey(self):
        if self.loadedPublicKeyPath == "None":
            messagebox.showinfo(message="Please ask the server for a Public Key first")
            return
        publicKey = load_public_key_with_filepath(self.loadedPublicKeyPath)
        blockchainToLoad = open(self.blockchainToVerifyPath, "r")
        lines = blockchainToLoad.read().splitlines()
        max = len(lines)-1
        x = 2
        y = 3
        while(x < max):
            if not check_if_signature_matches_message(lines[x].encode(),publicKey,base64.b64decode(lines[y])):
                self.loadedPublicKeyPath = "None"
                messagebox.showerror(message=f"The Blockchain {os.path.basename(self.blockchainToVerifyPath)} is faulty beginning at block {lines[x-2]}")
                self.blockchainToVerifyPath = "None"
                blockchainToLoad.close()
                shutil.rmtree("tmp/")
                os.mkdir("tmp/")
                return
            print(f"Signature for Block {lines[x-2]} valid")
            x +=7
            y +=7
        self.loadedPublicKeyPath = "None"
        messagebox.showinfo(message=f"Success! The Blockchain {os.path.basename(self.blockchainToVerifyPath)} is valid")
        self.blockchainToVerifyPath = "None"
        blockchainToLoad.close()
        shutil.rmtree("tmp/")
        os.mkdir("tmp/")
        
        blockchainToLoad.close()
        
        self.removeValidationServer()
        self.addValidationServer()
    
    #Buttons/Labels add
    def addBlenderAndGifButtons(self):
        self.startBackGifFrame = tk.Frame(self.master)
        self.startBackGifFrame.columnconfigure(2,weight=1)
        self.startBlenderButton = tk.Button(self.startBackGifFrame,height=3, width=14,bg="orange", text="StartBlender", command=lambda:startBlenderAndStartTakingScreenshots(self.currentBlockchain))
        self.createGifFromScreenshotsButton = tk.Button(self.startBackGifFrame, height=3, width=14, text="CreateGif", command=lambda:self.currentBlockchain.loadAllImagesFromBlockchainAndCreateGif(self.currentBlockchainName.strip(".txt")))
        self.checkIfBlockchainIsValidButton = tk.Button(self.startBackGifFrame, height=3, width=14, text="Check Blockchain",command=self.checkIfBlockchainIsValid)
        self.createSignatureForBlockchainButton = tk.Button(self.startBackGifFrame, height=3, width=14, text="Register Key", command=self.uploadPublicKeyToServer)
        self.refreshGuiButton = tk.Button(self.startBackGifFrame, height=3, width=14, text="Refresh", command=self.refreshGUI)
        self.startBackGifFrame.pack(side="bottom",fill="both")
        self.createGifFromScreenshotsButton.grid(column=0,row=1,sticky="w")
        self.checkIfBlockchainIsValidButton.grid(column=1,row=1,sticky="w")
        self.createSignatureForBlockchainButton.grid(column=0,row=0,sticky="w")
        self.refreshGuiButton.grid(column=3,row=1, sticky="e") 
        self.startBlenderButton.grid(column=4,row=1,sticky="e")
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
        self.blockchainValdidatorButton = tk.Button(self.master,text="Validation Server",height=2,width=13, command=lambda:[self.removeLogin(), self.addValidationServer()])
        self.usernameLabel.grid(column=0, row=0)
        self.passwordLabel.grid(column=0, row=1)
        self.usernameEntry.grid(column=1,row=0)
        self.passwordEntry.grid(column=1,row=1)
        
        
        self.loginCreateFrame.grid(column=0, row=0,columnspan=2)
        self.loginButton.grid(column=1, row=1, sticky="e")
        self.createNewUserButton.grid(column=0, row=1, sticky="w")
        self.blockchainValdidatorButton.grid(column=3,row=0)
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
    def addValidationServer(self):
        self.validationServerFrame = tk.Frame(self.master,width=self.master.winfo_width(), height=self.master.winfo_height())
        #self.validationServerFrame.columnconfigure(1, weight=1)
        self.validationServerFrame.rowconfigure(2, weight=1)
        self.backFromBlockchainValidatorButton = tk.Button(self.validationServerFrame,text="Back", command=lambda:(self.removeValidationServer(), self.addLogin()))
        self.blockcainToVerifyButton = tk.Button(self.validationServerFrame, text="Enter Blockchain To verify", command=self.getPublicKeyFromServer)
        #self.uploadCertificateToServerButton = tk.Button(self.validationServerFrame, text="Upload Certificate", command=self.uploadCertificateToServer)
        self.pingServerButton = tk.Button(self.validationServerFrame, text="Ping Server", command=self.pingServer)
        self.blockchainToVerifyLabel = tk.Label(self.validationServerFrame, text=os.path.basename(self.blockchainToVerifyPath))
        self.loadedPublicKeyPathLabel = tk.Label(self.validationServerFrame, text=os.path.basename(self.loadedPublicKeyPath))
        #self.uploadedBlockchainLabel = tk.Label(self.validationServerFrame, text="None")
        #self.uploadedCertificateLabel = tk.Label(self.validationServerFrame, text="None")
        #self.userWhoSignedTheCertificateLabel = tk.Label(self.validationServerFrame, text="Enter User")
        #self.userWhoSignedTheCertificateEntry = tk.Entry(self.validationServerFrame)
        self.verifyBlockchainWithPublicKeyButton = tk.Button(self.validationServerFrame, text="Validate", command=self.validateBlockchainWithPublicKey)
        self.validationServerFrame.pack(side="left",fill="both")
        self.blockcainToVerifyButton.grid(column=0, row=0)
        #self.uploadedBlockchainLabel.grid(column=1, row=0)
        #self.uploadCertificateToServerButton.grid(column=0, row=1)
        #self.uploadedCertificateLabel.grid(column=1, row=1)
        #self.userWhoSignedTheCertificateLabel.grid(column=0, row=2)
        #self.userWhoSignedTheCertificateEntry.grid(column=1, row=2)
        self.backFromBlockchainValidatorButton.grid(column=0, row=4, sticky="w")
        self.verifyBlockchainWithPublicKeyButton.grid(column=2, row=4, sticky="e")
        self.pingServerButton.grid(column=1, row=4, sticky="e")
        self.blockchainToVerifyLabel.grid(column=0, row=1, sticky="w")
        self.loadedPublicKeyPathLabel.grid(column=0, row=2, sticky="w")

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
        self.blockchainValdidatorButton.grid_forget()
    def removeImageDisplay(self):
        try:
            self.imageFrame.pack_forget()
        except AttributeError:
            pass
    def removeValidationServer(self):
        self.validationServerFrame.pack_forget()
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

    #old
    """ def uploadBlockchainToServer(self):
        filePath = filedialog.askopenfilename()
        if not filePath:
            return
        fileName = os.path.basename(filePath)
        if fileName[-4:] != ".txt":
            messagebox.showerror(message="This cant be an valid Blockchain haven't found .txt")
            return
        client = blockchainClient()
        try:
            client.upload_File(filePath)
        except Exception:
            return 
        self.uploadedBlockchainLabel.config(text=fileName)    
    def uploadCertificateToServer(self):
        filePath = filedialog.askopenfilename()
        if not filePath:
            return
        fileName = os.path.basename(filePath)
        if fileName[-5:] != ".cert":
            messagebox.showerror(message="This cant be an valid Certificate haven't found .cert")
            return
        client = blockchainClient()
        try:
            client.upload_File(filePath)
        except Exception:
            return 
        self.uploadedCertificateLabel.config(text=fileName)  
    def uploadKeyFileFromCurrentUser(self):
        client = blockchainClient()
        if client.check_if_file_exists_on_server('keys/' + self.successfullyLoggedInUser +'Public.pem'):
            return
        client.upload_key_File('keys/' + self.successfullyLoggedInUser +'Public.pem')
    def validateBlockchainWithCertificate(self):
        if self.uploadedBlockchainLabel['text'] == "None":
            messagebox.showinfo(message="Please upload a Blockchain first")
            return
        if self.uploadedCertificateLabel['text'] == "None":
            messagebox.showinfo(message="Please upload a Certificate first")
            return
        if not self.userWhoSignedTheCertificateEntry.get():
            messagebox.showinfo(message="Please enter the User who signed the Certificate")
            return
        client = blockchainClient()
        response = client.check_If_Blockchain_is_valid_for_user(self.userWhoSignedTheCertificateEntry.get(), 'blockchains/'+self.uploadedBlockchainLabel['text'])
        if response.strip("b''") == 'True':
            messagebox.showinfo(message="Certificate for " + self.uploadedBlockchainLabel['text'] + " is Valid")
            self.uploadedCertificateLabel['text'] = "None"
            self.uploadedBlockchainLabel['text'] = "None"
        else:
            messagebox.showinfo(message=response)
    """