r"""
Program na priraďovanie hospitalizačných prípadov do medicínskych služieb.

Vytvorí kópiu vstupného súboru s pripojeným novým stĺpcom so zoznamom priradených medicínskych služieb.

Args:
    file_path: Relatívna cesta k súboru s dátami.
    --vsetky_vykony_hlavne, -v: Pri vyhodnotení príloh predpokladaj, že ktorýkoľvek z výkazaných výkonov mohol byť hlavný.
    --vyhodnot_neuplne_pripady, -n: V prípade, že nie je vyplnená nejaká povinná hodnota, aj tak pokračuj vo vyhodnocovaní. Štandardne vráti hodnotu 'ERROR'.

Returns:
    None

Examples:
    # Spustenie na Linuxe
    python3 ./main.py ./test_data.csv
    # Spustenie so zapnutým prepínačom na vyhodnotenie aj neúplných prípadov
    python3 ./main.py ./test_data.csv --vyhodnot_neuplne_pripady
    # Spustenie so všetkými prepínačmi zapnutými
    python3 ./main.py ./test_data.csv -vn
    # Spustenie na Windows
    python .\main.py .\test_data_phsk_2.csv -vn
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


def grouper_ms(file_path, vsetky_vykony_hlavne=False, vyhodnot_neuplne_pripady=False):
    """
    Funkcia na priraďovanie hospitalizačných prípadov do medicínskych služieb.

    Vytvorí kópiu vstupného súboru s pripojeným novým stĺpcom so zoznamom priradených medicínskych služieb.

    Args:
        file_path (str): Relatívna cesta k súboru s dátami.
        vsetky_vykony_hlavne (bool, optional): Pri vyhodnotení príloh predpokladaj, že ktorýkoľvek z výkazaných výkonov mohol byť hlavný.
        vyhodnot_neuplne_pripady (bool, optional): V prípade, že nie je vyplnená nejaká povinná hodnota, aj tak pokračuj vo vyhodnocovaní. Štandardne vráti hodnotu 'ERROR'.

    Returns:
        None
    """

    if vsetky_vykony_hlavne:
        print(
            "Aktivovaný prepínač 'Všetky výkony hlavné'. Pri vyhodnotení príloh sa bude predpokladať, že ktorýkoľvek z výkazaných výkonov mohol byť hlavný."
        )
    if vyhodnot_neuplne_pripady:
        print(
            "Aktivovaný prepínač 'Vyhodnoť neúplné prípady'. V prípade, že nie je vyplnená nejaká povinná hodnota, aj tak sa bude pokračovať vo vyhodnocovaní."
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

                if not validuj_hp(hp, vyhodnot_neuplne_pripady):
                    hospitalizacny_pripad["ms"] = "ERROR"
                    writer.writerow(hospitalizacny_pripad)
                    continue

                priprav_hp(hp)

                if medicinske_sluzby := prirad_ms(hp, vsetky_vykony_hlavne):
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
        "--vsetky_vykony_hlavne",
        "-v",
        action="store_true",
        help="Pri vyhodnotení príloh predpokladaj, že ktorýkoľvek z výkazaných výkonov mohol byť hlavný. Štandardne sa za hlavný výkon považuje iba prvý vykázaný, prípadne žiaden, pokiaľ zoznam začína znakom '~'.",
    )
    parser.add_argument(
        "--vyhodnot_neuplne_pripady",
        "-n",
        action="store_true",
        help="V prípade, že nie je vyplnená nejaká povinná hodnota, aj tak pokračuj vo vyhodnocovaní. Štandardne vráti hodnotu 'ERROR'.",
    )

    args = parser.parse_args()

    grouper_ms(args.data_path, args.vsetky_vykony_hlavne, args.vyhodnot_neuplne_pripady)
