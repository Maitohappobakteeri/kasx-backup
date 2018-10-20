#!/usr/bin/env python3


import backup
import version

import os
import datetime
import sys
import argparse
import enum


class Toiminto(enum.Enum):
    TULOSTA_VERSIO = enum.auto()
    PAIVITA = enum.auto()


def lue_argumentit():
    parser = argparse.ArgumentParser()
    parser.add_argument("kohde", default=[], nargs="*",
                        help="polku hakemistolle")
    parser.add_argument("-v", "--versio", dest='toiminto', action="append_const",
                        const=Toiminto.TULOSTA_VERSIO, help="tulosta versio")
    parser.add_argument("-u", "--paivita", dest='toiminto', action="append_const",
                        const=Toiminto.PAIVITA, help="päivitä lähde tai kohde")
    args = parser.parse_args()
    return args


def tulosta_versio(polut):
    if len(polut) == 0:
        print("Asennettu versio:", version.versioStr)
    elif len(polut) == 1:
        try:
            notenPolku = polut[0]
            note = backup.Note(os.path.join(notenPolku, backup.lockFilename))
            print("Versio:", note.version)
        except RuntimeError as e:
            print(e)
    else:
        print("Liian monta polkua version tulostukselle!")
        return


def paivita(polut):
    if len(polut) == 0:
        polku = os.getcwd()
    elif len(polut) == 1:
        polku = polut[0]
    else:
        print("Liian monta polkua päivitykselle!")
        return

    try:
        note = backup.Note(os.path.join(polku, backup.lockFilename))
    except RuntimeError as e:
        print(e)
        return

    print("Päivitetään {} -> {}".format(note.version, version.versioStr))
    print("Ei toteutettu!")


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
        return paivita(args.kohde)
    else:
        raise RuntimeError("Tuntematon toiminto = {}".format(args.toiminto[0]))


if __name__ == "__main__":
    main()