#!/usr/bin/env python3


from varmuuskopiot.environment import Environment
from varmuuskopiot import backup, config
import komento

import os
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
    environment = Environment.current_environment()
    dateString = environment.date.strftime(backup.dateFormat)

    args = lue_argumentit()
    onlyTest = args.testi
    dryRun = args.vain_tiedostot
    backupLocation = args.kohde

    if(not backupLocation[0] == "/"):
        print("varmuuskopion polun pitää alkaa /")
        return

    try:
        local = backup.Local(os.getcwd())
        backp = backup.Backup(backupLocation)
    except RuntimeError:
        return

    if not local.can_backup_into(backp):
        return

    if not os.path.isfile(config.configFilename):
        print("{} ei ole olemassa".format(config.configFilename))
        return

    conf = local.read_config(environment)

    if not conf.tarkista_tiedostot():
        return

    if not onlyTest and not dryRun:
        print("kopioidaan konfiguraatio tiedosto")
        local.kopioi_konfiguraatio(backp)

    print("konfiguraatio tiedosto luettu onnistuneesti")

    commands = komento.create_backup_commands(
        environment,
        conf,
        local,
        backp,
        dryRun
    )

    for command in commands:
        print(command)
        if not onlyTest:
            os.system(command)

    if not onlyTest and not dryRun:
        backup.write_note(os.path.join(backupLocation, backup.lockFilename),
                          dateString, True)
        backup.write_note(backup.lockFilename, dateString)
        print("molemmat kasx muokkausaikatiedostot päivitettiin")


if __name__ == "__main__":
    main()
