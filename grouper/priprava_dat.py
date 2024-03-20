import csv
import uuid

NAZVY_STLPCOV = [
    "id",
    "vek",
    "vek_dni",
    "hmotnost",
    "umela_plucna_ventilacia",
    "diagnozy",
    "vykony",
    "odbornosti",
    "drg",
]


def validuj_hp(hp, iza):
    """
    Funkcia na validáciu hospitalizačného prípadu.

    Skontroluje, či hospitalizačný prípad obsahuje neprázdne ID, platný vek, platný vek v dňoch, platnú hmotnosť, platný počet hodín umelej pľúcnej ventilácie a neprázdny zoznam diagnóz.

    Args:
        hp (dict): Hospitalizačný prípad, ktorý sa má validovať.
        iza (bool): Príznak určujúci, či sa pracuje v IZA móde.

    Returns:
        bool: True, ak je hospitalizačný prípad platný, False inak.
    """

    # Identifikátor hospitalizačného prípadu nesmie byť prázdny
    if hp["id"] == "":
        if not iza:
            return False
        hp["id"] = uuid.uuid4().hex
        print(f'WARNING: Prázdne pole "id", priraďujem nové ID: {hp["id"]}')

    # Vek musí byť celé číslo
    try:
        hp["vek"] = int(hp["vek"])
    except ValueError:
        if not iza:
            return False
        print(f'WARNING: HP {hp["id"]} nemá správne vyplnený vek.')
        hp["vek"] = None

    # Vek v dňoch musí byť celé číslo
    try:
        hp["vek_dni"] = int(hp["vek_dni"])
    except ValueError:
        if not iza:
            return False
        print(f'WARNING: HP {hp["id"]} nemá správne vyplnený vek v dňoch.')
        hp["vek_dni"] = None

    # Hmotnosť pacienta ku dňu prijatia v gramoch musí byť celé číslo
    try:
        hp["hmotnost"] = int(hp["hmotnost"])
    except ValueError:
        if not iza:
            return False
        print(f'WARNING: HP {hp["id"]} nemá správne vyplnenú hmotnosť.')
        hp["hmotnost"] = None

    # Počet hodín umelej pľúcnej ventilácie musí byť celé číslo
    try:
        hp["umela_plucna_ventilacia"] = int(hp["umela_plucna_ventilacia"])
    except ValueError:
        if not iza:
            return False
        print(
            f'WARNING: HP {hp["id"]} nemá správne vyplnený počet hodín umelej pľúcnej ventilácie.'
        )
        hp["umela_plucna_ventilacia"] = None

    # Zoznam diagnóz nesmie byť prázdny
    if hp["diagnozy"] == "":
        if not iza:
            return False
        print(f'WARNING: HP {hp["id"]} nemá vyplnenú ani jednu diagnózu.')
        hp["diagnozy"] = None

    return True


def priprav_hp(hp):
    if hp["diagnozy"]:
        hp["diagnozy"] = remove_dots_and_asterisks(hp["diagnozy"]).split("~")
    if hp["vykony"]:
        hp["vykony"] = remove_dots_and_asterisks(hp["vykony"]).split("~")
        hp["vykony"] = [v.split("&")[0] for v in hp["vykony"]]
    if hp["odbornosti"]:
        hp["odbornosti"] = hp["odbornosti"].split("~")


def priprav_citac_dat(file):
    try:
        csv_reader = csv.DictReader(
            file, fieldnames=NAZVY_STLPCOV, delimiter=";", strict=True
        )
    except csv.Error:
        print("ERROR: Zlý formát csv.")
        return
    return csv_reader


def priprav_zapisovac_dat(file):
    return csv.DictWriter(file, fieldnames=NAZVY_STLPCOV + ["ms"], delimiter=";")


def remove_dots_and_asterisks(text):
    return text.replace(".", "").replace("*", "")
