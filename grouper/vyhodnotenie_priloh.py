"""
Funkcie na vyhodnotenie jednotlivých príloh zákona 531/2023 Z. z.

Hlavnými funkicami sú funkcie nazvané priloha_x, prípadne prilohy_x_y. Tieto funkcie vždy vracajú zoznam nájdených medicínskych služieb.
"""

import re
from grouper.priprava_priloh import priprav_vsetky_prilohy

tabulky = priprav_vsetky_prilohy()


def s_viacerymi_tazkymi_problemami(diagnozy):
    """
    Vyhodnocuje splnenie podmienky pre globálnu funkciu „Viaceré ťažké problémy u novorodencov“ v klasifikačnom systéme.

    Interne je táto definícia implementovaná pomocou zoznamu diagnóz zapísaného v tabuľke. Je nutné mať aspoň 2 diagnózy z tohto zoznamu.

    Args:
        diagnozy (List[str]): zoznam diagnóz

    Returns:
        bool: Splnenie "Viaceré ťažké problémy u novorodencov"
    """
    if diagnozy is None:
        return False

    pocet_tazkych_problemov = len(
        [
            d
            for d in diagnozy
            if d in tabulky["p5_tazke_problemy_u_novorodencov_diagnozy"]
        ]
    )
    return pocet_tazkych_problemov >= 2


def so_signifikantnym_vykonom(vykony):
    """
    Vyhodnocuje splnenie podmienky pre globálnu funkciu „Signifikantný operačný výkon“ v klasifikačnom systéme.

    Interne je táto definícia implementovaná pomocou zoznamu výkonov zapísaného v tabuľke.

    Args:
        vykony (List[str]): zoznam výkonov

    Returns:
        bool: Splnenie globálnej funkcie "Signifikantný operačný výkon"
    """
    return any(vykon in tabulky["p5_signifikantne_OP_vykony"] for vykon in vykony)


