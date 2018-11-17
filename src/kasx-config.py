#!/usr/bin/env python3


from varmuuskopiot import backup, paivita
import versiot

import os
import argparse
import enum
import datetime


class Toiminto(enum.Enum):
    TULOSTA_VERSIO = enum.auto()
    PAIVITA = enum.auto()
    PRINT_TIME = enum.auto()


def lue_argumentit():
    parser = argparse.ArgumentParser()
    parser.add_argument("kohde", default=[], nargs="*",
                        help="polku hakemistolle")
    parser.add_argument("-v", "--versio", dest='toiminto',
                        action="append_const", const=Toiminto.TULOSTA_VERSIO,
                        help="tulosta versio")
    parser.add_argument("-u", "--paivita", dest='toiminto',
                        action="append_const", const=Toiminto.PAIVITA,
                        help="päivitä lähde tai kohde")
    parser.add_argument("-t", "--get-time", dest='toiminto',
                        action="append_const", const=Toiminto.PRINT_TIME,
                        help="print when has last sync happened")
    args = parser.parse_args()
    return args


def tulosta_versio(polut):
    if len(polut) == 0:
        print("Asennettu versio:", versiot.versioStr)
    elif len(polut) == 1:
        try:
            notenPolku = polut[0]
            note = backup.Note(os.path.join(notenPolku, backup.lockFilename),
                               False)
            print("Versio:", note.version)
        except RuntimeError as e:
            print(e)
    else:
        print("Liian monta polkua version tulostukselle!")
        return


def paivita_(polut):
    if len(polut) == 0:
        polku = os.getcwd()
    elif len(polut) == 1:
        polku = polut[0]
    else:
        print("Liian monta polkua päivitykselle!")
        return

    try:
        paivita.paivita(polku, versiot.versio)
    except RuntimeError as e:
        print(e)
        return


def print_sync_time_(polut):
    if len(polut) == 0:
        path = os.getcwd()
    elif len(polut) == 1:
        path = polut[0]
    else:
        print("Too many paths given for get-time!")
        return

    try:
        note = backup.Note(os.path.join(path, backup.lockFilename), False)
        time = datetime.datetime.strptime(note.dateString, backup.dateFormat)
        print(time.isoformat())
    except RuntimeError as e:
        print(e)


def main():
    args = lue_argumentit()

    if args.toiminto is None:
        print("Ei annettua toimintoa!")
        return
    elif len(args.toiminto) > 1:
        print("Liikaa toimintoja!")
        return

    if Toiminto.TULOSTA_VERSIO in args.toiminto:
        return tulosta_versio(args.kohde)
    elif Toiminto.PAIVITA in args.toiminto:
        return paivita_(args.kohde)
    elif Toiminto.PRINT_TIME in args.toiminto:
        return print_sync_time_(args.kohde)
    else:
        raise RuntimeError("Tuntematon toiminto = {}".format(args.toiminto[0]))


if __name__ == "__main__":
    main()
