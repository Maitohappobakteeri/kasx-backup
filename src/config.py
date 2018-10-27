

import os


configFilename = ".kasx-backup.config"
commandCharacter = '!'
fullCopyCommand = "saveall"
oneCopyCommand = "onecopy"


class Config:
    def __init__(self, configString):
        #files on full copy list are backed up without touching the old backup
        self.fullCopyList = []
        #files on one copy list will overwrite on the last save
        self.oneCopyList = []

        command = ""

        for line in configString.split("\n"):
            #kommenttirivi
            if not line or line[0] == " " or line[0] == "#":
                continue
            #komentorivi
            elif line[0] == commandCharacter:
                command = line[1:].rstrip().lstrip().lower().replace(" ", "").replace("\t", "")
                if(command not in (fullCopyCommand, oneCopyCommand)):
                    print("invalid command: {}".format(command))
                    raise RuntimeError()
                    return
                print("command: {}".format(command))
            #polku
            else:
                path = line.rstrip("\n")
                if not path:
                    continue

                # if not os.path.exists(path):
                #     print("{} doesn't exist".format(path))
                #     raise RuntimeError()
                #     return
                # elif os.path.isdir(path):
                #     if not path[-1] == "/":
                #         #path += "/"
                #         pass

                if command == fullCopyCommand:
                    self.fullCopyList.append(path)
                elif command == oneCopyCommand:
                    self.oneCopyList.append(path)
