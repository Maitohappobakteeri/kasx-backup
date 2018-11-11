

import socket


def gethostname():
    return socket.gethostname()


class Vaihtoehto:
    def __init__(self, ehto, kohdepolku):
        self.kohdepolku = kohdepolku
        self.ehto = ehto

    @staticmethod
    def luo_hostname_ehto(hostname, kohdepolku):
        return Vaihtoehto((lambda x: gethostname() == hostname), kohdepolku)


class Valinta:
    def __init__(self, nimi):
        self.nimi = nimi
        self.vaihtoehdot = []

    def lisaa_vaihtoehto(self, vaihtoehto):
        self.vaihtoehdot.append(vaihtoehto)

    def valitse(self):
        return next((v.kohdepolku for v in self.vaihtoehdot if v.ehto(None)), None)
