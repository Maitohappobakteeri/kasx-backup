

rsyncKomento = "rsync -R -a --delete --progress -o -g --omit-dir-times"


def rsync_komento(lahde, kohde, testiSuoritus):
    return rsyncKomento \
           + (" -n" if testiSuoritus else "") \
           + " {} {}".format(lahde, kohde)
