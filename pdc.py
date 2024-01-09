import os 
import os.path
import shutil

import subprocess
import threading

from blockchain import * 


import base64
from PIL import Image
import io

import time
import datetime

import mss

def takeScreenshotOfMonitor1AndWriteThemIntoABlockchain(blockchainRef):
    with mss.mss() as sct:
        sct.compression_level = 9
        sct.shot()
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

def makeScreenshotsBasedOnLogChangesAndWriteThemIntoABlockchain(blockchainRef):
    try:
        time.sleep(5)
        oldTime = 0
        while True:
            newTime = os.stat("scripts\Log.txt").st_mtime
            if(newTime != oldTime):
                takeScreenshotOfMonitor1AndWriteThemIntoABlockchain(blockchainRef)
            oldTime = newTime
            time.sleep(2)
    except KeyboardInterrupt:
        pass
        #blenderHandler.join()

def startBlenderAndStartTakingScreenshots(blockchainRef):
    blenderHandler = threading.Thread(target=startBlender)
    blenderHandler.start()
    makeScreenshotsBasedOnLogChangesAndWriteThemIntoABlockchain(blockchainRef)
    blenderHandler.join()



#misc
def makeScreenshotsBasedJustOnTimer(timeInterval):
    time.sleep(3)  
    while True:
        takeScreenshotOfMonitor1AndWriteThemIntoABlockchain()
        time.sleep(timeInterval)
#makeScreenshotsBasedJustOnTimer(20)




