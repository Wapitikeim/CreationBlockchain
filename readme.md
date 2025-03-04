## Creation Blockchain

### Important Notice
This code is not yet cleaned up and requires refactoring!
There are many unnecessary code snippets and functions that should be optimized.

### Compatibility
Designed for Windows 11 (likely compatible with Windows 10).
Tested on three different Windows 11 systems.
- Not compatible with macOS or Linux due to the use of blenderStart.bat.
- Requirements
Blender (tested with versions 3.6 and 4.0).
If not using the provided .exe files, you need:
Python 3.12+
Required Python modules (listed in requirements.txt).

### Usage

Main Program
There are two ways to use this program:

#### Using the Prebuilt Executable:

The compiled .exe files can be found in the out/ zip folder.
- Windows Defender may flag the .exe as a virus. You may need to add an exception in Windows Security.
Running via Python:

Install dependencies from requirements.txt.
Run main.py as the entry point.
Validation Server
The validation server can be used in two ways:

#### Using the Provided Executable:

Located in validationServerCode/.
If the server is not running locally, you must adjust the "HOST" entry in blockchainValidationClient.py.
Running via Python:

Use blockchainValidationServer.py as the entry point.
Install dependencies from serverRequirements.txt.


### Features
- Blockchain-based logging of Blender usage (captures screenshots).
- Displays stored blockchain data in a structured format.
- Verifies blockchain integrity through hash recalculations.
- Supports a validation server for storing public keys and verifying blockchain signatures.
