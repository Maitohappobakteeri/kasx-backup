#!/usr/bin/env python3


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

    dateString = backup.date_string()

    with open(config.configFilename, "r") as f:
        conf = config.Config(f.read())
    print("konfiguraatio tiedosto luettu onnistuneesti")

    fullCopyLahde = "{1}/full-copy/{2}/./{0}"
    oneCopyLahde = "{1}/one-copy/./{0}"

    for path in conf.fullCopyList:
        lahde = fullCopyLahde.format(path, backupLocation, dateString)
        komentoStr = komento.rsync_komento(lahde, "./", dryRun)

        print(komentoStr)
        if not onlyTest:
            os.system(komentoStr)

    for path in conf.oneCopyList:
        lahde = oneCopyLahde.format(path, backupLocation)
        komentoStr = komento.rsync_komento(lahde, "./", dryRun)

        print(komentoStr)
        if not onlyTest:
            os.system(komentoStr)

    if not onlyTest and not dryRun:
        # TODO: Backup kirjoittaa oman notensa
        backup.write_note(backup.lockFilename, dateString)
        print("paikallinen kasx muokkausaikatiedosto päivitettiin")


if __name__ == "__main__":
    main()
