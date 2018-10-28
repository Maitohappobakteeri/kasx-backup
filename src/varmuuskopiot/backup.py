
import versiot

import json
import os
import datetime


dateFormat = "%Y_%m_%d_%H_%M_%S"
lockFilename = ".kasx-backup-note"


def write_note(filename, dateString, canSync=False):
    with open(filename, "w") as notefile:
        json.dump({"dateString": dateString,
                   "version": versiot.versioStr,
                   "canSync": canSync},
                  notefile)


def write_note_with_version(filename, dateString, v, canSync):
    with open(filename, "w") as notefile:
        json.dump({"dateString": dateString, "version": v, "canSync": canSync},
                  notefile)


def read_note_time(filename):
    date = datetime.datetime.strptime(read_note_date(filename), dateFormat)
    return date.timestamp()


def read_note_date(filename):
    with open(filename, "r") as notefile:
        return json.load(notefile)["dateString"]


def read_note_valid_sync(filename):
    with open(filename, "r") as notefile:
        note = json.load(notefile)
        return note["canSync"]


class Note:
    def __init__(self, filename, vaadiVersio=True):
        with open(filename, "r") as notefile:
            noteDict = json.load(notefile)

        v = versiot.versio_stringista(noteDict["version"])

        if vaadiVersio:
            if v < versiot.versio:
                print("Virhe: aja migraatiot notelle: {}".format(filename))
                raise RuntimeError()
            if v > versiot.versio:
                print("Virhe: päivitä kasx-backup versioon: {}"
                      .format(versiot.string_versiosta(v)))
                raise RuntimeError()

        self.dateString = noteDict["dateString"]
        self.version = noteDict["version"]
        self.canSync = noteDict["canSync"]

    def timestamp(self):
        return datetime.datetime \
               .strptime(self.dateString, dateFormat) \
               .timestamp()


class DataSource_:
    def __init__(self, path, isLocal):
        self.path_ = path
        self.isLocal_ = isLocal

        try:
            self.note_ = Note(os.path.join(self.path_, lockFilename))
        except OSError:
            if not isLocal:
                raise RuntimeError()
            else:
                print("aja kasx-init hakemistolle", path)
                raise RuntimeError()

    def is_local(self):
        return self.isLocal_

    def is_backup(self):
        return not self.is_local()

    def is_same(self, dsource):
        return os.path.samefile(os.path.abspath(self.path_),
                                os.path.abspath(dsource.path_))

    def path(self):
        return self.path_

    def timestamp(self):
        return self.note_.timestamp()


class Local(DataSource_):
    def __init__(self, path):
        super().__init__(path, True)

    def can_sync_from(self, backup):
        if self.note_ is not None and self.is_same(backup):
            print("virheellinen kohde: sama polku")
            return False
        elif not backup.is_backup():
            print("kohde ei ole varmuuskopio")
            return False
        elif not backup.can_sync():
            print("kohteeseen ei ole luotu vielä kopiota")
            return False
        elif self.note_ is not None and backup.timestamp() <= self.timestamp():
            if backup.timestamp() < self.timestamp():
                print("paikallinen kasx muokkausaikatiedosto on uudempi")
            elif backup.timestamp() == self.timestamp():
                print("kasx muokkausaikatiedostojen aika on sama")

            if not backup.can_sync():
                print("kohteeseen ei ole luotu vielä kopiota")

            return False
        else:
            return True

    def can_backup_into(self, backup):
        if self.is_same(backup):
            print("virheellinen kohde: sama polku")
            return False
        elif not backup.is_backup():
            print("kohde ei ole varmuuskopio")
            return False
        elif backup.timestamp() > self.timestamp():
            print("varmuuskopion kasx muokkausaikatiedosto on uudempi")
            print("synkronoi muutokset viimeisimmästä kopiosta")
            return False
        else:
            return True


class Backup(DataSource_):
    def __init__(self, path):
        try:
            super().__init__(path, False)
        except RuntimeError:
            print("varmuuskopio kohteesta puuttuu kasx muokkausaikatiedosto")
            raise RuntimeError()

    def can_sync(self):
        return self.note_.canSync