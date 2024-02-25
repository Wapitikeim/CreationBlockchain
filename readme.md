IMPORTANT:
The code isn't cleaned up and is in need of an refactor!.
Alot of unnecessary codesnippets/functions are present.


Compatibility:
This Programm is written for Windows 11 (Probably 10 also fine)
->Tested on 3 different Windows 11 Systems
-> wont work on MAC/Linux because of "blenderStart.bat"

Requirements:
-Blender (tested with Blender 3.6 / 4.0)
-If not using the .exe then also python 3.12+ and the modules listed in requirements.txt

Usage:

Main Programm:
One way to use this programm is through the provided .exe Files inside the out/ zip. Folders
->Windows probably detects the .exe as an Virus (-> Need an exception in Windows Security)
Another way to use the programm is to use python:
->Requirements.txt lists the required python modules
-->main.py as the entry point

ValidationServer:
Either Provided exe in validationServerCode/
-> Need to adjust the "HOST" entry in blockchainValidationClient.py if Server is not used on local machine.
Or python with blockchainValidationServer.py as entry and the required modules in serverRequirements.txt


Features:
-Create a Blockchain structure which contains Screenshots of your Blender usage
-Shows the Data stored in the Blockchain structure
-Can verify the created Blockchain based on recalculation of Hashes
-In Combination with the provided Validation Server can store the public keys of users which then can verify the signatures inside the Blockchain.