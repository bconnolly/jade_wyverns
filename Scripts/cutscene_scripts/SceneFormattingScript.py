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

'''


import csv
import os
import sys
import pyperclip

def text_to_bin_preparation():
    
    DIALOG_COLUMN = 10
    SECOND_NUMBER = 50
    #SECOND_NUMBER = int(input("Input the 1st Header number: "))

    def looks_like_file_path(text):
        if not text or not isinstance(text, str):
            # Returns false if text isn't a string
            print("Content from clipboard is not a valid type.")
            return False
        elif not os.path.exists(text):
            # Checks if it is a valid file path
            print("Content from clipboard is not a valid file path.")
            return False
        else:
            return True


    def getFilePath():

        filepath = pyperclip.paste().strip().strip('"')

        if not looks_like_file_path(filepath):
            # Allows for the user to pass in the file name as an argument. Otherwise asks the user for it
            if len(sys.argv) > 1:
                filepath = sys.argv[1]
            else:
                filepath = input("Please put the filepath with .csv at the end: ").strip('"')

            if not os.path.exists(filepath):
                print("Error: {} does not exist. Please check the file path and try again.".format(filepath))
                sys.exit()

        return filepath


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
                if len(cell_value) <= 2:
                    break
                
                lineNo += 1
                textFileLine = [f'Line {lineNo}: ', cell_value]
                linesToAdd.append(textFileLine)


            innerCount += 1

        linesToAdd.insert(0, ['EventText', str(SECOND_NUMBER), str(lineNo)])

        return linesToAdd

    fileName = getFilePath()

    # Extracts the name of the file, minus the file type
    fileNameExtracted = fileName[:-4]

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

if __name__ == "__main__":
    text_to_bin_preparation()
