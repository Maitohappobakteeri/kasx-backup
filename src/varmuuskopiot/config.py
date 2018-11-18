

from varmuuskopiot.vaihtoehdot.valinta import Valinta
from varmuuskopiot.vaihtoehdot.valinta import Vaihtoehto

import os
import enum
import itertools
import more_itertools
import sys


configFilename = ".kasx-backup.config"
commandCharacter = '!'
fullCopyCommand = "saveall"
oneCopyCommand = "onecopy"
vaihtoehtoisetToiminto = "valinta"
lopetaToiminto = "lopeta"


class Lista(enum.Enum):
    AINA_UUSI = enum.auto()
    VAIN_YKSI = enum.auto()


class Config:
    def __init__(self, environment, configString):
        # files on full copy list are backed up without touching the old backup
        self.fullCopyList = []
        # files on one copy list will overwrite on the last save
        self.oneCopyList = []

        valittuLista = None
        komento = ""

        rivit = more_itertools.peekable(configString.split("\n"))
        for line in rivit:
            if not line:
                continue
            # kommenttirivi
            elif line[0] == "#":
                continue
            # komentorivi
            elif line[0] == commandCharacter:
                komento, *argumentit = line[1:].rstrip() \
                                  .lstrip() \
                                  .lower() \
                                  .replace("\t", " ") \
                                  .split()
                if(komento not in (fullCopyCommand, oneCopyCommand, vaihtoehtoisetToiminto)):
                    print("invalid command: {}".format(komento))
                    raise RuntimeError()
                print("komento: {}".format(komento))

                if komento == fullCopyCommand:
                    valittuLista = Lista.AINA_UUSI
                elif komento == oneCopyCommand:
                    valittuLista = Lista.VAIN_YKSI
                elif komento == vaihtoehtoisetToiminto:
                    valinta = Valinta(argumentit[0])
                    for vaihtoehto in lue_vaihtoehdot(rivit):
                        valinta.lisaa_vaihtoehto(vaihtoehto)
                    kohdepolku = valinta.valitse(environment)
                    if kohdepolku is not None:
                        if valittuLista is None:
                            print("saatiin polku ennen valittua listaa:", kohdepolku)
                            raise RuntimeError()

                        if valittuLista == Lista.AINA_UUSI:
                            self.fullCopyList.append(kohdepolku)
                        elif valittuLista == Lista.VAIN_YKSI:
                            self.oneCopyList.append(kohdepolku)
            # polku
            else:
                path = line.strip()
                if not path:
                    continue

                if valittuLista is None:
                    print("saatiin polku ennen valittua listaa:", path)
                    raise RuntimeError()

                if valittuLista == Lista.AINA_UUSI:
                    self.fullCopyList.append(path)
                elif valittuLista == Lista.VAIN_YKSI:
                    self.oneCopyList.append(path)

    def tarkista_tiedostot(self):
        for kohde in itertools.chain(self.fullCopyList, self.oneCopyList):
            if not os.path.exists(kohde):
                print("Kohde {} ei ole olemassa".format(kohde))
                return False
        return True


def create_option(enable, *args):
    if enable:
        conditionType, condition, path = args
    else:
        conditionType, condition = args
        path = None

    if not conditionType == "hostname":
        raise RuntimeError("unknown condition type", conditionType)

    return Vaihtoehto.hostname_option(enable, condition, path)


def lue_vaihtoehdot(rivit):
    actions = []

    while not len(rivit.peek().lstrip()) == 0 \
            and rivit.peek().lstrip()[0] == "|":
        rivi = next(rivit).rstrip()[1:]
        action, *tail = rivi.split()

        if action == "default":
            actions.append(Vaihtoehto.default_option(tail[0]))
        elif action in ["enable", "disable"]:
            actions.append(create_option(action == "enable", *tail))
        else:
            raise RuntimeError("unkown action for option", action)

    return actions


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        conf = Config(f.read())
        print("Fullcopy " + ", ".join(conf.fullCopyList))
        print("Onecopy " + ", ".join(conf.oneCopyList))
