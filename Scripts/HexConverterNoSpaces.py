'''
Dialogue Box Hex Generator
By: Lilypad33

This script generates the hex blocks for a dialogue box for an event bin file using the contents of a filled-out csv template.

This script was created for use with the Jade Wyverns cutscene spreadsheet template.

Dependencies:
- A filled out cutscene csv file using the Jade Wyverns cutscene spreadsheet template
- "CharacterIDs - Sheet1.csv"
    This file contains, in key/value pairs, the IDs for each character in the game. This script looks to that file for the IDs, 
    so it is a required file. DO NOT MOVE IT FROM THE SAME FOLDER AS THE SCRIPT.

    When you want to add a character to the game, and utilize this script, you must find their associated ID value in the csv file,
    and replace the value in Column A.

    This will not change what appears in the hex editor. In order for the correct names to appear in the hex editor, you will need to change
    the associated character in the enumCharacter enum in the "Three_House_Binary_Templates\Event-Related\include\event_script_enums.bt" file.


Returns:
- A text file containing all the hex for the dialogue boxes in the cutscene.
    In order to add it to the event bin file:
        1. Open the generated text file
        2. CTRL-A and CTRL-C to select all and copy.
        3. Open the event bin file in a hex editor.
        4. Delete all the old hex from below the New Scene hex block.
        5. Ensure your computer is in insert mode (Insert button on keyboard)
        6. Paste from Hex Text, which is CTRL-SHIFT-V. It is recommended that the command is hotkeyed.

Future updates:
- Options to pass in the file path to the cutscene spreadsheet as a parameter for the script.

'''


import csv
import os
import re

#if these change at all, the script can be edited in a later version
#ScriptFunction
scriptFunction = "03 00 00 00 "

#VoiceLine
voiceLine = "FF FF FF FF"

#last line is this *4, also use this for last hex on line 2
lastLine = "00 00 00 00 "

#Unknown?
unknownHex = "01 00 00 00 "


#FileNames
characterFileName = "CharacterIDs - Sheet1.csv"


#column numbers
CHARACTER_COL = 2
ACTION_COL = 4
EMOTION_COL = 5


def safe_str_to_int(value_str):
    '''
    Because a single value in the Character IDs csv file being unusual, this function needs to exist
    
    '''
    try:
        # Attempt to convert as a decimal integer
        return int(value_str)
    except ValueError:
        try:
            # Attempt to convert as a hexadecimal integer
            return int(value_str, 16)
        except ValueError:
            # Handle the case where the value is not a valid integer (neither decimal nor hexadecimal)
            print(f"Warning: Invalid integer value: {value_str}")
            return None


#searches the local directory for a CSV with a matching file name
#reads the csv and converts its contents into a dictionary
#returns a filled dictionary
def csvToDict(fileName):
    '''
    Converts the contents of a csv file to a dictionary.

    Args:
    - filename : str
        The name of the csv file.

    Returns:
    - datamap : dict
        A dictionary containing in key/value pairs the contents of columns A (key) and B (value)
    
    '''

    current_directory = os.path.dirname(os.path.abspath(__file__))

    csv_file_path = os.path.join(current_directory, fileName)

    dataMap = {}
    

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        
        # Iterate through each row in the CSV and populate the dictionary
        for row in csv_reader:
            if len(row) >= 2:
                key = row[0]
                value_str = row[1]
                value_int = safe_str_to_int(value_str)
                if value_int is not None:
                    dataMap[key] = value_int

    return dataMap


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Hex Value Functions

def convertHexToFormat(hexNumber):
    '''
    Takes a number, converts it to a hexadecimal format, and returns the number as a string in
    the required format.

    Args:
    - hexNumber
        The number, in decimal format, to be converted.
    
    Returns:
    - hex_formatted : str
        The converted number as a string
    
    '''

    
    hex_str = format(int(hexNumber), '08X')

    hex_formatted = ' '.join(hex_str[i:i+2] for i in range(6, -2, -2))  

    hex_formatted += ' '

    return hex_formatted


