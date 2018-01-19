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

    workDir = os.path.expanduser("~")
    folderFilePath = ".kasx-backup.config"
    lockFilename = ".kasx-backup-note"

    commandCharacter = '!'
    fullCopyCommand = "saveall"
    oneCopyCommand = "onecopy"

    dateFormat = "%Y_%m_%d_%H_%M_%S"
    dateString = None

    args = lue_argumentit()
    onlyTest = args.testi
    backupLocation = args.kohde
    
    if(not backupLocation[0] == "/"):
        print("varmuuskopion polun pitää alkaa /")
        return

    os.chdir(workDir)
    if(os.path.isfile(os.path.join(backupLocation, lockFilename))):
        if(os.path.isfile(lockFilename)):
            if(os.path.samefile(os.path.abspath(os.path.join(backupLocation, lockFilename)),
                                os.path.abspath(os.path.join(os.getcwd(), lockFilename)))):
                print("virheellinen kohde: sama polku")
                return
            else:
                print("löytyi molemmat kasx muokkausaikatiedostot")
                if(backup.read_note_time(os.path.join(backupLocation, lockFilename)) <= backup.read_note_time(lockFilename)):
                    print("paikallinen kasx muokkausaikatiedosto on uudempi")
                    print("selvitä tämä käsin")
                    return
                else:
                    print("kasx muokkausaikatiedostotojen vertailu onnistui")
        else:
            print("varmuuskopiota ei ole synkronoitu aikaisemmin")
    else:
        print("varmuuskopio kohteesta puuttuu kasx muokkausaikatiedosto")
        return

    dateString = backup.read_note_date(os.path.join(backupLocation, lockFilename))

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
                if command == fullCopyCommand:
                    fullCopyList.append(path)
                elif command == oneCopyCommand:
                    oneCopyList.append(path)
    print("konfiguraatio tiedosto luettu onnistuneesti")
                    
    for path in fullCopyList:
        if(onlyTest):
            print("rsync -a --delete --progress {1}/FullCopy/{2}/{0} {0}".format(path, backupLocation, dateString))
        else:
            raise RuntimeError("oh no");
            os.system("rsync -a --delete --progress {1}/FullCopy/{2}/{0} {0}".format(path, backupLocation, dateString))
        
    for path in oneCopyList:
        if(onlyTest):
            print("rsync -a --delete --progress {1}/OneCopy/{0} {0}".format(path, backupLocation, dateString))
        else:
            raise RuntimeError("oh no");
            os.system("rsync --delete -a --progress {1}/OneCopy/{0} {0}".format(path, backupLocation, dateString))
   
    if not onlyTest or True:
        backup.write_note(lockFilename, dateString)
        
        
if __name__ == "__main__":
    main()         
