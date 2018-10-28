#!/usr/bin/env python3


from varmuuskopiot import backup, config

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
    dateString = datetime.datetime.fromtimestamp(0).strftime(backup.dateFormat)

    args = lue_argumentit()
    onlyTest = args.testi
    backupLocation = args.kohde

    if(not backupLocation[0] == "/"):
        print("varmuuskopion polun pitää alkaa /")
        return

    if(os.path.isfile(os.path.join(backupLocation, backup.lockFilename))):
        print("kohteessa on jo kasx muokkausaikatiedosto")
        return

    with open(config.configFilename, "r") as f:
        conf = config.Config(f.read())

    print("konfiguraatio tiedosto luettu onnistuneesti")

    if not onlyTest:
        backup.write_note(os.path.join(backupLocation, backup.lockFilename),
                          dateString)
        print("kasx muokkausaikatiedosto luotiin")


if __name__ == "__main__":
    main()
