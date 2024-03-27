"""
Funkcie na načítanie a predspracovanie súborov s dátami z príloh.

Načíta všetky prílohy zo súborov a vytvorí pomocné zoznamy pre rôzne kritériá.
"""

import csv
from pathlib import Path

cesta_k_suborom = Path("./Prilohy")


def extrahuj_do_zoznamu(tabulky, nazov_tabulky, nazov_stlpca):
    """
    Extrahuje hodnoty z tabulky (zoznam slovníkov) do zoznamu hodnôt podľa zadaného názvu tabuľky a názvu stĺpca.

    Args:
    tabulky (dict): Slovník obsahujúci všetky tabuľky.
    nazov_tabulky (str): Názov tabuľky, z ktorej sa majú extrahovať hodnoty.
    nazov_stlpca (str): Názov stĺpca, z ktorého sa majú extrahovať hodnoty.

    Returns:
    list: Zoznam hodnôt extrahovaných zo zadaného stĺpca tabuľky.
    """
    return [t[nazov_stlpca] for t in tabulky[nazov_tabulky]]


def nacitaj_vsetky_prilohy():
    """
    Načíta všetky prílohy zo súborov a vráti ich vo forme slovníka.

    Returns:
        dict: Slovník obsahujúci načítané prílohy, kde kľúč je názov súboru bez '.csv' a hodnota je zoznam slovnkov (riadkov príslušnej tabuľky).
    """

    prilohy = {}

    for cesta_k_suboru in cesta_k_suborom.iterdir():
        with open(cesta_k_suboru, "r", encoding="utf-8") as subor:
            nazov_tabulky = cesta_k_suboru.stem
            prilohy[nazov_tabulky] = []
            csv_reader = csv.DictReader(subor, delimiter=";")
            for line in csv_reader:
                prilohy[nazov_tabulky].append(line)

    return prilohy


def priprav_pomocne_zoznamy(tabulky):
    """
    Pripraví pomocné zoznamy pre tabuľky z príloh. Zoznamy vkladá priamo do vstupného slovníka.

    Args:
        tabulky (dict): Slovník obsahujúci všetky tabuľky.

    Returns:
        None
    """

    tabulky["p5_kriterium_nekonvencna_upv_vykony"] = extrahuj_do_zoznamu(
        tabulky, "p5_kriterium_nekonvencna_upv", "kod_vykonu"
    )
    tabulky["p5_kriterium_paliativna_starostlivost_diagnozy"] = extrahuj_do_zoznamu(
        tabulky, "p5_kriterium_paliativna_starostlivost", "kod_diagnozy"
    )
    tabulky["p5_kriterium_potreba_vymennej_transfuzie_vykony"] = extrahuj_do_zoznamu(
        tabulky, "p5_kriterium_potreba_vymennej_transfuzie", "kod_vykonu"
    )
    tabulky["p5_kriterium_riadena_hypotermia_vykony"] = extrahuj_do_zoznamu(
        tabulky, "p5_kriterium_riadena_hypotermia", "kod_vykonu"
    )
    tabulky["p5_signifikantne_OP_vykony"] = extrahuj_do_zoznamu(
        tabulky, "p5_signifikantne_OP", "kod_vykonu"
    )
    tabulky["p5_tazke_problemy_u_novorodencov_diagnozy"] = extrahuj_do_zoznamu(
        tabulky, "p5_tazke_problemy_u_novorodencov", "kod_diagnozy"
    )

    tabulky["p16_koma_diagnozy"] = extrahuj_do_zoznamu(
        tabulky, "p16_koma", "kod_diagnozy"
    )
    tabulky["p16_opuch_mozgu_diagnozy"] = extrahuj_do_zoznamu(
        tabulky, "p16_opuch_mozgu", "kod_diagnozy"
    )
    tabulky["p16_vybrane_ochorenia_diagnozy"] = extrahuj_do_zoznamu(
        tabulky, "p16_vybrane_ochorenia", "kod_diagnozy"
    )


def priprav_vsetky_prilohy():
    """
    Načíta a pripraví všetky prílohy.

    Returns:
        None
    """
    tabulky = nacitaj_vsetky_prilohy()

    priprav_pomocne_zoznamy(tabulky)

    return tabulky