def splna_kriterium_podla_5(kriterium, diagnozy, vykony, hmotnost, upv):
    """
    Vyhodnotenie doplňujúcich kritérií podľa prílohy 5.

    Args:
        kriterium (str): názov kritéria
        diagnozy (List[str]): zoznam diagnóz
        vykony (Listr[str]): zoznam výkonov
        hmotnost (int): hmotnosť pacienta v gramoch
        upv (int): trvanie umelej pľúcnej ventilácie v hodinách

    Returns:
        bool: spĺňa doplňujúce kritérium
    """

    # Doplňujúce kritérium „Nekonvenčná UPV (vysokofrekvenčná, NO ventilácia)“ sa je splnené, ak mal pacient vykázaný najmenej jeden z definovaných výkonov
    if kriterium == "Nekonvenčná UPV (vysokofrekvenčná, NO ventilácia)":
        return any(
            vykon in tabulky["p5_kriterium_nekonvencna_upv_vykony"] for vykon in vykony
        )

    # Doplňujúce kritérium „Riadená hypotermia“ je splnené, ak mal pacient vykázaný najmenej jeden z definovaných výkonov
    if kriterium == "Riadená hypotermia":
        return any(
            vykon in tabulky["p5_kriterium_riadena_hypotermia_vykony"]
            for vykon in vykony
        )

    # Doplňujúce kritérium „Paliatívna starostlivosť u novorodencov“ je splnené, ak mal pacient vykázanú najmenej jednu z definovaných diagnóz
    if kriterium == "Paliatívna starostlivosť u novorodencov":
        return diagnozy is not None and any(
            diagnoza in tabulky["p5_kriterium_paliativna_starostlivost_diagnozy"]
            for diagnoza in diagnozy
        )

    # Doplňujúce kritérium „Potreba výmennej transfúzie“ je splnené, ak mal pacient vykázaný najmenej jeden z definovaných výkonov
    if kriterium == "Potreba výmennej transfúzie":
        return any(
            vykon in tabulky["p5_kriterium_potreba_vymennej_transfuzie_vykony"]
            for vykon in vykony
        )

    # Doplňujúce kritérium „Akútny pôrod novorodenca v prípade ohrozenia života bez ohľadu na gestačný vek a hmotnosť” je splnené, ak mal pacient vykázaný aj tento výkon: 93083, Akútny pôrod novorodenca v prípade ohrozenia života
    if (
        kriterium
        == "Akútny pôrod novorodenca v prípade ohrozenia života bez ohľadu na gestačný vek a hmotnosť"
    ):
        return "93083" in vykony

    # Doplňujúce kritérium „Novorodenec pod hranicou viability (< 24 týždeň alebo < 500 g)” je splnené, ak mal hospitalizovaný pacient hmotnosť menej ako 500g alebo gestačný vek nižší ako 24 týždňov.
    # Gestačný vek sa kontroluje ako výkon "99999"
    if kriterium == "Novorodenec pod hranicou viability (< 24 týždeň alebo < 500 g)":
        return (hmotnost is not None and hmotnost < 500) or "99999" in vykony

    # Doplňujúce kritérium „So signifikantným OP výkonom“ je splnené, ak hospitalizačný prípad pacienta splnil podmienky pre globálnu funkciu „Signifikantný operačný výkon“ v klasifikačnom systéme.
    if kriterium == "So signifikantným OP výkonom":
        return so_signifikantnym_vykonom(vykony)

    # Doplňujúce kritérium „Bez signifikantného OP výkonu, s UPV > 95 hodín, s viacerými ťažkými problémami“ je splnené, ak hospitalizačný prípad pacienta nesplnil podmienky pre globálnu funkciu „Signifikantný operačný výkon“ v klasifikačnom systéme, ale dĺžka umelej pľúcnej ventilácie poskytnutej počas hospitalizácie v súlade s pravidlami kódovania pre umelú pľúcnu ventiláciu bola vyššia ako 95 hodín a hospitalizačný prípad splnil podmienky pre globálnu funkciu „Viaceré ťažké problémy u novorodencov“ v klasifikačnom systéme.
    if (
        kriterium
        == "Bez signifikantného OP výkonu, s UPV > 95 hodín, s viacerými ťažkými problémami"
    ):
        return (
            not so_signifikantnym_vykonom(vykony)
            and upv is not None
            and upv > 95
            and s_viacerymi_tazkymi_problemami(diagnozy)
        )

    # Doplňujúce kritérium „Bez signifikantného OP výkonu a bez UPV > 95 hodín a viacerých ťažkých problémov“ je splnené, ak hospitalizačný prípad pacienta nesplnil podmienky pre globálnu funkciu „Signifikantný operačný výkon“ v klasifikačnom systéme a zároveň dĺžka umelej pľúcnej ventilácie poskytnutej počas hospitalizácie v súlade s pravidlami kódovania pre umelú pľúcnu ventiláciu nebola vyššia ako 95 hodín alebo hospitalizačný prípad nesplnil podmienky pre globálnu funkciu „Viaceré ťažké problémy u novorodencov“ v klasifikačnom systéme.
    if (
        kriterium
        == "Bez signifikantného OP výkonu a bez UPV > 95 hodín a viacerých ťažkých problémov"
    ):
        return not so_signifikantnym_vykonom(vykony) and (
            (upv is not None and upv <= 95)
            or not s_viacerymi_tazkymi_problemami(diagnozy)
        )


def priloha_5(hmotnost, upv, diagnozy, vykony, drg):
    """
    Ak mal poistenec v deň prijatia na hospitalizáciu vek najviac 28 dní, medicínska služba sa určí podľa skupiny klasifikačného systému, do ktorej bol hospitalizačný prípad zaradený alebo podľa skupiny klasifikačného systému a zdravotného výkonu alebo diagnózy podľa doplňujúceho kritéria (NOV).

    Args:
        hmotnost (int): hmotnosť poistenca v gramoch
        upv (int): doba umelej pľúcnej ventilácie v hodinách
        diagnozy (List[str]): zoznam diagnóz
        vykony (List[str]): zoznam výkonov
        drg (str): skupina klasifikačného systému DRG

    Returns:
        List[str]: Zoznam priradených medicínskych služieb
    """

    return [
        line["kod_ms"]
        for line in tabulky["p5_novorodenci"]
        if drg.startswith(line["drg"])
        and (
            not line["doplnujuce_kriterium"]
            or splna_kriterium_podla_5(
                line["doplnujuce_kriterium"],
                diagnozy,
                vykony,
                hmotnost,
                upv,
            )
        )
    ]


