import socket 
import os 
import hashlib
import select

def getHashOfFile(filename):
    hash = hashlib.sha256()
    fileInputHash = open(filename, "rb")
    while True:
        data = fileInputHash.read(BUFFER_SIZE)
        if not data:
            break 
        hash.update(data)
    return hash.hexdigest()

SERVER_HOST = "0.0.0.0" # 0..0 means all local ip adresses
SERVER_PORT = 5001
SERVER_MAX_CONNECTIONS = 5

BUFFER_SIZE = 4096
SEPERATOR = "<SEPERATOR>"

class validationServer:
    global server_Socket

    def __init__(self) -> None:
        self.server_Socket = socket.socket()
        
    def run(self):
        self.server_Socket.bind((SERVER_HOST,SERVER_PORT))
        self.server_Socket.listen(SERVER_MAX_CONNECTIONS)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        try:
            while True:
                self.__handle_Connections()
        except KeyboardInterrupt:
            pass

    def stop(self):
        self.server_Socket.close()

    def __handle_Connections(self):
        client_socket, client_address = self.server_Socket.accept()
        print(f"[+] {client_address} is connected.")
        self.__choose_Options(client_socket)

    def __choose_Options(self, client_socket):
        if not client_socket:
            return 
        recevied_Option = client_socket.recv(BUFFER_SIZE).decode()
        recevied_Option = str(recevied_Option)
        match recevied_Option:
            case "Upload File":
                print("Upload File option recevied")
                client_socket.send("OK".encode())
                self.__upload_File(client_socket)
            case "Ping":
                print("Server ping recevied")
                client_socket.send("OK".encode())
                client_socket.close()
            case "FileCheck":
                print("FileCheck option recevied")
                client_socket.send("OK".encode())
                self.__check_if_File_is_On_Server(client_socket)
            case _:
                print("Error no valid Option")
                client_socket.send("ERROR".encode())
                client_socket.close()

    def __upload_File(self, client_socket):
        receviedFileInfos = client_socket.recv(BUFFER_SIZE).decode()
        filename,fileHash,fileSize = receviedFileInfos.split(SEPERATOR)
        filename = os.path.basename(filename)
        fileCreation = open(filename, "wb")
        fileCreation.close()
        while os.path.getsize(filename) < int(fileSize):
            fileAppend = open(filename, "ab")
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            fileAppend.write(bytes_read)
            fileAppend.close()
        hash = hashlib.sha256()
        fileInputHash = open(filename, "rb")
        while True:
            data = fileInputHash.read(BUFFER_SIZE)
            if not data:
                break 
            hash.update(data)
        fileInputHash.close()
        print("Recived Hash: " + fileHash)
        print("Hash: " + hash.hexdigest())
        if(fileHash == hash.hexdigest()):
            client_socket.send("True".encode())
        else:
            client_socket.send("False".encode())
        client_socket.close()

    def __check_if_File_is_On_Server(self, client_socket):
        receviedFileInfos = client_socket.recv(BUFFER_SIZE).decode()
        receviedFileInfos = str(receviedFileInfos)
        print(os.path.exists(receviedFileInfos))
        if os.path.exists(receviedFileInfos):
            client_socket.send("True".encode())
        else:
            client_socket.send("False".encode())
        client_socket.close()

server = validationServer()
server.run()
