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
from copy import deepcopy
from grouper.priprava_dat import (
    priprav_hp,
    validuj_hp,
    priprav_citac_dat,
    priprav_zapisovac_dat,
)
from grouper.vyhodnotenie_priloh import prirad_ms


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
        with open(
            f"{file_path[:-4]}_output.csv", "w", encoding="utf-8", newline=""
        ) as output_file:

            reader = priprav_citac_dat(input_file)
            writer = priprav_zapisovac_dat(output_file)
            writer.writeheader()

            for hospitalizacny_pripad in reader:
                hp = deepcopy(hospitalizacny_pripad)

                if not validuj_hp(hp, iza):
                    hospitalizacny_pripad["ms"] = "ERROR"
                    writer.writerow(hospitalizacny_pripad)
                    continue

                priprav_hp(hp)

                medicinske_sluzby = prirad_ms(hp, iza)

                if medicinske_sluzby:
                    # deduplikuj medicinske sluzby
                    medicinske_sluzby = list(dict.fromkeys(medicinske_sluzby))
                    hospitalizacny_pripad["ms"] = "~".join(medicinske_sluzby)
                else:
                    hospitalizacny_pripad["ms"] = None

                writer.writerow(hospitalizacny_pripad)


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