def s_kraniocerebralnou_traumou(diagnozy):
    """
    Diagnóza patrí do skupiny diagnóz „Kraniocerebrálna trauma“, ak mal poistenec vykázanú najmenej jednu diagnózu s kódom začínajúcim v rozsahu kódov diagnóz „S02“ až „S09“.

    Args:
        diagnozy (List[str]): zoznam diagnóz

    Returns:
        bool: aspoň 1 z diagnóz je v rozsahu kódov diagnóz „S02“ až „S09“
    """
    return any(
        diagnoza[:3] in ["S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09"]
        for diagnoza in diagnozy
    )


def splna_kriterium_podla_6(kriterium, diagnozy):
    """
    Diagnóza musí zodpovedať stĺpcu skupiny diagnóz.

    Aktuálne sú 2 skupiny: „Kraniocerebrálna trauma“ a "bez diagnózy Kraniocerebrálna trauma".

    Args:
        kriterium (_type_): názov kritéria
        diagnozy (_type_): zoznam diagnóz

    Returns:
        bool: spĺňa kritérium skupiny diagnóz
    """
    if kriterium == "Kraniocerebrálna trauma":
        return s_kraniocerebralnou_traumou(diagnozy)

    if kriterium == "bez diagnózy Kraniocerebrálna trauma":
        return not s_kraniocerebralnou_traumou(diagnozy)


def priloha_6(drg, diagnozy, je_dieta):
    """
    Ak bol hospitalizačný prípad poistenca zaradený podľa klasifikačného systému do skupiny podľa stĺpca "Skupina klasifikačného systému" pri diagnóze zodpovedajúcej stĺpcu „skupina diagnóz“, hospitalizácii sa určí medicínska služba podľa stĺpca "medicínska služba" (DRGD).

    Napr.
    Skupina klasifikačného systému: Skupina klasifikačného systému začínajúca na „W“
    Skupina diagnóz: Kraniocerebrálna trauma
    Medicínska služba: Polytrauma s kraniocerebrálnou traumou (S02-01)

    Rozdelené podľa veku.

    Args:
        drg (str): skupina klasifikačného systému DRG
        diagnozy (List[str]): zoznam diagnóz
        je_dieta (bool): poistenec vo veku 18 rokov a menej

    Returns:
        List[str]: Zoznam priradených medicínskych služieb
    """
    nazov_tabulky = "p6_polytrauma_deti" if je_dieta else "p6_polytrauma_dospeli"

    return [
        line["kod_ms"]
        for line in tabulky[nazov_tabulky]
        if drg.startswith(line["drg"])
        and splna_kriterium_podla_6(line["doplnujuce_kriterium"], diagnozy)
    ]


def poskytnuty_vedlajsi_vykon(vykony, skupina_vykonov, nazov_tabulky):
    """
    Bol vykázaný minimálne jeden výkon z uvedenej skupiny výkonov.

    Args:
        vykony (List[str]): zoznam výkonov
        skupina_vykonov (str): skupina výkonov podľa hlavného výkonu
        nazov_tabulky (str): názov tabuľky, v ktorej sa nachádzajú prislúchajúce skupiny výkonov

    Returns:
        bool: aspoň jeden vykázaný výkon sa nachádza v uvedenej skupine výkonov.
    """
    cielove_vykony = [
        vykon["kod_vykonu"]
        for vykon in tabulky[nazov_tabulky]
        if vykon["skupina_vedlajsich_vykonov"] == skupina_vykonov
    ]

    return any(vykon in cielove_vykony for vykon in vykony)


