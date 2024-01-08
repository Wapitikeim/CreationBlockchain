from tkinter import *
from tkinter import ttk

import os 
import os.path
import shutil

import subprocess
import threading

import time
import datetime

import mss

def takeScreenshotOfMonitor1():
    with mss.mss() as sct:
        sct.compression_level = 9
        sct.shot()
        newNameWithTimestamp = datetime.datetime.now().strftime("%d %m %Y,%H %M %S")+".png"
        if(os.path.isfile(newNameWithTimestamp) == False):
            os.rename("monitor-1.png", newNameWithTimestamp)
        shutil.move(newNameWithTimestamp, "media/Screenshots/"+newNameWithTimestamp)

def startBlender():
    subprocess.run([r"scripts\blenderStart.bat"], shell=False, capture_output=False)

def makeScreenshotsBasedOnLogChanges():
    try:
        time.sleep(3)
        oldTime = 0
        while True:
            newTime = os.stat("scripts\Log.txt").st_mtime
            if(newTime != oldTime):
                takeScreenshotOfMonitor1()
            oldTime = newTime
            time.sleep(2)
    except KeyboardInterrupt:
        pass
        #blenderHandler.join()

def makeScreenshotsBasedJustOnTimer(timeInterval):
    time.sleep(3)  
    while True:
        takeScreenshotOfMonitor1()
        time.sleep(timeInterval)

def startBlenderAndStartTakingScreenshots():
    blenderHandler = threading.Thread(target=startBlender)
    blenderHandler.start()
    makeScreenshotsBasedOnLogChanges()
    blenderHandler.join()


#makeScreenshotsBasedJustOnTimer(20)




