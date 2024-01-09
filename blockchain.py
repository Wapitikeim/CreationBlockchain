import hashlib
import io 
import hmac
import datetime

from dataToBlockchain import * 

from pngTogif import createGifFromScreenshotsGiven

class Block:
    #MercleRoot? (permissionedBlockchain?)
    def __init__(self, index, timestamp, data, prevHash):
        self.index = index 
        self.timestamp = timestamp
        self.data = data
        self.prevHash = prevHash

        self.hash = self.calcHash()
    
    def calcHash(self):
        hashStr = str(self.index) + str(self.timestamp) + str(self.data) + str(self.prevHash)
        return hashlib.sha256(hashStr.encode()).hexdigest()
    
#Permissioned = nur der Private Key Owner darf Blöcke Hinzufügen
#-> Was ist wenn der Ursprungsblock etwas enthält das nur der Owner entschlüsseln kann?
#Was ist mit den Mercle Trees
#Wo speichere ich diese Blockchain ? Bzw. wo lade Ich eine bereits erstellte?
class Blockchain:
    name = ""
    allowedToModify = True
    
    def __init__(self, user, blockChainName, loadFlag):
        if loadFlag == False:
            self.createNewBlockchain(user,blockChainName)
        else:
            self.owner = user
            self.name = blockChainName 
            self.blocks = [self.loadFirstBlockFromFile(0)]
            if (self.getLatestBlock().prevHash != user):
                print("User isnt allowed to modify the " + blockChainName + " Blockchain")
                self.allowedToModify = False
            else: 
                if not self.checkIfLineCountOfBlockchainIsRight():
                    print("Something isnt right with the Linecount of " + self.name)
                    self.allowedToModify = False
                else:
                    self.loadRemaingBlocks()

    def createNewBlockchain(self, user, blockChainName):
        self.owner = user
        self.name = blockChainName
        self.blocks = [self.createBlockZero()]
        self.writeFirstBlockToFile()
        print("Successfully created the Blockchain: " +blockChainName)

    def createBlockZero(self) -> Block:
        return Block(0, datetime.datetime.now(), self.name, self.owner)

    def getLatestBlock(self) -> Block:
        return self.blocks[-1]

    def addNewBlockForScreenshots(self, newBlock):
        #Data at this point is ImageName Prev Hash isnt calculated yet UGLY
        self.writeNormalLastBlockToFile(newBlock)
        dataLocation = returnLineCountOfBlockchain(self.name)-1
        newBlock.data = readImageBytesFromBlockchain(dataLocation, self.name)
        newBlock.prevHash = self.getLatestBlock().hash
        newBlock.hash = newBlock.calcHash()
        writeStrToBlockchain(str(newBlock.hash), self.name)
        self.blocks.append(newBlock)

        print("Added Block " + str(newBlock.index) + " On Blockchain: " +self.name)

    def addNewBlock(self, newBlock):
        print("Loaded Block " + str(newBlock.index) + " on " + self.name)
        self.blocks.append(newBlock)

    def loadFirstBlockFromFile(self, index):
        #Missing out of Range Error Handeling
        indexRef = readStrFromBlockchain(index, self.name) 
        timestampRef = readStrFromBlockchain(index+1, self.name)
        dataRef = readStrFromBlockchain(index+2, self.name)
        prevHashRef = readStrFromBlockchain(index+3, self.name)
        blockRef = Block(indexRef,timestampRef, dataRef, prevHashRef)
        return blockRef
    
    def loadBlockFromFile(self, index):
        #Missing out of Range Error Handeling
        indexRef = readStrFromBlockchain(index, self.name) 
        timestampRef = readStrFromBlockchain(index+1, self.name)
        dataRef = readImageBytesFromBlockchain(index+2, self.name)
        prevHashRef = readStrFromBlockchain(index+3, self.name)
        blockRef = Block(indexRef,timestampRef, dataRef, prevHashRef)
        return blockRef

    def loadRemaingBlocks(self):
        lineCount = returnLineCountOfBlockchain(self.name)
        if(lineCount>4):
            i = 5
            while(i <= lineCount):
                self.addNewBlock(self.loadBlockFromFile(i-1))
                i+=4
        return 

    def writeFirstBlockToFile(self):
        blockRef = self.getLatestBlock()
        writeStrToBlockchain(str(blockRef.index), self.name)
        writeStrToBlockchain(str(blockRef.timestamp), self.name)
        writeStrToBlockchain(str(blockRef.data), self.name)
        writeStrToBlockchain(str(blockRef.prevHash), self.name)

    def writeNormalLastBlockToFile(self, newBlock):
        writeStrToBlockchain(str(newBlock.index), self.name)
        writeStrToBlockchain(str(newBlock.timestamp), self.name)
        writeImageToBlockchain(newBlock.data, self.name)
        #writeStrToBlockchain(str(blockRef.prevHash), self.name)
    
    #misc
    def checkIfLineCountOfBlockchainIsRight(self) -> bool:
        if(returnLineCountOfBlockchain(self.name)%4==0):
            return True
        return False
    def getHighestIndex(self)-> int:
        return int(self.getLatestBlock().index)

    def loadAllImagesFromBlockchainAndCreateGif(self):
        screenshots = []
        
        for blockRef in self.blocks:
            if(blockRef.index != "0"):
                screenshots.append(blockRef.data)
        if not len(screenshots) == 0:
            createGifFromScreenshotsGiven(screenshots)

    #of What? That the Blockchain owner is rightous?
    def checkValidity(self):
        pass