def prilohy_7_8(vykony, je_dieta, iza):
    """
    Ak bol poistencovi poskytnutý hlavný zdravotný výkon podľa stĺpca "zdravotný výkon" a minimálne jeden výkon z uvedených výkonov (VV).

    Hlavné výkony sú v tabuľkách p7 (deti) a p8 (dospelí).
    Vedľajšie výkony sa kontrolujú z tabuliek p7_vedlajsie_vykony a p8_vedlajsie_vykony podľa parametru skupina_vedlajsich_vykonov.

    V IZA móde predpokladaj, že ktorýkoľvek z vykázaných výkonov mohol byť hlavný.

    Args:
        vykony (List[str]): zoznam výkonov
        je_dieta (bool): poistenec vo veku 18 rokov a menej
        iza (bool): IZA mód, skúša všetky možné hlavné výkony

    Returns:
        List[str]: Zoznam priradených medicínskych služieb
    """
    nazov_tabulky = "p7" if je_dieta else "p8"
    nazov_vedlajsej_tabulky = (
        "p7_vedlajsie_vykony" if je_dieta else "p8_vedlajsie_vykony"
    )

    hlavny_vykon = vykony[0]
    if not iza and not hlavny_vykon:
        return []
    vedlajsie_vykony = vykony[1:]

    out = []

    for line in tabulky[nazov_tabulky]:
        if line["kod_hlavny_vykon"] == hlavny_vykon and poskytnuty_vedlajsi_vykon(
            vedlajsie_vykony,
            line["skupina_vedlajsich_vykonov"],
            nazov_vedlajsej_tabulky,
        ):
            out.append(line["kod_ms"])

        if iza:
            for i, hlavny_vykon in enumerate(vykony[1:]):
                vedlajsie_vykony = vykony[: i + 1] + vykony[i + 2 :]
                if hlavny_vykon == line[
                    "kod_hlavny_vykon"
                ] and poskytnuty_vedlajsi_vykon(
                    vedlajsie_vykony,
                    line["skupina_vedlajsich_vykonov"],
                    nazov_vedlajsej_tabulky,
                ):
                    out.append(line["kod_ms"])
    return out


def splna_diagnoza_zo_skupiny_podla_9(diagnozy, skupina_diagnoz, je_dieta):
    """
    Kontroluj, či prípad má diagnózu patriacu skupine definovaných diagnóz.


        Args:
            diagnozy (List[str]): zoznam diagnóz hospitalizačného prípadu
            skupina_diagnoz (str): Názov skupiny diagnóz podľa prílohy 9 stĺpec Diagnóza
            je_dieta (bool): poistenec vo veku 18 rokov a menej

        Returns:
            bool: aspoň jedna diagnóza je z uvedenej skupiny diagnóz
    """
    diagnozy_zo_skupiny = [
        diagnoza
        for diagnoza in tabulky["p9_skupiny_diagnoz"]
        if diagnoza["skupina_diagnoz"] == skupina_diagnoz
    ]

    for line in diagnozy_zo_skupiny:
        if line["typ_diagnozy"] == "hlavná":
            kontrolovane_diagnozy = [diagnozy[0]]
        elif line["typ_diagnozy"] == "akákoľvek":
            kontrolovane_diagnozy = diagnozy

        if line["kod_diagnozy"] == "Vzťahuje sa na viacero diagnóz":
            nazov_ms_tabulky = "p14" if je_dieta else "p15"
            nazov_ms = re.search("„.*“", line["nazov_diagnozy"]).group()[1:-1]
            cielove_diagnozy = diagnozy_podla_ms(nazov_ms, nazov_ms_tabulky)
        else:
            cielove_diagnozy = [line["kod_diagnozy"]]

        for cielova_diagnoza in cielove_diagnozy:
            for kontrolovana_diagnoza in kontrolovane_diagnozy:
                if kontrolovana_diagnoza.startswith(cielova_diagnoza):
                    return True

    return False


