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


def lue_argumentit():
    parser = argparse.ArgumentParser()
    parser.add_argument("kohde", default=[], nargs="*",
                        help="polku hakemistolle")
    parser.add_argument("-v", "--versio", dest='toiminto', action="append_const",
                        const=Toiminto.TULOSTA_VERSIO, help="tulosta versio")
    args = parser.parse_args()
    return args


def main():
    args = lue_argumentit()

    if args.toiminto is None:
        print("Ei annettua toimintoa!")
        return
    elif len(args.toiminto) > 1:
        print("Liikaa toimintoja!")
        return

    if Toiminto.TULOSTA_VERSIO in args.toiminto:
        print("Asennettu versio: {}".format(version.versioStr))
    else:
        raise RuntimeError("Tuntematon toiminto = {}".format(args.toiminto[0]))


if __name__ == "__main__":
    main()
