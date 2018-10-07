#!/usr/bin/env python3


import backup

import os
import datetime
import sys
import argparse


def lue_argumentit():
    parser = argparse.ArgumentParser()
    parser.add_argument("kohde",
                        help="polku hakemistolle, johon varmuuskopio tehdään")
    parser.add_argument("-t", "--testi", action="store_true",
                        help="testaa toimintaa, vain tulosta komennot")
    parser.add_argument("-f", "--vain-tiedostot", action="store_true",
                        help="aja rsync -n asetuksella")
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
    currentTime = datetime.datetime.today()
    dateString = currentTime.strftime(dateFormat)

    args = lue_argumentit()
    onlyTest = args.testi
    dryRun = args.vain_tiedostot
    backupLocation = args.kohde

    if(not backupLocation[0] == "/"):
        print("varmuuskopion polun pitää alkaa /")
        return

    #os.chdir(workDir)
    try:
        local = backup.Local(os.getcwd())
        backp = backup.Backup(backupLocation)
    except RuntimeError:
        return

    if not local.can_backup_into(backp):
        return

    if not os.path.isfile(folderFilePath):
        print("{} ei ole olemassa".format(folderFilePath))
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
                        #path += "/"
                        pass

                if command == fullCopyCommand:
                    fullCopyList.append(path)
                elif command == oneCopyCommand:
                    oneCopyList.append(path)
    print("konfiguraatio tiedosto luettu onnistuneesti")

    rsyncKomento = "rsync -R -a --delete --progress -o -g --omit-dir-times "
    if dryRun:
        rsyncKomento += "-n "

    komentoFullCopy = rsyncKomento + " {0} {1}/full-copy/{2}/"
    komentoOneCopy = rsyncKomento + " {0} {1}/one-copy/"

    for path in fullCopyList:
        if(onlyTest):
            print(komentoFullCopy.format(path, backupLocation, dateString))
        else:
            os.system(komentoFullCopy.format(path, backupLocation, dateString))

    for path in oneCopyList:
        if(onlyTest):
            print(komentoOneCopy.format(path, backupLocation, dateString))
        else:
            os.system(komentoOneCopy.format(path, backupLocation, dateString))

    if not onlyTest and not dryRun:
        backup.write_note(os.path.join(backupLocation, lockFilename), dateString, True)
        backup.write_note(lockFilename, dateString)
        print("molemmat kasx muokkausaikatiedostot päivitettiin")

if __name__ == "__main__":
    main()
