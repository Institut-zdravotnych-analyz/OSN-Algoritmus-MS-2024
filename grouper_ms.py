"""
Funkcia na priraďovanie hospitalizačných prípadov do medicínskych služieb.

Vytvorí kópiu vstupného súboru s pripojeným novým stĺpcom so zoznamom priradených medicínskych služieb.

Args:
    file_path (str): Relatívna cesta k súboru s dátami.
    iza (bool, optional): Pracuj v tzv. IZA móde, snaž sa priradiť všetky teoreticky možné MS aj pre neúplné HP.

Returns:
    None

Examples:
    # Example usage
    grouper_ms("data.csv", iza=True)
"""

import argparse
import csv
import uuid
from copy import deepcopy
from vyhodnotenie_priloh import (
    priloha_5,
    priloha_6,
    prilohy_7_8,
    priloha_9,
    priloha_10,
    priloha_11,
    prilohy_12_13,
    prilohy_14_15,
    priloha_16,
)


def remove_dots_and_asterisks(text):
    return text.replace(".", "").replace("*", "")


def validate_hp(hp, iza):
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


def grouper_ms(file_path, iza=False):
    """
    Funkcia na priraďovanie hospitalizačných prípadov do medicínskych služieb.

    Vytvorí kópiu vstupného súboru s pripojeným novým stĺpcom so zoznamom priradených medicínskych služieb.

    Args:
        file_path (str): Relatívna cesta k súboru s dátami.
        iza (bool, optional): Pracuj v tzv. IZA móde, snaž sa priradiť všetky teoreticky možné MS aj pre neúplné HP.

    Returns:
        None
    """

    if iza:
        print(
            "Aktivovaný IZA mód, priraďujú sa všetky teoreticky možné MS aj pre neúplné HP."
        )

    with open(file_path, "r", encoding="utf-8") as input_file:
        fieldnames = [
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
        try:
            csv_reader = csv.DictReader(
                input_file, fieldnames=fieldnames, delimiter=";", strict=True
            )
        except csv.Error:
            print("ERROR: Zlý formát csv.")
            return

        output_data = []

        for hospitalizacny_pripad in csv_reader:
            hp = deepcopy(hospitalizacny_pripad)

            if not validate_hp(hp, iza):
                hospitalizacny_pripad["ms"] = "ERROR"
                output_data.append(hospitalizacny_pripad)
                continue

            if hp["diagnozy"]:
                hp["diagnozy"] = remove_dots_and_asterisks(hp["diagnozy"]).split("~")
            if hp["vykony"]:
                hp["vykony"] = remove_dots_and_asterisks(hp["vykony"]).split("~")
                hp["vykony"] = [v.split("&")[0] for v in hp["vykony"]]
            if hp["odbornosti"]:
                hp["odbornosti"] = hp["odbornosti"].split("~")

            services = []

            je_dieta = hp["vek"] is not None and hp["vek"] <= 18
            je_novorodenec = (
                hp["vek"] is not None
                and hp["vek"] == 0
                and hp["vek_dni"] is not None
                and hp["vek_dni"] <= 28
            )

            if (
                je_novorodenec
                and hp["hmotnost"] is not None
                and hp["umela_plucna_ventilacia"] is not None
                and hp["diagnozy"]
                and hp["vykony"]
                and hp["drg"]
            ):
                services.extend(
                    priloha_5(
                        hp["hmotnost"],
                        hp["umela_plucna_ventilacia"],
                        hp["diagnozy"],
                        hp["vykony"],
                        hp["drg"],
                    )
                )

            if hp["drg"] and hp["vek"] is not None and hp["diagnozy"]:
                services.extend(priloha_6(hp["drg"], hp["diagnozy"], je_dieta))

            if hp["vek"] is not None and hp["vykony"]:
                services.extend(prilohy_7_8(hp["vykony"], je_dieta, iza))

            if hp["vek"] is not None and hp["diagnozy"] and hp["vykony"]:
                services.extend(priloha_9(hp["diagnozy"], hp["vykony"], je_dieta, iza))

            if hp["diagnozy"]:
                services.extend(priloha_10(hp["diagnozy"]))

            if hp["vek"] is not None and hp["vykony"] and hp["odbornosti"]:
                services.extend(
                    priloha_11(hp["vykony"], hp["odbornosti"], je_dieta, iza)
                )

            if hp["vek"] is not None and hp["vykony"]:
                services.extend(prilohy_12_13(hp["vykony"], je_dieta, iza))

            if hp["vek"] is not None and hp["diagnozy"]:
                services.extend(prilohy_14_15(hp["diagnozy"], je_dieta))

            if hp["diagnozy"]:
                services.extend(priloha_16(hp["diagnozy"]))

            if services:
                unique_services = list(dict.fromkeys(services))
                hospitalizacny_pripad["ms"] = "~".join(unique_services)
            else:
                hospitalizacny_pripad["ms"] = None

            output_data.append(hospitalizacny_pripad)

    with open(f"{file_path[:-4]}_output.csv", "w", encoding="utf-8") as output_file:
        fieldnames.append("ms")
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=";")
        csv_writer.writeheader()
        csv_writer.writerows(output_data)


if __name__ == "__main__":
    # Nastav argumenty pri spúšťaní
    parser = argparse.ArgumentParser(
        description="Funkcia na priraďovanie hospitalizačných prípadov do medicínskych služieb."
    )
    parser.add_argument(
        "data_path", action="store", help="Relatívna cesta k súboru s dátami."
    )
    parser.add_argument(
        "--iza",
        action="store_true",
        help="Pracuj v tzv. IZA móde, snaž sa priradiť všetky teoreticky možné MS aj pre neúplné HP.",
    )

    args = parser.parse_args()

    grouper_ms(args.data_path, args.iza)
