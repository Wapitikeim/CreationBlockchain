import os
import time  

while True:
    test = os.stat("Log.txt").st_mtime
    print(test)
    time.sleep(1)
    
