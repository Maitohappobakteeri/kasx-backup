
versio = (2, 3)
versioStr = "v{}.{}".format(*versio)


def versio_stringista(s):
    # TODO: Tarkistukset formaatille, regex?
    return tuple(int(n) for n in s[1:].split("."))


def string_versiosta(v):
    return "v{}.{}".format(*v)
