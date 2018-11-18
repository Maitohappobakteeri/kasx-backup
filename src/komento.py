

from varmuuskopiot.backup import dateFormat as dateFormat


rsyncKomento = "rsync -R -a --delete --progress -o -g --omit-dir-times"


def rsync_komento(lahde, kohde, testiSuoritus):
    return rsyncKomento \
           + (" -n" if testiSuoritus else "") \
           + " {} {}".format(lahde, kohde)


def create_backup_commands(environment, config, local, backup, dryRun):
    fullCopyKohde = "{0}/full-copy/{1}/"
    oneCopyKohde = "{0}/one-copy/"

    commands = []

    if config.fullCopyList:
        fullCopyDir = fullCopyKohde.format(
            backup.path(), environment.date.strftime(dateFormat)
        )
        commands.append("mkdir -p {}".format(fullCopyDir))

    for path in config.fullCopyList:
        commands.append(rsync_komento(path, fullCopyDir, dryRun))

    for path in config.oneCopyList:
        kohde = oneCopyKohde.format(backup.path())
        commands.append(rsync_komento(path, kohde, dryRun))

    return commands
