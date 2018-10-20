#!/usr/bin/env python3


import backup

import os
import datetime
import sys
import argparse


def lue_argumentit():
    parser = argparse.ArgumentParser()
    parser.add_argument("kohde", 
                        help="polku hakemistolle, josta varmuuskopio tuodaan")
    parser.add_argument("-t", "--testi", action="store_true",
                        help="testaa toimintaa, vain tulosta komennot")
    args = parser.parse_args()
    return args
    

def main():
    #files on full copy list are backed up without touching the old backup
    fullCopyList = []
    #files on one copy list will overwrite on the last save
    oneCopyList = []

    #workDir = os.path.expanduser("~")
    folderFilePath = ".kasx-backup.config"
    lockFilename = ".kasx-backup-note"

    commandCharacter = '!'
    fullCopyCommand = "saveall"
    oneCopyCommand = "onecopy"

    dateFormat = "%Y_%m_%d_%H_%M_%S"
    dateString = datetime.datetime.fromtimestamp(0).strftime(dateFormat)

    args = lue_argumentit()
    onlyTest = args.testi
    backupLocation = args.kohde
    
    if(not backupLocation[0] == "/"):
        print("varmuuskopion polun pitää alkaa /")
        return

    #os.chdir(workDir)
    if(os.path.isfile(os.path.join(backupLocation, lockFilename))):
        print("varmuuskopio kohteessa on jo kasx muokkausaikatiedosto")
        return

    with open(folderFilePath, "r") as f:
        command = ""

        for line in f:
            #kommenttirivi
            if line[0] == " " or line[0] == "#":
                continue
            #komentorivi
            elif line[0] == commandCharacter:
                command = line[1:].rstrip().lstrip().lower().replace(" ", "").replace("\t", "")
                if(command not in (fullCopyCommand, oneCopyCommand)):
                    print("invalid command: {}".format(command))
                    return
                print("command: {}".format(command))
            #polku
            else:
                path = line.rstrip("\n")
                if not path:
                    continue
                    
                if not os.path.exists(path):
                    print("{} doesn't exist".format(path))
                    return
                elif os.path.isdir(path):
                    if not path[-1] == "/":
                        path += "/"

                if command == fullCopyCommand:
                    fullCopyList.append(path)
                elif command == oneCopyCommand:
                    oneCopyList.append(path)
    print("konfiguraatio tiedosto luettu onnistuneesti")
  
    if not onlyTest:
        backup.write_note(os.path.join(backupLocation, lockFilename), dateString)
        print("varmuuskopion kasx muokkausaikatiedosto luotiin")
        
        
if __name__ == "__main__":
    main()         
