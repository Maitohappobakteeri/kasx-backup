#!/usr/bin/env python3

import os
import datetime
import sys

#files on full copy list are backed up without touching the old backup
fullCopyList = []
#files on one copy list will overwrite on the last save
oneCopyList = []

workDir = os.path.expanduser("~")
folderFilePath = "foldersToSync.txt"

fullCopyInstruction = "[SAVE ALL]"
oneCopyInstruction = "[ONE COPY]"

dateFormat = "%Y_%m_%d_%H_%M_%S"
currentTime = datetime.datetime.today()
dateString = currentTime.strftime(dateFormat)

backupLocation = sys.argv[1]

os.chdir(workDir)

with open(folderFilePath, "r") as f:

    lastInstruction = ""

    for line in f:
    
        if line[0] == " " or line[0] == "#":
        
            continue
    
        elif line[0] == "[":
        
            lastInstruction = line.rstrip().lstrip()
            print("inst: {}".format(line), end="")
            
        else:
        
            path = line.rstrip("\n")
            if not path:
                continue
        
            if lastInstruction == fullCopyInstruction:
            
                fullCopyList.append(path)
                
            elif lastInstruction == oneCopyInstruction:
            
                oneCopyList.append(path)
                
for path in fullCopyList:

    os.system("rsync -a --progress {0} {1}/FullCopy/{2}/".format(path, backupLocation, dateString))
    
for path in oneCopyList:

    os.system("rsync -a --progress {0} {1}/OneCopy/".format(path, backupLocation, dateString))
        
