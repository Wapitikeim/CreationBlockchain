import hashlib
from timeit import default_timer as timer
import datetime
import io
from dataclasses import dataclass
from publicKeyUtil import * 

from dataToBlockchain import * 

from pngTogif import createGifFromScreenshotsGiven

@dataclass
class blockHeader:
    index: int 
    timestamp: str 
    hashFromPreviousBlock: str = ""
    signatureHashPrevBlock: str = ""
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
        hashStr = str(self.block_Header.index) + str(self.block_Header.timestamp) + str(self.block_Header.hashFromPreviousBlock)+ str(self.block_Header.signatureHashPrevBlock) +str(self.block_Data.data1) + str(self.block_Data.data2) 
        return hashlib.sha256(hashStr.encode()).hexdigest()
    

class Blockchain:
    name = ""
    allowedToModify = True
    faultyBlock = ""
    global loadedPrivateKey
    global loadedPublicKey
    
    def __init__(self, user, blockChainName, loadFlag):
        if loadFlag == False:
            self.createNewBlockchain(user,blockChainName)
        else:
            startTime = timer()
            self.owner = user
            self.name = blockChainName 
            self.blocks = [self.loadBlockZeroIntoBlockchain()]
            try:
                self.loadedPrivateKey = load_private_key(user)
                self.loadedPublicKey = load_public_key(user)
                print(f"Keyfiles of {self.owner} loaded")
            except:
                print(f"Something went wrong loading the keyfiles of {self.name} with User {self.name}")
                self.allowedToModify = False
                return
            print("Loaded Block " + str(self.loadBlockZeroIntoBlockchain().block_Header.index) + " on " + self.name)
            if not (check_if_signature_matches_message(self.blocks[0].block_Header.hashFromPreviousBlock.encode(),
                                               self.loadedPublicKey,
                                               self.blocks[0].block_Header.signatureHashPrevBlock
                                            )
            ):
                print(f"{self.owner} isnt allowed to modify the {self.name} Blockchain")
                self.allowedToModify = False 
                return
            else: 
                if not self.checkIfLineCountOfBlockchainIsRight():
                    print("Something isnt right with the Linecount of " + self.name)
                    self.allowedToModify = False
                    return
                else:
                    self.loadRemaingBlocks()
                    endTime = timer()
                    print("It took: " + str(endTime-startTime) + " To Load" )

    #New Blockchain
    def createNewBlockchain(self, user, blockChainName):
        self.owner = user
        self.name = blockChainName
        try:
            self.loadedPrivateKey = load_private_key(user)
            self.loadedPublicKey = load_public_key(user)
            print(f"Keyfiles of {self.owner} loaded")
        except:
            print("Generating Key Files")
            create_Key_Pair_and_write_to_file(user)
            print(f"Generated Key files {self.owner} Private and Public Key under keys/")
            self.loadedPrivateKey = load_private_key(user)
            self.loadedPublicKey = load_public_key(user)
            print(f"Keyfiles of {self.owner} loaded")
        self.blocks = [self.createBlockZero()]
        self.blocks[0].block_Header.signatureHashPrevBlock = create_signature_for_message(self.blocks[0].block_Header.hashFromPreviousBlock.encode(), self.loadedPrivateKey)
        self.blocks[0].block_Header.hashForThisBlock = self.blocks[0].calcHash()
        self.writeFirstBlockToFile()
        print(f"Successfully created the Blockchain: {blockChainName} ")
    def createBlockZero(self) -> Block:
        return Block(blockHeader(0,datetime.datetime.now(),get_SHA512_Hash_from_File("keys/" + self.owner + "Public.pem")), blockData(self.name))
    def writeFirstBlockToFile(self):
        blockRef = self.getLatestBlock()
        writeStrToBlockchain(str(blockRef.block_Header.index), self.name)
        writeStrToBlockchain(str(blockRef.block_Header.timestamp), self.name)
        writeStrToBlockchain(str(blockRef.block_Header.hashFromPreviousBlock), self.name)
        writeBytesToBlockchain(blockRef.block_Header.signatureHashPrevBlock, self.name)
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
        signPrevHashRef = base64.b64decode(blockchainToLoadSplit[3])
        thisHashRef = blockchainToLoadSplit[4]
        data1Ref = blockchainToLoadSplit[5]
        data2Ref = blockchainToLoadSplit[6]
        blockchainToLoad.close()
        return Block(blockHeader(indexRef, timestampRef,prevHashRef,signPrevHashRef,thisHashRef),blockData(data1Ref,data2Ref))
    def loadRemaingBlocks(self):
        lineCount = returnLineCountOfBlockchain(self.name)
        if(lineCount>7):
            i = 7
            blockchainToLoad = open("blockchains/"+self.name, "r")
            blockchainToLoadSplit = blockchainToLoad.read().splitlines()
            while(i < lineCount):
                indexForLoadedBlock = blockchainToLoadSplit[i]
                timestampLoadedBlock = blockchainToLoadSplit[i+1]
                hashPrevLoadedBlock = blockchainToLoadSplit[i+2]
                signPrevHashLoadedBlock = base64.b64decode(blockchainToLoadSplit[i+3])
                hashThisBlockLoadedBlock = blockchainToLoadSplit[i+4]
                data1LoadedBlock = "Image missing"
                data2LoadedBlock = blockchainToLoadSplit[i+6]
                self.addBlockToList(Block(blockHeader(indexForLoadedBlock,timestampLoadedBlock, hashPrevLoadedBlock,signPrevHashLoadedBlock,hashThisBlockLoadedBlock), blockData(data1LoadedBlock, data2LoadedBlock)))
                i+=7
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
                data1Pos = (int(block.block_Header.index)*7)+5
                block.block_Data.data1 = io.BytesIO(base64.b64decode(blockchainToLoadSplit[data1Pos]))
                print("Loaded Image on Block " + block.block_Header.index)
        blockchainToLoad.close()
    
    #Add Block triggerd from Outside(with b64encoded Image Data)
    def addNewBlockForScreenshots(self, newBlock):
        newBlock.block_Header.hashFromPreviousBlock = self.getLatestBlock().block_Header.hashForThisBlock
        newBlock.block_Header.signatureHashPrevBlock = create_signature_for_message(self.getLatestBlock().block_Header.hashFromPreviousBlock.encode(), self.loadedPrivateKey)
        newBlock.block_Header.hashForThisBlock = newBlock.calcHash()
        self.writeScreenshotBlockToBlockchainFile(newBlock)
        newBlock.block_Data.data1 = io.BytesIO(base64.b64decode(newBlock.block_Data.data1))
        self.blocks.append(newBlock)

        print("Added Block " + str(newBlock.block_Header.index) + " On Blockchain: " +self.name)
    def writeScreenshotBlockToBlockchainFile(self, newBlock):
        writeStrToBlockchain(str(newBlock.block_Header.index), self.name)
        writeStrToBlockchain(str(newBlock.block_Header.timestamp), self.name)
        writeStrToBlockchain(str(newBlock.block_Header.hashFromPreviousBlock), self.name)
        writeBytesToBlockchain(newBlock.block_Header.signatureHashPrevBlock, self.name)
        writeStrToBlockchain(str(newBlock.block_Header.hashForThisBlock), self.name)
        writeImageDataBase64ToBlockchain(newBlock.block_Data.data1, self.name)
        writeStrToBlockchain(str(newBlock.block_Data.data2), self.name)
    
    #utility
    def getLatestBlock(self) -> Block:
        return self.blocks[-1]
    def checkIfLineCountOfBlockchainIsRight(self) -> bool:
        if(returnLineCountOfBlockchain(self.name)%7==0):
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
                ref = (int(block.block_Header.index)*7) 
                indexRef = blockchainToLoadSplit[ref]
                timestampRef = blockchainToLoadSplit[ref+1]
                hashPrevRef = blockchainToLoadSplit[ref+2]
                signHashPrevRef = base64.b64decode(blockchainToLoadSplit[ref+3])
                hashThisRef = blockchainToLoadSplit[ref+4]
                data1Ref = blockchainImageLoaderSplit[ref+5]
                data2Ref = blockchainToLoadSplit[ref+6]
                hashStrRef = str(indexRef) + str(timestampRef) + str(hashPrevRef) + str(signHashPrevRef) + str(data1Ref) + str(data2Ref)
                hashThatShouldBe = hashlib.sha256(hashStrRef.encode()).hexdigest()
                if hashThatShouldBe != hashThisRef:
                    result = False
                    self.faultyBlock = str(block.block_Header.index)
                    break
        blockchainImageLoader.close()
        blockchainToLoad.close()
        return result
    
