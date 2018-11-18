

class Vaihtoehto:
    def __init__(self, enable, ehto, kohdepolku):
        self.kohdepolku = kohdepolku
        self.ehto = ehto
        self.enable = enable

    @staticmethod
    def hostname_option(enable, hostname, path):
        return Vaihtoehto(enable, (lambda env: env.hostname == hostname), path)

    @staticmethod
    def default_option(path):
        return Vaihtoehto(True, (lambda env: True), path)


class Valinta:
    def __init__(self, backupPath):
        self.backupPath = backupPath
        self.vaihtoehdot = []

    def lisaa_vaihtoehto(self, vaihtoehto):
        self.vaihtoehdot.append(vaihtoehto)

    def valitse(self, environment):
        choice = None

        for option in self.vaihtoehdot:
            if option.ehto(environment):
                if option.enable and not choice:
                    choice = option.kohdepolku
                else:
                    choice = None

        return (choice, self.backupPath) if choice else None
