@echo off
cd C:\Program Files\Blender Foundation\Blender 4.0\
blender --log "*operator*" --log-file C:\Users\Wenz\Desktop\CreationBlockchain\scripts\Log.txt --log-level 1 --python-use-system-env --python C:\Users\Wenz\Desktop\CreationBlockchain\scripts\blenderControl.py 
