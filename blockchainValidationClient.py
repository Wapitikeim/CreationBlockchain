import socket 
import os 
import hashlib
import time

SEPERATOR = "<SEPERATOR>" 
BUFFER_SIZE = 4096

HOST = "192.168.1.195"
PORT = 5001 

hash = hashlib.sha256()
filename = "blockchains/BlenderGuruDonut.txt"
fileSize = os.path.getsize(filename)
print(fileSize)
fileInputHash = open(filename, "rb")
while True:
    data = fileInputHash.read(BUFFER_SIZE)
    if not data:
        break 
    hash.update(data)
fileInputHash.close()
print("Hash: " + hash.hexdigest())
fileHash = hash.hexdigest()

s = socket.socket()

print(f"[+] Connection to {HOST}:{PORT}")
s.connect((HOST,PORT))
print("[+] Connected.")

s.send(f"{filename}{SEPERATOR}{fileHash}{SEPERATOR}{fileSize}".encode())
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break 
        s.send(bytes_read)
print("Waiting for Response: ")
answer = s.recv(BUFFER_SIZE)
print(answer)
s.close()