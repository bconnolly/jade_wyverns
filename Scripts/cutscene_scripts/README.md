These scripts assist with the creation of cutscenes. 

# Setup & Running the Scripts (Windows only)

## Setup
1. Install Python
2. Click setup.bat to install pip and requirements.txt

## Running the Scripts
### Using the bat file (recommended)
1. Copy the path of the cutscene csv file.
2. Click on run.bat

### Manual Script execution
```
python HexConverterNoSpaces.py
python SceneFormattingScript.py
```
⚠️ Note for macOS/Linux users reading this section:
These commands use python, which is the default on Windows.
On macOS/Linux, you should use python3 instead.

# Setup & Running the Scripts (Linux/Mac)
No setup or run scripts available yet. The linux and mac instructions are untested.

## Manual setup
Install the below requirements:
- python (version 3.0 or higher)
- run the below commands to install the requirements.txt
```
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```
⚠️ Note for Windows users:
These commands use python3, which may not work on Windows.
On Windows, use python instead — or run setup.bat.

💡 Not sure which command works?
Try python --version and python3 --version to see which one responds.
## Manual Script execution
```
python3 HexConverterNoSpaces.py
python3 SceneFormattingScript.py
```