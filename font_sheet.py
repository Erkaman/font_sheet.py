# escape character is slash:
# convert -font /Library/Fonts/Comic\ Sans\ MS.ttf -background blue   -size 64x64 -gravity center  label:"\@" at.png
# http://forum.devmaster.net/t/spritesheet-animation-in-opengl/24020

import platform
import os
import string
import subprocess
import sys

# these are the sizes of the characters.
LETTER_WIDTH = 64
LETTER_HEIGHT = 64

# the fontshoot is written to this file
OUT_FILE = "out.png"

# how characters are put per column in the sheet.
FONT_SHEET_COLS = 16

def log(s):
    print s

def delete_filelist(filelist):
    for f in filelist:
        os.remove(f)

# now clean up all the temp files created.
def cleanup(rowFiles, charFiles):
    delete_filelist(rowFiles)
    delete_filelist(charFiles)

counter = 0

def generateTempFile():
    global counter
    f =  "temp{0}.png".format(counter)
    counter = counter + 1
    return f

# open a file. I have only tested this function on OS X,
# so it may break on other platforms...
def open_file(file):
    if platform.system() ==('linux'): # linux
        subprocess.call(["xdg-open", file])
    elif platform.system() == "Darwin": # os x
        subprocess.call(["open", file])
    else:
        os.startfile(file)

def makeChar(char):

    outFile =  generateTempFile()
    # some characters will have to be escaped.
    if "@" == char:
        char = "\\@"
    elif char == '"':
        char = '\\"'
    elif ord(char) == 96:
        char = '\`'
    elif ord(char) == 92:
        char = "\\\\\\\\"

    command = 'convert -font /Library/Fonts/Comic\ Sans\ MS.ttf -background blue   -size {0}x{1} -gravity center  label:"{2}" {3}'.format(LETTER_WIDTH, LETTER_HEIGHT, char, outFile)
    log(command)

    os.system(command)
    return outFile

def makeRow(rowNum, files):
    outFile = "row{0}.png".format(rowNum)


    filesStr = ' '.join(files)

    command = "convert +append {0} {1}".format(filesStr, outFile)
    log(command)

    os.system(command)
    return outFile


charFiles = []

# generate images of all the desired characters.
for i in range(32, 127):
    charFiles.append(makeChar(chr(i)))


# next, we combine all the generated characters images into a montage, thus making a sprite sheet of the characters.

charListStr = ""

for char in charFiles:
    charListStr = charListStr + char + " "

cols = FONT_SHEET_COLS
rows = len(charFiles) / cols + 1 # use upwards rounding!

# divide the list into rows, and makes images for all the rows.

rowFiles = []

for row in range(0, rows):
    beg = row * cols
    e = ((row+1) * cols)

    subList = charFiles[beg:e]

    rowFile = makeRow(row, subList)
    rowFiles.append(rowFile)


command = "convert -append {0} {1}".format(' '.join(rowFiles), OUT_FILE)
log(command)
os.system(command)


# we will attempt to pad the fontsheet horizintally,
# so that its height is a power of two.
blankChar = makeChar(chr(32))

desired_height = LETTER_HEIGHT * FONT_SHEET_COLS
current_height = LETTER_HEIGHT * len(rowFiles)

while current_height < desired_height:

    command = "convert -append {0} {1} {2}".format(OUT_FILE, blankChar, OUT_FILE)
    log(command)
    os.system(command)
    current_height = current_height + LETTER_HEIGHT

open_file(OUT_FILE)

cleanup(rowFiles, charFiles)