def diagnozy_podla_ms(nazov_ms, nazov_ms_tabulky):
    """
    Vráť diagnózy, ktoré sú definované danou medicínskou službou

    Args:
        nazov_ms (str): Názov medicínskej služby
        nazov_ms_tabulky (str): Názov tabuľky s definíciami medicínskych služieb podľa diagnóz

    Returns:
        List[str]: zoznam kódov diagnóz
    """
    return [
        line["kod_hlavnej_diagnozy"]
        for line in tabulky[nazov_ms_tabulky]
        if line["nazov_ms"] == nazov_ms
    ]


def rozsah_na_zoznam(rozsah):
    """
    Premeň rozsah tvaru C15-26 na zoznam tvaru [C15, C16, ..., C26]

    Args:
        rozsah (str): definícia rozsahu

    Returns:
        List[str]: zoznam kódov v rozsahu
    """
    prvy_prvok, posledne_cislo = rozsah.split("-")
    prve_cislo = prvy_prvok[-len(posledne_cislo) :]
    prefix = prvy_prvok[: -len(posledne_cislo)]
    return [
        prefix + str(cislo) for cislo in range(int(prve_cislo), int(posledne_cislo) + 1)
    ]


def splna_diagnoza_zo_zoznamu_podla_9(diagnozy, zoznam_diagnoz):
    """
    Kontroluj, či prípad má diagnózu zo zoznamu definovaných diagnóz.

    Args:
        diagnozy (List[str]): zoznam diagnóz hospitalizačného prípadu
        zoznam_diagnoz (List[str]): Zoznam diagnóz podľa prílohy 9 stĺpec Kód diagnózy

    Returns:
        bool: aspoň jedna diagnóza je zo zoznamu definovaných diagnóz
    """
    cielove_diagnozy = []

    for diagnoza in zoznam_diagnoz.split(","):
        diagnoza = diagnoza.strip()
        if "-" in diagnoza:
            cielove_diagnozy.extend(rozsah_na_zoznam(diagnoza))
        else:
            cielove_diagnozy.append(diagnoza)

    return any(
        diagnoza.startswith(cielova_diagnoza)
        for diagnoza in diagnozy
        for cielova_diagnoza in cielove_diagnozy
    )


def priloha_9(diagnozy, vykony, je_dieta, iza):
    """
    Ak bol poistencovi poskytnutý hlavný zdravotný výkon podľa stĺpca "zdravotný výkon" pri diagnóze zo skupiny diagnóz podľa stĺpca „diagnóza“ (alebo pri diagnóze alebo diagnózach podľa stĺpca „Kód diagnózy“), hospitalizácii sa určí medicínska služba podľa stĺpca "medicínska služba" (VD).

    Napr.
    Kód výkonu: 5t061
    Diagnóza: Trauma a poúrazové stavy (skupina diagnóz)
        alebo
    Kód diagnózy: C49, C772-3, C15-26, C78, C79, C64 (zoznam diagnóz)
    Medicínska služba: Osteosyntéza pre poúrazové stavy a komplikácie (S02-35)

    Args:
        diagnozy (List[str]): zoznam diagnóz
        vykony (List[str]): zoznam výkonov
        je_dieta (bool): poistenec vo veku 18 rokov a menej
        iza (bool): IZA mód, skúša všetky možné hlavné výkony

    Returns:
        List[str]: zoznam priradených medicínskych služieb
    """
    nazov_tabulky_skupiny_diagnoz = (
        "p9_deti_skupiny_diagnoz" if je_dieta else "p9_dospeli_skupiny_diagnoz"
    )
    nazov_tabulky_zoznam_diagnoz = (
        "p9_deti_zoznam_diagnoz" if je_dieta else "p9_dospeli_zoznam_diagnoz"
    )

    hlavny_vykon = vykony[0]
    if not iza and not hlavny_vykon:
        return []

    out = []
    for line in tabulky[nazov_tabulky_skupiny_diagnoz]:
        if line[
            "kod_hlavneho_vykonu"
        ] == hlavny_vykon and splna_diagnoza_zo_skupiny_podla_9(
            diagnozy, line["skupina_diagnoz"], je_dieta
        ):
            out.append(line["kod_ms"])

        if iza:
            for hlavny_vykon in vykony[1:]:
                if line[
                    "kod_hlavneho_vykonu"
                ] == hlavny_vykon and splna_diagnoza_zo_skupiny_podla_9(
                    diagnozy, line["skupina_diagnoz"], je_dieta
                ):
                    out.append(line["kod_ms"])

    for line in tabulky[nazov_tabulky_zoznam_diagnoz]:
        if line[
            "kod_hlavneho_vykonu"
        ] == hlavny_vykon and splna_diagnoza_zo_zoznamu_podla_9(
            diagnozy, line["zoznam_diagnoz"]
        ):
            out.append(line["kod_ms"])

        if iza:
            for hlavny_vykon in vykony[1:]:
                if line[
                    "kod_hlavneho_vykonu"
                ] == hlavny_vykon and splna_diagnoza_zo_zoznamu_podla_9(
                    diagnozy, line["zoznam_diagnoz"]
                ):
                    out.append(line["kod_ms"])

    return out


