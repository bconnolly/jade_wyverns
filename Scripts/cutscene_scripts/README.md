These scripts assist with the creation of cutscenes. 

Both scripts require that the cutscene is written using this template provided [here](https://docs.google.com/spreadsheets/d/1Q34DNdbEwAs9QqQI5tPBMmyNvVdBDbIpUJMQE7kkpVI/edit?usp=sharing). 


**To download the template to your Google Drive:**
Click "File" -> ?Make a Copy"

**To download the template as a Microsoft Excel file:**
Click "File" -> "Download" -> "Microsoft Excel (.xlsx)".

**Before running these scripts, ensure that you have a local copy of the cutscene sheet by clicking "File" -> "Download" -> "Comma Separated Values (.csv)".** Currently the scripts do not support Excel files natively; they will only support .csv files. This may change in a future update.

# Script Descriptions
## HexConverterNoSpaces.py
This script generates the hex code for a cutscene's dialogue boxes. This is useful for the cutscene's **event bin** file.

There are two modes: **Default** and **Spaces**.
### Default
The hex code is generated to a text file in one uninteruppted text file. This makes it easy to copy/paste the hex code for all of a cutscene's dialogue boxes into the event bin.

This is the default mode, and it will run if you hit "n" or "Enter" when prompted by the script.

### Spaces
The hex code is generated to a text file with a line number indicator, followed by the hex code for each dialogue box in the cutscene. 

This is the alt mode, and it will run if you hit "y" or "Y" when prompted by the script.

## SceneFormatttingScript.py
This script prepares a text file that can be used in the Triabolical editor to create the **text bin** for a cutscene. 

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