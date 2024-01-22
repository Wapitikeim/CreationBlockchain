import os 
import os.path
import shutil

import subprocess
import threading

from blockchain import * 

import dataToBlockchain
from PIL import Image
from PIL import ImageChops
import io
import re

import time
import datetime
import filecmp
import mss


def takeScreenshotOfMonitor1AndWriteThemIntoABlockchain(blockchainRef):
    with mss.mss() as sct:
        sct.compression_level = 9
        sct.shot()
        if(blockchainRef.getHighestIndex() != 0):
            #Check first if Image is the same
            """ ref = Image.open("monitor-1.png")
            i = returnLineCountOfBlockchain(blockchainRef.name)-2
            ref2 = Image.open(readImageBytesFromBlockchain(i, blockchainRef.name))
            b = ImageChops.difference(ref,ref2).getbbox() is not None
            ref.close()
            ref2.close()
            if(b): """
            newNameWithTimestamp = datetime.datetime.now().strftime("%d %m %Y,%H %M %S")+".png"
            if(os.path.isfile(newNameWithTimestamp) == False):
                os.rename("monitor-1.png", newNameWithTimestamp)
            shutil.move(newNameWithTimestamp, "media/Screenshots/"+newNameWithTimestamp)
            #BlockchainAddSuperUglyHere Data = name -> will get changed
            writeCurrentUndoCommandIntoSpecialList(blockchainRef)
            newIndex = blockchainRef.getHighestIndex()
            newIndex +=1
            imageData = getImageDataBase64FromScreenshotFolder(newNameWithTimestamp)
            blockchainRef.addNewBlockForScreenshots(Block(blockHeader(newIndex, newNameWithTimestamp.strip(".png")),blockData(imageData,getCurrentNameOfCommandFromUndoLogFile())))
            """ else:
                os.remove("monitor-1.png")
                print("Removed duplicate Picture") """
        else:
            newNameWithTimestamp = datetime.datetime.now().strftime("%d %m %Y,%H %M %S")+".png"
            if(os.path.isfile(newNameWithTimestamp) == False):
                os.rename("monitor-1.png", newNameWithTimestamp)
            shutil.move(newNameWithTimestamp, "media/Screenshots/"+newNameWithTimestamp)
            #BlockchainAddSuperUglyHere Data = name -> will get changed
            writeBlockZeroIntoSpecialCommandListForBlockchain(blockchainRef)
            newIndex = blockchainRef.getHighestIndex()
            newIndex +=1
            imageData = getImageDataBase64FromScreenshotFolder(newNameWithTimestamp)
            blockchainRef.addNewBlockForScreenshots(Block(blockHeader(newIndex, newNameWithTimestamp.strip(".png")),blockData(imageData,getCurrentNameOfCommandFromUndoLogFile())))

def startBlender():
    subprocess.run([r"scripts\blenderStart.bat"], shell=False, capture_output=False)

def makeScreenshotsBasedOnLogChangesAndWriteThemIntoABlockchain(blockchainRef, blenderThread):
    try:
        resetOldBlenderLog()
        time.sleep(5) #To give blender Time to Load
        #oldLinecount = getLineCountOFFile("scripts/undo_log.txt")
        while blenderThread.is_alive():
            #newTime = os.stat("scripts/undo_log.txt").st_mtime
            #newLinecount = getLineCountOFFile("scripts/undo_log.txt")
            if not checkIfBlenderLogIsTheSame():
                updateOldBlenderLogWithCurrentOne()
                takeScreenshotOfMonitor1AndWriteThemIntoABlockchain(blockchainRef)
            time.sleep(0.1) #somehow it just goes mayham without probably because the copy function is too slow
        
        shutil.rmtree("media/Screenshots/")
        os.mkdir("media/Screenshots/")
    except KeyboardInterrupt:
        print("User Interrupted")
        #blenderHandler.join()

def startBlenderAndStartTakingScreenshots(blockchainRef):
    blenderHandler = threading.Thread(target=startBlender)
    blenderHandler.start()
    screenshotHandler = threading.Thread(target=makeScreenshotsBasedOnLogChangesAndWriteThemIntoABlockchain(blockchainRef,blenderHandler))
    screenshotHandler.start()
    blenderHandler.join()
    screenshotHandler.join()

#util
def checkIfBlenderLogIsTheSame():
    return filecmp.cmp("scripts/undo_log.txt", "scripts/undo_log_old.txt", shallow=False) 
def resetOldBlenderLog():
    oldLog = open('scripts/undo_log_old.txt', "w")
    oldLog.close()
def updateOldBlenderLogWithCurrentOne():
    shutil.copyfile("scripts/undo_log.txt", "scripts/undo_log_old.txt")
def getCurrentCommandFromUndoLogFile() ->str:
    undoLogFile = open("scripts/undo_log_old.txt", "r") #old here cause the blender script may write to fast
    undoLogFileLines = undoLogFile.read().splitlines()
    undoLogFile.close()
    ref = "Nothing"
    for line in undoLogFileLines:
        if '*' in line:
            ref = line 
            break
    return ref 
def getCurrentNameOfCommandFromUndoLogFile() ->str:
    ref = getCurrentCommandFromUndoLogFile()
    command = re.search(r'name=\'.*\'', ref)
    ref2 = re.search(r'\'.*\'', command.group())
    return ref2.group()
def writeCurrentUndoCommandIntoSpecialList(blockchainRef):
    commandList = open("Blockchains/" + blockchainRef.name.strip(".txt") + "commands.txt" , "a")
    commandList.write(str(blockchainRef.getHighestIndex()))
    commandList.write(" ")
    commandList.write(getCurrentNameOfCommandFromUndoLogFile())
    commandList.write("\n")
    commandList.close()
def writeBlockZeroIntoSpecialCommandListForBlockchain(blockchainRef):
    commandList = open("Blockchains/" + blockchainRef.name.strip(".txt") + "commands.txt" , "w")
    commandList.write(str(blockchainRef.getHighestIndex()))
    commandList.write(" ")
    commandList.write("Block Zero")
    commandList.write("\n")
    commandList.close()
#misc
def makeScreenshotsBasedJustOnTimer(timeInterval):
    time.sleep(3)  
    while True:
        takeScreenshotOfMonitor1AndWriteThemIntoABlockchain()
        time.sleep(timeInterval)
def takeBlenderScreenshotAndWriteItToIntoABlockchain(blockchainRef):
    newNameWithTimestamp = datetime.datetime.now().strftime("%d %m %Y,%H %M %S")+".png"
    if(os.path.isfile(newNameWithTimestamp) == False):
        try:
            os.rename("out_put.png", newNameWithTimestamp)
        except PermissionError:
            time.sleep(0.1)
            return
        shutil.move(newNameWithTimestamp, "media/Screenshots/"+newNameWithTimestamp)
        #BlockchainAddSuperUglyHere Data = name -> will get changed
        newIndex = blockchainRef.getHighestIndex()
        newIndex +=1
        blockchainRef.addNewBlockForScreenshots(Block(newIndex, newNameWithTimestamp.strip(".png"), newNameWithTimestamp, ""))

#makeScreenshotsBasedJustOnTimer(20)
