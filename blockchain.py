import hashlib
from timeit import default_timer as timer
import datetime
import io
from dataclasses import dataclass

from dataToBlockchain import * 

from pngTogif import createGifFromScreenshotsGiven

@dataclass
class blockHeader:
    index: int 
    timestamp: str 
    hashFromPreviousBlock: str = ""
    hashForThisBlock: str = ""

@dataclass
class blockData:
    data1: str = "Empty" #Probably the Screenshot, could be decoded blend file
    data2: str = "Empty" #Probably command that triggerd the Screenshot, could be empty


class Block:
    def __init__(self, blockchainHeaderRef, blockDataRef):
        
        self.block_Header= blockchainHeaderRef
        self.block_Data = blockDataRef
    
    def calcHash(self):
        hashStr = str(self.block_Header.index) + str(self.block_Header.timestamp) + str(self.block_Header.hashFromPreviousBlock) +str(self.block_Data.data1) + str(self.block_Data.data2) 
        return hashlib.sha256(hashStr.encode()).hexdigest()
    

class Blockchain:
    name = ""
    allowedToModify = True
    faultyBlock = ""
    
    def __init__(self, user, blockChainName, loadFlag):
        if loadFlag == False:
            self.createNewBlockchain(user,blockChainName)
        else:
            startTime = timer()
            self.owner = user
            self.name = blockChainName 
            self.blocks = [self.loadBlockZeroIntoBlockchain()]
            print("Loaded Block " + str(self.loadBlockZeroIntoBlockchain().block_Header.index) + " on " + self.name)
            if (self.getLatestBlock().block_Header.hashFromPreviousBlock != user):
                print("User isnt allowed to modify the " + blockChainName + " Blockchain")
                self.allowedToModify = False
            else: 
                if not self.checkIfLineCountOfBlockchainIsRight():
                    print("Something isnt right with the Linecount of " + self.name)
                    self.allowedToModify = False
                else:
                    self.loadRemaingBlocks()
                    endTime = timer()
                    print("It took: " + str(endTime-startTime) + " To Load" )

    #New Blockchain
    def createNewBlockchain(self, user, blockChainName):
        self.owner = user
        self.name = blockChainName
        self.blocks = [self.createBlockZero()]
        self.getLatestBlock().block_Header.hashForThisBlock = self.getLatestBlock().calcHash()
        self.writeFirstBlockToFile()
        print("Successfully created the Blockchain: " +blockChainName)
    def createBlockZero(self) -> Block:
        return Block(blockHeader(0,datetime.datetime.now(),self.owner), blockData(self.name))
    def writeFirstBlockToFile(self):
        blockRef = self.getLatestBlock()
        writeStrToBlockchain(str(blockRef.block_Header.index), self.name)
        writeStrToBlockchain(str(blockRef.block_Header.timestamp), self.name)
        writeStrToBlockchain(str(blockRef.block_Header.hashFromPreviousBlock), self.name)
        writeStrToBlockchain(str(blockRef.block_Header.hashForThisBlock), self.name)
        writeStrToBlockchain(str(blockRef.block_Data.data1), self.name)
        writeStrToBlockchain(str(blockRef.block_Data.data2), self.name)

    #Loading Blockchain
    def loadBlockZeroIntoBlockchain(self):
        blockchainToLoad = open("blockchains/"+self.name, "r")
        blockchainToLoadSplit = blockchainToLoad.read().splitlines()
        indexRef = blockchainToLoadSplit[0]
        timestampRef = blockchainToLoadSplit[1]
        prevHashRef = blockchainToLoadSplit[2]
        thisHashRef = blockchainToLoadSplit[3]
        data1Ref = blockchainToLoadSplit[4]
        data2Ref = blockchainToLoadSplit[5]
        blockchainToLoad.close()
        return Block(blockHeader(indexRef, timestampRef,prevHashRef,thisHashRef),blockData(data1Ref,data2Ref))
    def loadRemaingBlocks(self):
        lineCount = returnLineCountOfBlockchain(self.name)
        if(lineCount>6):
            i = 6
            blockchainToLoad = open("blockchains/"+self.name, "r")
            blockchainToLoadSplit = blockchainToLoad.read().splitlines()
            while(i < lineCount):
                indexForLoadedBlock = blockchainToLoadSplit[i]
                timestampLoadedBlock = blockchainToLoadSplit[i+1]
                hashPrevLoadedBlock = blockchainToLoadSplit[i+2]
                hashThisBlockLoadedBlock = blockchainToLoadSplit[i+3]
                data1LoadedBlock = "Image missing"
                data2LoadedBlock = blockchainToLoadSplit[i+5]
                self.addBlockToList(Block(blockHeader(indexForLoadedBlock,timestampLoadedBlock, hashPrevLoadedBlock,hashThisBlockLoadedBlock), blockData(data1LoadedBlock, data2LoadedBlock)))
                i+=6
            blockchainToLoad.close()
            self.loadAllRemaningImagesFromBlockchain()
        return 
    def addBlockToList(self, newBlock):
        print("Loaded Block " + str(newBlock.block_Header.index) + " on " + self.name)
        self.blocks.append(newBlock)
    def getScreenshotBlockFromFile(self, index):
        indexRef = readStrFromBlockchain(index, self.name) 
        timestampRef = readStrFromBlockchain(index+1, self.name)
        prevHashRef = readStrFromBlockchain(index+2, self.name)
        thisHashRef = readStrFromBlockchain(index+3, self.name)
        data1Ref = readImageBytesFromBlockchain(index+4, self.name)
        data2Ref = readStrFromBlockchain(index+5, self.name)
        return Block(blockHeader(indexRef, timestampRef,prevHashRef,thisHashRef),blockData(data1Ref,data2Ref))
    def loadAllRemaningImagesFromBlockchain(self):
        blockchainToLoad = open("blockchains/"+self.name, "rb")
        blockchainToLoadSplit = blockchainToLoad.read().splitlines()
        for block in self.blocks:
            if block.block_Data.data1 == "Image missing":
                data1Pos = (int(block.block_Header.index)*6)+4
                block.block_Data.data1 = io.BytesIO(base64.b64decode(blockchainToLoadSplit[data1Pos]))
                print("Loaded Image on Block " + block.block_Header.index)
        blockchainToLoad.close()
    #Add Block triggerd from Outside(with b64encoded Image Data)
    def addNewBlockForScreenshots(self, newBlock):
        newBlock.block_Header.hashFromPreviousBlock = self.getLatestBlock().block_Header.hashForThisBlock
        newBlock.block_Header.hashForThisBlock = newBlock.calcHash()
        self.writeScreenshotBlockToBlockchainFile(newBlock)
        newBlock.block_Data.data1 = io.BytesIO(base64.b64decode(newBlock.block_Data.data1))
        self.blocks.append(newBlock)

        print("Added Block " + str(newBlock.block_Header.index) + " On Blockchain: " +self.name)
    def writeScreenshotBlockToBlockchainFile(self, newBlock):
        writeStrToBlockchain(str(newBlock.block_Header.index), self.name)
        writeStrToBlockchain(str(newBlock.block_Header.timestamp), self.name)
        writeStrToBlockchain(str(newBlock.block_Header.hashFromPreviousBlock), self.name)
        writeStrToBlockchain(str(newBlock.block_Header.hashForThisBlock), self.name)
        writeImageDataBase64ToBlockchain(newBlock.block_Data.data1, self.name)
        writeStrToBlockchain(str(newBlock.block_Data.data2), self.name)
    
    #utility
    def getLatestBlock(self) -> Block:
        return self.blocks[-1]
    def checkIfLineCountOfBlockchainIsRight(self) -> bool:
        if(returnLineCountOfBlockchain(self.name)%6==0):
            return True
        return False
    def getHighestIndex(self)-> int:
        return int(self.getLatestBlock().block_Header.index)
    def getBlock(self,index) ->Block:
        return self.blocks[index]


    #loading Images / creating Gif
    def loadAllImagesFromBlockchainAndCreateGif(self, name):
        screenshots = []
        
        for blockRef in self.blocks:
            if (blockRef.block_Header.index != "0" and blockRef != self.blocks[0]):
                screenshots.append(blockRef.block_Data.data1)
        if not len(screenshots) == 0:
            createGifFromScreenshotsGiven(screenshots, name)

    #Recalc Blockchain Hashes based on Information @ the textfile and check if theyre correct
    def checkValidity(self) -> bool:
        result = True
        blockchainToLoad = open("blockchains/"+self.name, "r")
        blockchainImageLoader = open("blockchains/"+self.name, "rb")
        blockchainImageLoaderSplit = blockchainImageLoader.read().splitlines()
        blockchainToLoadSplit = blockchainToLoad.read().splitlines()
        for block in self.blocks:
            if str(block.block_Header.index) != "0":
                ref = (int(block.block_Header.index)*6) 
                indexRef = blockchainToLoadSplit[ref]
                timestampRef = blockchainToLoadSplit[ref+1]
                hashPrevRef = blockchainToLoadSplit[ref+2]
                hashThisRef = blockchainToLoadSplit[ref+3]
                data1Ref = blockchainImageLoaderSplit[ref+4]
                
                data2Ref = blockchainToLoadSplit[ref+5]
                hashStrRef = str(indexRef) + str(timestampRef) + str(hashPrevRef) + str(data1Ref) + str(data2Ref)
                hashThatShouldBe = hashlib.sha256(hashStrRef.encode()).hexdigest()
                if hashThatShouldBe != hashThisRef:
                    result = False
                    self.faultyBlock = str(block.block_Header.index)
                    break
        blockchainImageLoader.close()
        blockchainToLoad.close()
        return result
    
