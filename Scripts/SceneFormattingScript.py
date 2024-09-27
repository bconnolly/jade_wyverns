import csv

def generateExtractedCSVList(csvFile):
    '''
    This function takes the contents of a csv file, performs some manipulation, and returns a formatted list.

    Parameters
    - csvFile : _reader
        The contents of the csv file to be read

    Output
    - linesToAdd : list
        The elements of this list equate to rows on a text file. The writing to the txt file is done at a later stage
        outside of this function.
    
    '''

    lineNo = -1
    linesToAdd = []
    innerCount = 0
    charLine = ""

    for index, row in enumerate(csvFile):
        cell_value = row[DIALOG_COLUMN]

        # Accumulate data for every three rows
        charLine += cell_value

        if (innerCount + 1) % 3 == 0:

            #have lineNo be incremented here?
            lineNo += 1
            textFileLine = [f'Line {lineNo}: ', charLine]
            linesToAdd.append(textFileLine)
            
            charLine = ""

        innerCount += 1

    if charLine:
        textFileLine = [f'Line {lineNo}: ', charLine]
        linesToAdd.append(textFileLine)

    #I think it needs to decrement one since it counts a second one sometimes?
    #lineNo -= 1
    linesToAdd.insert(0, ['EventText', str(secondNumber), str(lineNo)])

    return linesToAdd

###################################### START OF MAIN ###############################################

fileName = input("Please put the filepath with .csv at the end: ")

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
