#!/usr/bin/env python3

import os
import tempfile
import subprocess
import shutil


filesToInstall = [os.path.join("src", f) for f in [
    "kasx-backup.py",
    "kasx-init.py",
    "kasx-sync.py",
    "kasx-config.py",
    "versiot.py",
    "komento.py",
    "varmuuskopiot/__init__.py",
    "varmuuskopiot/backup.py",
    "varmuuskopiot/paivita.py",
    "varmuuskopiot/config.py",
    "varmuuskopiot/vaihtoehdot/valinta.py"
]]

suoritettavat = {
    "src/kasx-init.py": "kasx-init",
    "src/kasx-backup.py": "kasx-backup",
    "src/kasx-sync.py": "kasx-sync",
    "src/kasx-config.py": "kasx-config"
 }


def checkout_git(repoPath):
    print("Kloonataan repo")
    subprocess.run(["git", "clone", repoPath, "repo"])

    print("Checkout master haara")
    repo = os.path.join(os.getcwd(), "repo")
    os.chdir(repo)
    subprocess.run(["git", "checkout", "master"])

    return repo


def package(repoHakemisto):
    print("Kootaan asennettavia tiedostoja")
    paketointiHakemisto = os.path.join(os.getcwd(), "asennus")

    def tarkista_skipattavat(hakemisto, filut):
        skipattavat = []

        for filu in filut:
            kokoPolku = os.path.join(hakemisto, filu)
            relPolku = os.path.relpath(kokoPolku, repoHakemisto)

            def onko_sisalla(hakemisto, filu):
                return os.path.commonpath([relPolku, filu]) != relPolku

            if all(onko_sisalla(relPolku, f) for f in filesToInstall):
                skipattavat.append(filu)

        return skipattavat

    shutil.copytree(repoHakemisto, paketointiHakemisto,
                    ignore=tarkista_skipattavat)

    return paketointiHakemisto


def kopioi_kirjasto(paketointiHakemisto):
    print("Kopioidaan filut")
    asennusHakemisto = "/usr/local/lib/kasx-backup"

    if os.path.exists(asennusHakemisto):
        shutil.rmtree(asennusHakemisto)
    shutil.copytree(paketointiHakemisto, asennusHakemisto)

    return asennusHakemisto


def aseta_oikeudet(kirjastoHakemisto):
    print("Asetetaan tiedosto-oikeudet")
    os.chmod(kirjastoHakemisto, 0o755)
    for root, dirs, files in os.walk(kirjastoHakemisto):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o755)


def luo_linkit(kirjastoHakemisto):
    print("Luodaan linkit")
    binaariHakemisto = "/usr/local/bin"
    for filunNimi, linkinNimi in suoritettavat.items():
        filu = os.path.join(kirjastoHakemisto, filunNimi)
        linkki = os.path.join(binaariHakemisto, linkinNimi)

        if os.path.exists(linkki):
            os.remove(linkki)

        os.symlink(filu, linkki)


def install(paketointiHakemisto):
    print("Asennetaan")
    kirjastoHakemisto = kopioi_kirjasto(paketointiHakemisto)
    aseta_oikeudet(kirjastoHakemisto)
    luo_linkit(kirjastoHakemisto)


def main():
    repoPath = os.path.dirname(os.path.realpath(__file__))
    with tempfile.TemporaryDirectory() as dir:
        os.chdir(dir)
        repo = checkout_git(repoPath)
        os.chdir(dir)
        paketointiHakemisto = package(repo)
        os.chdir(dir)
        install(paketointiHakemisto)


if __name__ == "__main__":
    main()