def stringValueToHex(value):
    '''
    This function takes a number, looks in the cell of a csv to extract a number that matches the regex pattern,
    and returns a string.

    If it doesn't find a match, hex_formatted returns as "00 00 00 00".
    If the value is -1, it returns "FF FF FF FF".
    Otherwise, it uses convertHexToFormat to convert the number to hexadecimal format and returns the formatted string.

    Args:
    - value : any
        The cell of a csv that is to be looked at.

    Returns:
    - hex_formatted : str
        A string formatted in the appropriate format.

    '''
    value = str(value)

    #pattern searches for an optional "-" character (for -1 actions) and a digit
    pattern = r'\-?\d+'
    match = re.search(pattern, value)  
    if match:
        number = int(match.group())
        if number == -1:
            hex_formatted = "FF FF FF FF"
        else:  
            hex_formatted = convertHexToFormat(number)  
    else:
        # at some point I need to set this to the default "00 00 00 00" value
        hex_formatted = "00 00 00 00"

    return hex_formatted


def retrieveHexValue(retrievingValue, dictionaryValue):
    '''
    This is used for retrieving the character IDs from a cutscene. It takes a dictionary,
    and uses the retrievingValue parameter (the character) to search for its corresponding
    ID value. It then uses convertHexToFormat to convert and format the number in a
    hexidecimal format.


    Parameters:
    - retrievingValue : any
        The key to search for
    - dictionaryValue : any
        The dictionary that is being searched

    Returns:
    - returningValue : str
        Using convertHexToFormat, it takes the value associated with the value from dictionaryValue 
        and converts it to the correct format.
    
    
    '''

    returningKey = 0
    isSuccessfull = False

    for key in dictionaryValue:

        #searches the dictionary for the first matching key
        #if it does find a matching value, sets a boolean to True
        #and breaks the loop
        if key.startswith(str(retrievingValue)):
            returningKey = dictionaryValue[key]
            isSuccessfull = True
        if isSuccessfull:
            break


    #calls the convertHexToFormat function to convert
    #the integer to a hex and format it correctly
    returningValue = convertHexToFormat(returningKey)
            
    return returningValue


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#returns an array of values where each line is a converted hex line or spaces
#for separation purposes
def generateTextBox(csvFile):
    '''
    The main function for generating each dialogue box. It generates the 3 lines for each dialogue box before being added to
    a list. 

    Parameters:
    - csvFile
        The contents of the cutscene spreadsheet.

    Returns:
    - linesToAdd : list
        A list of the strings generated. Each string equates to a row in the text file, which is done outside of the function.
    
    
    
    '''

    innerCount = 0

    linesToAdd = []

    #current Line number
    lineNo = 0

    for index, row in enumerate(csvFile):

        #an inner counter is used to track each text box number
        #any number that is divisible by 3
        if innerCount % 3 == 0:

            
            characterValue = row[CHARACTER_COL]
            characterHex = retrieveHexValue(characterValue, characterDict)

            actionValue = row[ACTION_COL]
            if actionValue is None or actionValue == "":
                actionValue = 0

            actionHex = stringValueToHex(actionValue)
            
            emotionValue = row[EMOTION_COL]

            if emotionValue is None or emotionValue == "":
                emotionValue = 0

            
            emotionHex = stringValueToHex(emotionValue)


            lineNoToHex = convertHexToFormat(lineNo)
            
            
            #creating the lines
            line1 = [scriptFunction, characterHex, lineNoToHex, actionHex]
            line2 = [emotionHex, voiceLine, unknownHex, lastLine]
            line3 = [lastLine] * 4

            lineNo += 1


            
            completedTextBox = [line1,line2,line3]

            #Appends the text box, plus the extra blank rows, to the new array
            #linesToAdd.append(completedTextBox)
            for line in completedTextBox:
                linesToAdd.append(line)


        #increment the inner counter
        innerCount += 1

    #returns a completed array        
    return linesToAdd


################################### START OF MAIN ######################################################

#generates the dictionaries
characterDict = csvToDict(characterFileName)


sceneFileName = input("Please put the full filepath with .csv at the end: ")
fileNameExtracted = sceneFileName[:-4]


with open(sceneFileName, 'r') as fileIn, open(f'{fileNameExtracted}HexValues.txt', 'w') as fileOut:
    content = csv.reader(fileIn, delimiter=',')

    #skips the header row
    next(content)

    print("Starting the data transformation...")

    #takes the data taken from the scene csv, and transforms the data
    #the return value for the function is placed in newArray
    textBox = generateTextBox(content)

    #formats and adds the data in textBox to the txt file
    for row in textBox:
        formatted_row = ' '.join(str(item).strip() for item in row if str(item).strip())
        fileOut.write(str(formatted_row) + "\n")
    print(f'File with the name {fileNameExtracted}HexValues.txt created')
    print(f'in the same folder as {sceneFileName}')




print("Script completed")
