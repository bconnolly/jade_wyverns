#Scene Hex converter
#This script takes a csv for an individual and converts columns C-F into a hex format
#The difference between this one and the HexConverter2 script is that this one contains no spaces between the blocks of hex.

#THIS SCRIPT REQUIRES THE "CharacterIDs - Sheet1.csv"
#TO BE LOCATED IN THE SAME FOLDER AS THE SCRIPT

#This script will only work for .csv files. xlsx or any other type of spreadsheet
#file will not work so be sure to convert it to a csv before attempting
#to use the script

#hex format for text file
#03 00 00 00 04 00 00 00 10 00 00 00 FF FF FF FF
#01 00 00 00 FF FF FF FF 01 00 00 00 00 00 00 00
#00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

#03 00 00 00 - Script Function
#04 00 00 00 - Character for text
#10 00 00 00 - Which text line to use
#FF FF FF FF - Characters Animation/Physical Gesture
#01 00 00 00 - Portrait Expression
#FF FF FF FF - Voice line (always going to be this)
#01 00 00 00 - Unknown, but always like this for text box stuff
#00 00 00 00 - then 5 of these


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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#csv to dictionary. used for the character file
#converts them to a data structure that will be used here
#REQUIRES THE FILE TO BE IN THE SAME FOLDER AS THE SCRIPT

#because of a single value being weird, I need this function
def safe_str_to_int(value_str):
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


    

#converts a new hex number to a text format
def convertHexToFormat(hexNumber):

    
    hex_str = format(int(hexNumber), '08X')

    hex_formatted = ' '.join(hex_str[i:i+2] for i in range(6, -2, -2))  

    hex_formatted += ' '

    return hex_formatted

#Uses regular expressions to find a number from the value parameter
#as the template we use uses a dropdown for emotion (ex: Sad = 3)
#This function extracts that number and uses convertHexToFormat
#to return the formatted hex value
#while the values for Action should all be numerical, the action
#values are sent through here just in case
def stringValueToHex(value):
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
        hex_formatted = "00 00 00 00"

    return hex_formatted


#Takes a key and searches for its corresponding value in a specified dictionary
def retrieveHexValue(retrievingValue, dictionaryValue):

    returningKey = 0;
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


#END OF FUNCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#START OF MAIN

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
