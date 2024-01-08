import tkinter as tk

import hashlib


class MainApplication(tk.Frame):
    #Labels
    usernameLabel = tk.Label
    passwordLabel = tk.Label
    #Entrys
    usernameEntry = tk.Entry
    passwordEntry = tk.Entry
    #Buttons
    loginButton = tk.Button


    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.createLoginWindow()
    
    def configure_gui(self):
        self.master.title("Creation Blockchain")
        self.master.geometry("500x500")
    
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
                self.cleanupLogin()
                UserDatabase.close()
                return
        UserDatabase.close()

    def cleanupLogin(self):
        self.usernameLabel.pack_forget()
        self.passwordLabel.pack_forget()
        self.usernameEntry.pack_forget()
        self.passwordEntry.pack_forget()
        self.loginButton.pack_forget()
            