def priloha_10(diagnozy):
    """
    Ak bola poistencovi pri hospitalizácii vykázaná hlavná diagnóza podľa stĺpca „skupina diagnóz pre hlavnú diagnózu“ a vedľajšia diagnóza podľa stĺpca „názov vedľajšej diagnózy“, hospitalizácii sa určí medicínska služba podľa stĺpca "medicínska služba" (DD).

    Args:
        diagnozy (List[str]): zoznam diagnóz

    Returns:
        List[str]: zoznam medicínskych služieb
    """
    return [
        line["kod_ms"]
        for line in tabulky["p10"]
        if line["kod_hlavnej_diagnozy"] == diagnozy[0]
        and line["kod_vedlajsej_diagnozy"] in diagnozy[1:]
    ]


def priloha_11(vykony, odbornosti, je_dieta, iza):
    """
    Ak bol poistencovi poskytnutý hlavný zdravotný výkon podľa stĺpca "zdravotný výkon" na pracovisku s odbornosťou 023 „rádiológia“, hospitalizácii sa určí medicínska služba podľa stĺpca "medicínska služba" (VO).

    Rozdelené podľa veku.

    Args:
        vykony (List[str]): zoznam výkonov
        odbornosti (List[str]): zoznam odborností
        je_dieta (bool): poistenec vo veku 18 rokov a menej
        iza (bool): IZA mód, skúša všetky možné hlavné výkony

    Returns:
        List[str]: zoznam medicínskych služieb
    """
    nazov_tabulky = "p11_deti" if je_dieta else "p11_dospeli"

    hlavny_vykon = vykony[0]
    if not iza and not hlavny_vykon:
        return []

    out = [
        line["kod_ms"]
        for line in tabulky[nazov_tabulky]
        if line["kod_hlavneho_vykonu"] == hlavny_vykon and "023" in odbornosti
    ]

    if iza:
        for hlavny_vykon in vykony[1:]:
            out.extend(
                [
                    line["kod_ms"]
                    for line in tabulky[nazov_tabulky]
                    if line["kod_hlavneho_vykonu"] == hlavny_vykon
                    and "023" in odbornosti
                ]
            )

    return out


