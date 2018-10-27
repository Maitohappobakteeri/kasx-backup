
version = (2, 1)
versioStr = "v{}.{}".format(*version)


def version_from_string(s):
    # TODO: Tarkistukset formaatille, regex?
    return tuple(int(n) for n in s[1:].split("."))


def string_from_version(v):
    return "v{}.{}".format(*v)
