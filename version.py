
oikeaVersio = (1, 0)
version = 100 * oikeaVersio[0] + oikeaVersio[1]
versioStr = "v{}.{}".format(*oikeaVersio)


def versio_stringi(lukuEsitys):
    return "v{}.{}".format(lukuEsitys // 100, lukuEsitys % 100)