def prilohy_12_13(vykony, je_dieta, iza):
    """
    Ak bol poistencovi poskytnutý hlavný zdravotný výkon podľa stĺpca "zdravotný výkon", hospitalizácii sa určí medicínska služba podľa stĺpca "medicínska služba" (V).

    Rozdelené podľa veku.

    Args:
        vykony (List[str]): zoznam výkonov
        je_dieta (bool): poistenec vo veku 18 rokov a menej
        iza (bool): IZA mód, skúša všetky možné hlavné výkony

    Returns:
        List[str]: zoznam medicínskych služieb
    """
    nazov_tabulky = "p12" if je_dieta else "p13"

    hlavny_vykon = vykony[0]
    if not iza and not hlavny_vykon:
        return []

    out = [
        line["kod_ms"]
        for line in tabulky[nazov_tabulky]
        if line["kod_hlavneho_vykonu"] == hlavny_vykon
    ]

    if iza:
        for hlavny_vykon in vykony[1:]:
            out.extend(
                [
                    line["kod_ms"]
                    for line in tabulky[nazov_tabulky]
                    if line["kod_hlavneho_vykonu"] == hlavny_vykon
                ]
            )

    return out


def prilohy_14_15(diagnozy, je_dieta):
    """Ak bola poistencov pri hospitalizácii vykázaná hlavná diagnóza podľa stĺpca "hlavná diagnóza", hospitalizácii sa určí medicínska služba podľa stĺpca "medicínska služba" (D).

    Rozdelené podľa veku.

    Args:
        diagnozy (List[str]): zoznam diagnóz
        je_dieta (bool): pacient vo veku 18 rokov a menej

    Returns:
        List[str]: Zoznam medicínskych služieb
    """
    nazov_tabulky = "p14" if je_dieta else "p15"

    return [
        line["kod_ms"]
        for line in tabulky[nazov_tabulky]
        if line["kod_hlavnej_diagnozy"] == diagnozy[0]
    ]


def priloha_16(diagnozy):
    """
    Medicínska služba „Identifikácia mŕtveho darcu orgánov“ (S17-22) sa určí, ak je pri hospitalizačnom prípade vykázaná aspoň jedna diagnóza zo skupiny diagnóz „Kóma“ a súčasne aspoň jedna diagnóza zo skupiny „Opuch mozgu“ a súčasne aspoň jedna z diagnóz so skupiny „Vybrané ochorenia mozgu“ (S)

    Args:
        diagnozy (List[str]): Zoznam diagnóz hospitalizačného prípadu.

    Returns:
        [List[str]]: Zoznam medicínskych služieb.
    """

    kod_ms = "S17-22"
    nazvy_zoznamov_diagnoz = [
        "p16_koma_diagnozy",
        "p16_opuch_mozgu_diagnozy",
        "p16_vybrane_ochorenia_diagnozy",
    ]

    for cielovy_zoznam in nazvy_zoznamov_diagnoz:
        if not any(
            cielova_diagnoza in diagnozy for cielova_diagnoza in tabulky[cielovy_zoznam]
        ):
            return []
    return [kod_ms]


def prirad_ms(hp, iza):
    """Vyhodnoť všetky prílohy a vytvor zoznam medicínskych služieb priraditeľných k hospitalizačnému prípadu.

    Príloha sa vyhodnocuje, iba pokiaľ hospitalizačný prípad má vyplnené polia nutné pre vyhodnotenie prílohy.

    Args:
        hp (dict): hospitalizačný prípad
        iza (bool): IZA mód, skúša všetky možné hlavné výkony

    Returns:
        List[str]: zoznam medicínskych služieb
    """
    services = []

    je_dieta = hp["vek"] is not None and hp["vek"] <= 18
    je_novorodenec = (
        hp["vek"] is not None
        and hp["vek"] == 0
        and hp["vek_dni"] is not None
        and hp["vek_dni"] <= 28
    )

    if je_novorodenec and hp["drg"]:
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
        services.extend(priloha_11(hp["vykony"], hp["odbornosti"], je_dieta, iza))

    if hp["vek"] is not None and hp["vykony"]:
        services.extend(prilohy_12_13(hp["vykony"], je_dieta, iza))

    if hp["vek"] is not None and hp["diagnozy"]:
        services.extend(prilohy_14_15(hp["diagnozy"], je_dieta))

    if hp["diagnozy"]:
        services.extend(priloha_16(hp["diagnozy"]))

    return services
