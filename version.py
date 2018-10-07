
version = (2, 0)
versioStr = "v{}.{}".format(*version)


def version_from_string(s):
    # TODO: Tarkistukset formaatille, regex?
    return tuple(int(n) for n in s[1:].split("."))
