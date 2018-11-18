

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


def create_sync_commands(environment, config, local, backup, dryRun):
    fullCopyLahde = "{1}/full-copy/{2}/./{0}"
    oneCopyLahde = "{1}/one-copy/./{0}"

    commands = []

    for path in config.fullCopyList:
        lahde = fullCopyLahde.format(
            path,
            backup.path(),
            environment.date.strftime(dateFormat)
        )
        commands.append(rsync_komento(lahde, "./", dryRun))

    for path in config.oneCopyList:
        lahde = oneCopyLahde.format(path, backup.path())
        commands.append(rsync_komento(lahde, "./", dryRun))

    return commands
