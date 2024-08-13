import csv

fileName = input("Please put the filepath with .csv at the end: ")

# Extracts the filename
fileNameExtracted = fileName[:-4]


secondNumber = int(input("Input the 1st Header number: "))



DIALOG_COLUMN = 10


#compare this to the javascript version. I think this script can be improved.
#also, make the changes in this repo, so phoebe and Hues and receive this version.

# Generates the first line and adds it to the front of the list of lists
def generateExtractedCSVArray(csvFile):
    
    #I think this can start at -1 and change the variable to LineNo, to maintain
    #consistency with my other script.
    lineCount = -1
    linesToAdd = []
    innerCount = 0
    charLine = ""

    for index, row in enumerate(csvFile):
        cell_value = row[DIALOG_COLUMN]

        # Accumulate data for every three rows
        charLine += cell_value

        if (innerCount + 1) % 3 == 0:

            #have lineCount be incremented here?
            lineCount += 1
            textFileLine = [f'Line {lineCount}: ', charLine]
            linesToAdd.append(textFileLine)
            
            charLine = ""

        #do I even need this anymore?    
        else:
            charLine += '\0'  # Add delimiter for data within a set of three rows

        innerCount += 1

    if charLine:
        textFileLine = [f'Line {lineCount}: ', charLine]
        linesToAdd.append(textFileLine)

    #I think it needs to decrement one since it counts a second one sometimes?
    #lineCount -= 1
    linesToAdd.insert(0, ['EventText', str(secondNumber), str(lineCount)])

    return linesToAdd


# Opens the file and generates a new text file with the same name as the csv
with open(fileName, 'r') as fileIn, open(f'{fileNameExtracted}TextFormatted.txt', 'w') as fileOut:
    csvContent = csv.reader(fileIn, delimiter=',')
    next(csvContent)  # Skip the header

    textToWrite = generateExtractedCSVArray(csvContent)

    for item in textToWrite:
        formattedString = '\t'.join(item) + '\n'
        fileOut.write(formattedString)

print("Script completed")
