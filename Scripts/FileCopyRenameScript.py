'''
FileCopyRenameScript.py
By: Lilypad33

This script takes the contents of a directory (sourceDir) where all the file names are in the following format:

FileNumber-FileName
(i.e. 4545-MyFileName)

and copies the contents to the destination directory (destDir) with the names being in the following format:
FileNumber - FileName
(i.e. 4545 - MyFileName)

'''

import os
import shutil

# User input
sourceDir = input("Give the source directory: ")
destDir = input("Give the destination directory: ")

# Counting the number of the files copied
fileCount = 0

# For every file in the source directory
for filename in os.listdir(sourceDir):
    filenameSplit = filename.split("-")

    # Some files don't follow the expected convention, without filenameSplit[1], so the try/except block will catch that.
    try:
        newFileName = f"{filenameSplit[0]} - {filenameSplit[1]}"
    except IndexError:
            newFileName = f"{filenameSplit[0]}"

    fullSourcePath = f"{sourceDir}/{filename}"

    # Creates the new filepath with the destination directory and the newFileName
    new_path = f"{destDir}/{newFileName}"

    # Copies the file from the source directory to the destination
    shutil.copy(fullSourcePath, new_path)

    print(f"Copied {fullSourcePath} to {new_path}")

    fileCount += 1


print(f"Successfully copied {fileCount} files from {sourceDir} to {destDir}.")