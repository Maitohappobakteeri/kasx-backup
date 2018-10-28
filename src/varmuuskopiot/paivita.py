

import versiot
from varmuuskopiot import backup

import os


def paivita(hakemisto, uusiVersio):
    note = backup.Note(os.path.join(hakemisto, backup.lockFilename), False)
    vanhaVersio = versio = versiot.versio_stringista(note.version)

    if versio == uusiVersio:
        print("Versio on jo haluttu")

    while not versio == uusiVersio:
        if versio not in paivitykset_:
            print("Virhe! Ei päivitystä, joka toimisi versioon", versio)
            return False

        versio, onnistuiko = paivitykset_[versio](hakemisto)

        if not onnistuiko:
            print("Virhe! Päivitys epäonnistui")
            return False

        if versio > uusiVersio:
            print("Virhe! Päivitettiin halutun version ohi")
            return False

    return True


paivitykset_ = {}


class Paivitys:
    def __init__(self, vanhaVersio, uusiVersio):
        self.vanhaVersio_ = vanhaVersio
        self.uusiVersio_ = uusiVersio

    def __call__(self, paivitysFunktio):
        global paivitykset_

        # print("Alustetaan päivitys {} -> {}".format(
        #     version.string_from_version(self.vanhaVersio_),
        #     version.string_from_version(self.uusiVersio_)
        # ))

        def palautaVersio(hakemisto):
            print("Päivitetään versio {} -> {}".format(
                versiot.string_versiosta(self.vanhaVersio_),
                versiot.string_versiosta(self.uusiVersio_)
            ))

            try:
                onnistuiko = paivitysFunktio(hakemisto)
            except Exception as e:
                print(e)
                onnistuiko = False

            return (self.uusiVersio_, onnistuiko)

        paivitykset_[self.vanhaVersio_] = palautaVersio
        return palautaVersio


@Paivitys((2, 1), (2, 2))
def paivita_2_1_to_2_2_(hakemisto):
    return tyhja_paivitys_2_1_(hakemisto, (2, 2))


@Paivitys((2, 2), (2, 3))
def paivita_2_2_to_2_3_(hakemisto):
    return tyhja_paivitys_2_1_(hakemisto, (2, 3))


@Paivitys((2, 3), (2, 4))
def paivita_2_3_to_2_4_(hakemisto):
    return tyhja_paivitys_2_1_(hakemisto, (2, 4))


@Paivitys((2, 4), (2, 5))
def paivita_2_4_to_2_5_(hakemisto):
    return tyhja_paivitys_2_1_(hakemisto, (2, 5))


@Paivitys((2, 5), (2, 6))
def paivita_2_5_to_2_6_(hakemisto):
    return tyhja_paivitys_2_1_(hakemisto, (2, 6))


def tyhja_paivitys_2_1_(hakemisto, uusiVersio):
    print("Ei muutoksia, nostetaan vain versiota")

    note = backup.Note(os.path.join(hakemisto, backup.lockFilename), False)
    noteFilunimi = os.path.join(hakemisto, backup.lockFilename)
    backup.write_note_with_version(noteFilunimi,
                                   note.dateString,
                                   versiot.string_versiosta(uusiVersio),
                                   note.canSync)

    return True


if __name__ == "__main__":
    print("Testi",
          "onnistui" if paivita(os.getcwd(), (2, 2)) else "epäonnistui")
