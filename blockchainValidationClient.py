import socket 
import os 
import hashlib
from publicKeyUtil import *
from cryptography.hazmat.primitives import serialization  

SEPERATOR = "<SEPERATOR>" 
BUFFER_SIZE = 4096

HOST = "192.168.1.195"
PORT = 5001 

class blockchainClient():
    global client 
    def __start_Connection(self):
        self.client = socket.socket()
        try:
            self.client.connect((HOST,PORT))
            return True
        except Exception as e:
            print("Server unreachable "+ str(HOST) + " " + str(PORT))
            print(e)
            return False 
    
    def upload_File(self, file_Name):
        if self.__start_Connection():
            pass
        else:
            return
        self.client.send("Upload File".encode())
        response = self.client.recv(BUFFER_SIZE)
        if response == b"OK":
            self.__upload_File_Process(file_Name)
            self.client.close()
        else:
            print("Something went wrong server responded with " + str(response))
            self.client.close()

    def upload_key_File(self, file_Name):
        if self.__start_Connection():
            pass
        else:
            return
        self.client.send("Upload Key File".encode())
        response = self.client.recv(BUFFER_SIZE)
        if response == b"OK":
            self.__upload_File_Process(file_Name)
            self.client.close()
        else:
            print("Something went wrong server responded with " + str(response))
            self.client.close()
    
    def __upload_File_Process(self, file_Name):
        hash = hashlib.sha256()
        filename = file_Name
        fileSize = os.path.getsize(filename)
        #print(fileSize)
        fileInputHash = open(filename, "rb")
        while True:
            data = fileInputHash.read(BUFFER_SIZE)
            if not data:
                break 
            hash.update(data)
        fileInputHash.close()
        #print("Hash: " + hash.hexdigest())
        fileHash = hash.hexdigest()
        self.client.send(f"{filename}{SEPERATOR}{fileHash}{SEPERATOR}{fileSize}".encode())
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break 
                self.client.send(bytes_read)
        #print("Waiting for Response: ")
        answer = self.client.recv(BUFFER_SIZE)
        if answer == b"True":
            print("Upload of " + file_Name + " complete.")
        else:
            print("Upload of " + file_Name + " failed.")
            print("Server Response: " + str(answer))

    def ping_Server(self) ->bool:
        if self.__start_Connection():
            pass
        else:
            return
        self.client.send("Ping".encode())
        response = self.client.recv(BUFFER_SIZE)
        
        if response == b"OK":
            print("Server ping successfull")
            self.client.close()
            return True
        else:
            print("Something is wrong with the Server")
            self.client.close()
            return False
        return False 

    def check_if_file_exists_on_server(self, file_Name)->bool:
        if self.__start_Connection():
            pass
        else:
            return
        self.client.send("FileCheck".encode())
        response = self.client.recv(BUFFER_SIZE)
        if response == b"OK":
            answer = self.__file_check_process(file_Name)
            self.client.close()
            return answer
        else:
            print("Something went wrong server responded with " + str(response))
            return False
            self.client.close()

    def __file_check_process(self, file_Name):
        self.client.send(file_Name.encode())
        response = self.client.recv(BUFFER_SIZE)
        if response == b"True":
            return True
        else:
            return False 

    def check_If_Blockchain_is_valid_for_user(self, username, blockchainName):
        if self.__start_Connection():
            pass
        else:
            return
        self.client.send("Check Blockchain Signature".encode())
        response = self.client.recv(BUFFER_SIZE)
        if response == b"OK":
            self.__check_If_Blockchain_is_valid_for_user_process(username, blockchainName)
            self.client.close()
        else:
            print("Something went wrong server responded with " + str(response))
            self.client.close()          

    def __check_If_Blockchain_is_valid_for_user_process(self, username, blockchainName):
        blockchainHash = hashlib.sha256()
        fileInputHash = open(blockchainName, "rb")
        while True:
            data = fileInputHash.read(BUFFER_SIZE)
            if not data:
                break 
            blockchainHash.update(data)
        fileInputHash.close()
        message = blockchainHash.hexdigest().encode()
        signature = create_signature_for_message(message, load_private_key(username))
        self.client.send(f"{blockchainName}{SEPERATOR}{username}".encode())
        self.client.send(signature)
        answer = self.client.recv(BUFFER_SIZE)
        if answer == b"True":
            print(f"Signature of {blockchainName} from User {username} valid")
            return True
        else:
            print(answer)
            return False

#clientForTesting = blockchainClient()
#create_Key_Pair_and_write_to_file("Alice")
#clientForTesting.upload_File("blockchains/Test.txt")
#clientForTesting.upload_key_File("keys/AlicePublic.pem")
#clientForTesting.check_If_Blockchain_is_valid_for_user("Alice", "blockchains/BlenderGuruDonut.txt")

#print(clientForTesting.check_if_file_exists_on_server("Test.txt"))