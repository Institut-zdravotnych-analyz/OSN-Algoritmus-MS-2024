import re


def zjednot_kod(kod):
    return re.sub("[^0-9a-zA-Z]", "", kod).lower()


def zjednot_zoznam_kodov(zoznam_kodov):
    return ", ".join(
        [
            "-".join(zjednot_kod(kod) for kod in kody.split("-"))
            for kody in zoznam_kodov.split(", ")
        ]
    )
