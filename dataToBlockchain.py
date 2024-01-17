import base64
from PIL import Image
import io

def writeImageToBlockchain(imageName, blockchainName):
    image = open("media/Screenshots/" + imageName, "rb")
    imageBinarys = image.read()
    imageBinarysEncoded = base64.b64encode(imageBinarys)
    image.close()
    
    blockchain = open("blockchains/" + blockchainName, "ab")
    blockchain.write(imageBinarysEncoded)
    blockchain.close()
    
    blockchain = open("blockchains/" + blockchainName, "a")
    blockchain.write("\n")
    blockchain.close()

def writeStrToBlockchain(strToAdd, blockchainName):
    blockchain = open("blockchains/" + blockchainName, "a")
    blockchain.write(strToAdd)
    blockchain.write("\n")
    blockchain.close()

def readImageBytesFromBlockchain(index, blockchainName) ->bytes:
    blockchainRead = open("blockchains/"+blockchainName, "rb")
    blockchainBytes = blockchainRead.read().splitlines()
    pngBytes = base64.b64decode(blockchainBytes[index])
    blockchainRead.close()

    imageStream = io.BytesIO(pngBytes) 
    return imageStream

def readStrFromBlockchain(index, blockchainName) ->str:
    blockchainRead = open("blockchains/"+blockchainName, "r")
    #Just Read Specific line? 
    blockchainStr = blockchainRead.read().splitlines()
    blockchainRead.close()

    return blockchainStr[index]

def returnLineCountOfBlockchain(blockchainName) ->int:
    blockchainRead = open("blockchains/"+blockchainName, "r") 
    blockchainStr = blockchainRead.read().splitlines()
    ref = len(blockchainStr)
    blockchainRead.close()
    return ref

def getLineCountOFFile(fileName) ->int:
    fileRead = open(fileName, "r") 
    fileReadStr = fileRead.read().splitlines()
    ref = len(fileReadStr)
    fileRead.close()
    return ref



#Examp
#print(readStrFromBlockchain(6, "bchain.txt"))
#writeStrToBlockchain("Pups", "bchain.txt")
#writeImageToBlockchain("test.png", "bchain.txt") 
""" imageFile = Image.open(readImageBytesFromBlockchain(3, "bchain.txt"))
imageFile.save("media/Screenshots/ReadFromFile.png") 
imageFile.close() """ 