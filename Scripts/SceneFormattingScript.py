'''
SceneFormattingScript.py
By: Lilypad33

This script generates a formatted text file that can be used with the Triabolical edtior to create
the text bin file for a cutscene.

This script was created for use with the Jade Wyverns cutscene spreadsheet template.

Dependencies:
- A filled out cutscene using the Jade Wyverns cutscene spreadsheet template

Returns:
- A formatted text file

Future updates:
- Options to pass in the file path to the cutscene spreadsheet as a parameter for the script.

'''


import csv
import os
import sys

def generateExtractedCSVList(csvFile):
    '''
    This function takes the contents of a csv file, performs some manipulation, and returns a formatted list of strings.

    For each dialogue box in a cutscene, it formats a string that contains the line number (lineNo) and the aggregation (DIALOG_COLUMN) from the csv file.
    The result is appended to a list which is the output of this function.

    Args:
    - csvFile : _reader
        The contents of the csv file to be read

    Returns:
    - linesToAdd : list
        A list of the strings generated. Each string equates to a row in the text file, which is done outside of the function.
    
    '''

    lineNo = -1
    linesToAdd = []
    innerCount = 0

    for index, row in enumerate(csvFile):

        # Because a dialogue box in the template is 3 rows, we need to jump to every 3rd row
        if (innerCount) % 3 == 0:

            cell_value = row[DIALOG_COLUMN]

            # Stops running if a blank dialogue box is found.
            if len(cell_value) == 2:
                break
            
            lineNo += 1
            textFileLine = [f'Line {lineNo}: ', cell_value]
            linesToAdd.append(textFileLine)


        innerCount += 1

    linesToAdd.insert(0, ['EventText', str(secondNumber), str(lineNo)])

    return linesToAdd

###################################### START OF MAIN ###############################################

# Allows for the user to pass in the file name as a parameter. Otherwise asks the user for it
if len(sys.argv) > 1:
    fileName = sys.argv[1]
else:
    fileName = input("Please put the filepath with .csv at the end: ")

if not os.path.exists(fileName):
    print("Error: {} does not exist. Please check the file path and try again.".format(fileName))
    sys.exit()


# Extracts the name of the file, minus the file type
fileNameExtracted = fileName[:-4]

#note for the future: should I make this a global variable?
secondNumber = int(input("Input the 1st Header number: "))

DIALOG_COLUMN = 10


# Opens the file and generates a new text file with the same name as the csv
with open(fileName, 'r') as fileIn, open(f'{fileNameExtracted}TextFormatted.txt', 'w') as fileOut:
    csvContent = csv.reader(fileIn, delimiter=',')
    next(csvContent)  # Skip the header

    textToWrite = generateExtractedCSVList(csvContent)

    # Write the contents of the list generated above into a text file
    for item in textToWrite:
        formattedString = '\t'.join(item) + '\n'
        fileOut.write(formattedString)

print("Script completed")
