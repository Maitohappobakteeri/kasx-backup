#!/usr/bin/env python3


from varmuuskopiot.environment import Environment
from varmuuskopiot import backup, config
import komento

import os
import argparse


def lue_argumentit():
    parser = argparse.ArgumentParser()
    parser.add_argument("kohde",
                        help="polku hakemistolle, josta varmuuskopio tuodaan")
    parser.add_argument("-t", "--testi", action="store_true",
                        help="testaa toimintaa, vain tulosta komennot")
    parser.add_argument("-f", "--vain-tiedostot", action="store_true",
                        help="aja rsync -n asetuksella")
    args = parser.parse_args()
    return args


def main():
    dateString = None

    args = lue_argumentit()
    onlyTest = args.testi
    dryRun = args.vain_tiedostot
    backupLocation = args.kohde

    if(not backupLocation[0] == "/"):
        print("varmuuskopion polun pitää alkaa /")
        return

    # os.chdir(workDir)
    try:
        local = backup.Local(os.getcwd())
        backp = backup.Backup(backupLocation)
    except RuntimeError:
        return

    if not local.can_sync_from(backp):
        return

    print("kopioidaan konfiguraatio tiedosto")
    backp.kopioi_konfiguraatio(local)

    dateString = backp.date_string()

    environment = Environment.current_environment()
    with open(config.configFilename, "r") as f:
        conf = config.Config(environment, f.read())
    print("konfiguraatio tiedosto luettu onnistuneesti")

    commands = komento.create_sync_commands(
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
        # TODO: Backup kirjoittaa oman notensa
        backup.write_note(backup.lockFilename, dateString)
        print("paikallinen kasx muokkausaikatiedosto päivitettiin")


if __name__ == "__main__":
    main()
