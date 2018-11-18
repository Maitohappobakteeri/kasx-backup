

from varmuuskopiot.backup import dateFormat as dateFormat

import os


rsyncKomento = "rsync -a --delete --progress -o -g --omit-dir-times"


def rsync_komento(lahde, kohde, testiSuoritus):
    return rsyncKomento \
           + (" -n" if testiSuoritus else "") \
           + " {} {}".format(lahde, kohde)


def create_backup_commands(environment, config, local, backup, dryRun):
    fullCopyKohde = "{0}/full-copy/{1}/"
    oneCopyKohde = "{0}/one-copy/"

    commands = []

    if config.fullCopyList:
        fullCopyDir = os.path.normpath(fullCopyKohde.format(
            backup.path(), environment.date.strftime(dateFormat)
        ))
        commands.append("mkdir -p {}".format(fullCopyDir))

    for path in config.fullCopyList:
        localPath = os.path.normpath(path[0]) \
            if not path[0][-1] == "/" \
            else os.path.normpath(path[0]) + "/"

        backupPath = os.path.normpath(os.path.join(fullCopyDir, path[1]))
        backupPathDirName = os.path.dirname(backupPath)
        if not backupPathDirName == fullCopyDir:
            commands.append("mkdir -p {}".format(backupPathDirName))
        commands.append(rsync_komento(localPath, backupPath, dryRun))

    if config.oneCopyList:
        oneCopyDir = os.path.normpath(oneCopyKohde.format(backup.path()))
        commands.append("mkdir -p {}".format(oneCopyDir))

    for path in config.oneCopyList:
        localPath = os.path.normpath(path[0]) \
            if not path[0][-1] == "/" \
            else os.path.normpath(path[0]) + "/"

        backupPath = os.path.normpath(os.path.join(oneCopyDir, path[1]))
        backupPathDirName = os.path.dirname(backupPath)
        if not backupPathDirName == oneCopyDir:
            commands.append("mkdir -p {}".format(backupPathDirName))
        commands.append(rsync_komento(localPath, backupPath, dryRun))

    return commands


def create_sync_commands(environment, config, local, backup, dateString, dryRun):
    fullCopyLahde = "{0}/full-copy/{1}/"
    oneCopyLahde = "{0}/one-copy/"

    commands = []

    # TODO: Convert date to dateString here?
    fullCopyDir = os.path.normpath(fullCopyLahde.format(
        backup.path(), dateString
    ))

    for path in config.fullCopyList:
        localPath = os.path.normpath(path[0])

        backupPath = os.path.normpath(os.path.join(fullCopyDir, path[1]))
        backupPath = backupPath \
            if not path[0][-1] == "/" \
            else backupPath + "/"

        localPathDirName = os.path.dirname(localPath)
        if localPathDirName:
            commands.append("mkdir -p {}".format(localPathDirName))
        commands.append(rsync_komento(backupPath, localPath, dryRun))

    oneCopyDir = os.path.normpath(oneCopyLahde.format(backup.path()))

    for path in config.oneCopyList:
        localPath = os.path.normpath(path[0])

        backupPath = os.path.normpath(os.path.join(oneCopyDir, path[1]))
        backupPath = backupPath \
            if not path[0][-1] == "/" \
            else backupPath + "/"

        localPathDirName = os.path.dirname(localPath)
        if localPathDirName:
            commands.append("mkdir -p {}".format(localPathDirName))
        commands.append(rsync_komento(backupPath, localPath, dryRun))

    return commands
