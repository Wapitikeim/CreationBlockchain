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

import time
import datetime

import mss

def takeScreenshotOfMonitor1AndWriteThemIntoABlockchain(blockchainRef):
    with mss.mss() as sct:
        sct.compression_level = 9
        sct.shot()
        if(blockchainRef.getHighestIndex() != 0):
            #Check first if Image is the same
            ref = Image.open("monitor-1.png")
            i = returnLineCountOfBlockchain(blockchainRef.name)-2
            ref2 = Image.open(readImageBytesFromBlockchain(i, blockchainRef.name))
            b = ImageChops.difference(ref,ref2).getbbox() is not None
            ref.close()
            ref2.close()
            if(b):
                newNameWithTimestamp = datetime.datetime.now().strftime("%d %m %Y,%H %M %S")+".png"
                if(os.path.isfile(newNameWithTimestamp) == False):
                    os.rename("monitor-1.png", newNameWithTimestamp)
                shutil.move(newNameWithTimestamp, "media/Screenshots/"+newNameWithTimestamp)
                #BlockchainAddSuperUglyHere Data = name -> will get changed
                newIndex = blockchainRef.getHighestIndex()
                newIndex +=1
                blockchainRef.addNewBlockForScreenshots(Block(newIndex, newNameWithTimestamp.strip(".png"), newNameWithTimestamp, ""))
            else:
                os.remove("monitor-1.png")
                print("Removed duplicate Picture")
        else:
            newNameWithTimestamp = datetime.datetime.now().strftime("%d %m %Y,%H %M %S")+".png"
            if(os.path.isfile(newNameWithTimestamp) == False):
                os.rename("monitor-1.png", newNameWithTimestamp)
            shutil.move(newNameWithTimestamp, "media/Screenshots/"+newNameWithTimestamp)
            #BlockchainAddSuperUglyHere Data = name -> will get changed
            newIndex = blockchainRef.getHighestIndex()
            newIndex +=1
            blockchainRef.addNewBlockForScreenshots(Block(newIndex, newNameWithTimestamp.strip(".png"), newNameWithTimestamp, ""))
        
        
def startBlender():
    subprocess.run([r"scripts\blenderStart.bat"], shell=False, capture_output=False)

def makeScreenshotsBasedOnLogChangesAndWriteThemIntoABlockchain(blockchainRef, blenderThread):
    try:
        time.sleep(5)
        oldTime = 0
        while blenderThread.is_alive():
            newTime = os.stat("scripts\Log.txt").st_mtime
            if(newTime != oldTime):
                takeScreenshotOfMonitor1AndWriteThemIntoABlockchain(blockchainRef)
            oldTime = newTime
            time.sleep(0.25)
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
    



#misc
def makeScreenshotsBasedJustOnTimer(timeInterval):
    time.sleep(3)  
    while True:
        takeScreenshotOfMonitor1AndWriteThemIntoABlockchain()
        time.sleep(timeInterval)
#makeScreenshotsBasedJustOnTimer(20)




