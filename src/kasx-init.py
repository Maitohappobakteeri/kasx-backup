#!/usr/bin/env python3


from varmuuskopiot.environment import Environment
from varmuuskopiot import backup, config

import os
import datetime
import argparse


def lue_argumentit():
    parser = argparse.ArgumentParser()
    parser.add_argument("kohde",
                        help="polku hakemistolle, josta varmuuskopio tuodaan")
    parser.add_argument("-t", "--testi", action="store_true",
                        help="testaa toimintaa, vain tulosta komennot")
    parser.add_argument("-k", "--konfig",
                        help="malli konfiguraation sisältävä hakemisto")
    args = parser.parse_args()
    return args


def main():
    dateString = datetime.datetime.fromtimestamp(0).strftime(backup.dateFormat)

    # TODO: Uudelleennimeä backupLocation
    args = lue_argumentit()
    onlyTest = args.testi
    backupLocation = args.kohde
    malliKonfiguraatio = args.konfig

    if(not backupLocation[0] == "/"):
        print("varmuuskopion polun pitää alkaa /")
        return

    if not os.path.isdir(backupLocation):
        print("kohde ei ole olemassa")
        return

    if(os.path.isfile(os.path.join(backupLocation, backup.lockFilename))):
        print("kohteessa on jo kasx muokkausaikatiedosto")
        return

    if malliKonfiguraatio is None:
        konfigTiedostonimi = os.path.join(backupLocation,
                                          config.configFilename)
    else:
        konfigTiedostonimi = os.path.join(malliKonfiguraatio,
                                          config.configFilename)

    if not os.path.isfile(konfigTiedostonimi):
        print("{} ei ole olemassa".format(konfigTiedostonimi))
        return

    # Testataan vain konffin oikea muoto
    environment = Environment.current_environment()
    with open(konfigTiedostonimi, "r") as f:
        config.Config(environment, f.read())

    if malliKonfiguraatio is not None:
        print("kopioidaan konfiguraatio tiedosto")
        backup.kopioi_konfiguraatio(malliKonfiguraatio, backupLocation)

    print("konfiguraatio tiedosto luettu onnistuneesti")

    if not onlyTest:
        backup.write_note(os.path.join(backupLocation, backup.lockFilename),
                          dateString)
        print("kasx muokkausaikatiedosto luotiin")


if __name__ == "__main__":
    main()
