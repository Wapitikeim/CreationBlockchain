import base64
from PIL import Image
import io
from collections import Counter

#TODO SORT OUT
def getImageDataBase64FromScreenshotFolder(imageName) -> bytes:
    image = open("media/Screenshots/" + imageName, "rb")
    imageBinarys = image.read()
    imageBinarysEncoded = base64.b64encode(imageBinarys)
    image.close()

    return imageBinarysEncoded

def writeImageDataBase64ToBlockchain(encodedImageData, blockchainName):
    blockchain = open("blockchains/" + blockchainName, "ab")
    blockchain.write(encodedImageData)
    blockchain.close()
    
    blockchain = open("blockchains/" + blockchainName, "a")
    blockchain.write("\n")
    blockchain.close()


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

def writeBytesToBlockchain(bytesToAdd, blockchainName):
    blockchain = open("blockchains/" + blockchainName, "ab")
    encodedBytes = base64.b64encode(bytesToAdd)
    blockchain.write(encodedBytes)
    blockchain.close()
    blockchain = open("blockchains/" + blockchainName, "a")
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
    i = 0
    for line in fileRead:
        i+=1
    """ fileReadStr = fileRead.read().splitlines()
    ref = len(fileReadStr) """
    fileRead.close()
    return i

def getTheTop3MostUsedCommandsOfBlockchain(blockchainName, highestIndex):
    blockchainRead = open("blockchains/"+blockchainName, "r")
    highestIndex = highestIndex*7
    lineNumbers = []
    top3CommandsIncludingTheirCount = []
    if highestIndex != 0:
        i = 6
        while i < highestIndex+7:
            lineNumbers.append(i)
            i+=7
        entrys = []
        for y, line in enumerate(blockchainRead):
            if y in lineNumbers:
                entrys.append(line.strip())
        counts = Counter(entrys)
        #mostFreq, mostFreqCount = counts.most_common(1)[0]
        #print(mostFreq, mostFreqCount) # Meistgenutztes Command
        #print(len(counts.values())) # Soviele unterschiedliche Befehle
        #print(counts.most_common(3)) # Gibt die dritt meist auftretendenden Strings zurück
        try:
            top3CommandsIncludingTheirCount = counts.most_common(3)
        except IndexError:
            pass          
    blockchainRead.close()
    return top3CommandsIncludingTheirCount 

def getUniqueCommandCountOfBlockchain(blockchainName, highestIndex):
    blockchainRead = open("blockchains/"+blockchainName, "r")
    highestIndex = highestIndex*7
    lineNumbers = []
    uniqueCommands = 0
    if highestIndex != 0:
        i = 6
        while i < highestIndex+7:
            lineNumbers.append(i)
            i+=7
        entrys = []
        for y, line in enumerate(blockchainRead):
            if y in lineNumbers:
                entrys.append(line.strip())
        counts = Counter(entrys)
        #mostFreq, mostFreqCount = counts.most_common(1)[0]
        #print(mostFreq, mostFreqCount) # Meistgenutztes Command
        #print(len(counts.values())) # Soviele unterschiedliche Befehle
        #print(counts.most_common(3)) # Gibt die dritt meist auftretendenden Strings zurück
        try:
            uniqueCommands = len(counts.values())
        except IndexError:
            pass          
    blockchainRead.close()
    return uniqueCommands

def getHighestIndexFromBlockchainFile(blockchainName):
    pass
#Examp
#print(readStrFromBlockchain(6, "bchain.txt"))
#writeStrToBlockchain("Pups", "bchain.txt")
#writeImageToBlockchain("test.png", "bchain.txt") 
""" imageFile = Image.open(readImageBytesFromBlockchain(3, "bchain.txt"))
imageFile.save("media/Screenshots/ReadFromFile.png") 
imageFile.close() """ 