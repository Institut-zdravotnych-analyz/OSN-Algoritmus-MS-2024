# Zaraďovanie hospitalizačných prípadov do medicínskych služieb

**[ENG]** Algorithm to assign hospital stays to specific medical services within the [hospital network optimization reform](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2021/540).

**[SK]** Informatívny algoritmus na zaradovanie hospitalizačných prípadov k medicínskym službám podľa kategorizačnej vyhlášky pre rok 2024. Jedná sa o technickú implementáciu [Príloh 2 - 12 vyhlášky 316/2022 Z. z.](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2022/316/20220930#prilohy) v rámci zákona [540/2021 Z. z.](https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2021/540) o kategorizácii ústavnej zdravotnej starostlivosti a o zmene a doplnení niektorých zákonov. Vyhláška je dostupná v prehladnej podobe na [https://vyhlaska.sietnemocnic.sk/](https://vyhlaska.sietnemocnic.sk/).

**Platnosť pre rok:** 2024

## Change log
V prípade, že identifikujete chyby v rámci kódu, prosím zaznamenajte ich na GitHub cez Issues, navrhnite priamo cez submit zmenu, alebo nám napíšte email na iza@health.gov.sk.

**Change log:**
- **21.12.2023**: Prvá verzia technickej implementácie vyhlášok pre rok 2024 publikovaná
- **III. 2024**: Prepis technickej implementácie. Zmena názvov príloh.

# Technické readme

## Časť 1: Základný opis programu
Skript je určený na priradenie kódov medicínskych služieb podľa vyhlášky platnej pre rok 2024.

Súčasťou skriptu sú prílohy, ktoré boli vytvorené podľa verzie vyhlášky o kategorizácii vo verzii z 18.10.2023 (verzia do MPK). V prípade zmien v prílohách (bez zmien v algoritme), bude potrebné vytvoriť tieto prílohy nanovo v rovnakej štruktúre a s rovnakým názvom.

## Časť 2: Práca so skriptom
Skript je napísaný v jazyku Python, na spustenie je potrebná inštalácia Python 3.0.

Program sa spustí príkazom: `python3 ./main.py cesta/k/suboru.csv`. Vstupný súbor musí mať nižšie uvedenú štruktúru. Výstupom spracovania je kópia vstupného súboru, kde ku každému riadku je pripojený zoznam nájdených medicínskych služieb.

Pri spúšťaní programu je možné pridať príznak `--iza`, ktorý spôsobí, že algoritmus bude pracovať v tzv. IZA móde, kedy hľadá medicínske služby aj pre neúplné dáta a predpokladá, že ktorýkoľvek z vykázaných výkonov môže byť hlavný. Tento príznak je teda vhodný použiť aj v prípade, keď sa algoritmus používa na dáta z roku 2023. 

### Popis vstupného súboru
Vstupný súbor musí byť vo formáte csv, kde každý riadok reprezentuje jeden hospitalizačný prípad. Oddeľovačom je bodkodčiarka.

Algoritmus predpokladá, že vstupný súbor je bez hlavičky, je nutné zachovať správne poradie.

Popis položiek:
| Č. | interný názov položky   | formát položky | popis položky                                                                                                                  |
|----|-------------------------|----------------|--------------------------------------------------------------------------------------------------------------------------------|
| 1  | id                      | string         | identifikátor hospitalizačného prípadu, umožňuje spätné priradenie kódu MS k HP                                                |
| 2  | vek                     | int            | vek pacienta ku dňu prijatia v rokoch, musí byť vyplnený, pre deti do 1 roka sa uvádza 0                                       |
| 3  | vek_dni                 | int            | vek pacienta ku dňu prijatia v dňoch, musí byť vyplnený pre deti do 1 roka, pre ostatných pacientov sa uvádza 0                |
| 4  | hmotnost                | int            | hmotnosť pacienta ku dňu prijatia v gramoch, musí byť vyplnený pre deti do 28 dní vrátane, pre ostatných pacientov sa uvádza 0 |
| 5  | umela_plucna_ventilacia | int            | počet hodín umelej pľúcnej ventilácie                                                                                          |
| 6  | diagnozy                | list\[string\] | zoznam kódov diagnóz pacienta oddelený znakom „~“, ako prvá sa uvádza hlavná diagnóza; kódy diagnóz sa uvádzajú bez bodky      |
| 7  | vykony                  | list\[string\] | zoznam kódov výkonov pacienta oddelený znakom „~“, ako prvý sa uvádza hlavný výkon; kódy výkonov sa uvádzajú bez bodky         |
| 8  | odbornosti              | list\[string\] | zoznam kódov odborností oddelenia, kde bol vykonaný hlavný výkon oddelený znakom „~“                                           |
| 9  | drg                     | string         | DRG skupina, do ktorej bol hospitalizačný prípad zaradený                                                                      |



# Definície z vyhlášky
(1)	Hlavným zdravotným výkonom je zdravotný výkon, ktorý je poistencovi poskytnutý počas ústavnej zdravotnej starostlivosti v nemocnici (ďalej len „hospitalizácia“), touto nemocnicou je jednoznačne použitý vo vzťahu k diagnostike alebo liečbe hlavnej diagnózy a pri ukončení hospitalizácie je označený ako jej hlavný dôvod.

(2)	Ak v odseku 3 nie je ustanovené inak, medicínska služba sa určuje týmto spôsobom v tomto poradí:

1. ak má poistenec v deň prijatia na hospitalizáciu vek najviac 28 dní, medicínska služba sa určí podľa skupiny klasifikačného systému diagnosticko-terapeutických skupín (ďalej len ,,klasifikačný systém“), do ktorej je poskytnutá ústavná zdravotná starostlivosť, na ktorú sa vzťahuje povinnosť poskytovateľa ústavnej starostlivosti zasielať v elektronickej podobe centru pre klasifikačný systém diagnosticko-terapeutických skupín údaje o poskytnutej zdravotnej starostlivosti a povinnosť zdravotnej poisťovne uhrádzať zdravotnú starostlivosť podľa klasifikačného systému (ďalej len ,,hospitalizačný prípad“), zaradená alebo podľa skupiny klasifikačného systému a zdravotného výkonu alebo diagnózy podľa doplňujúceho kritéria podľa prílohy č. 5,

2. ak je hospitalizačný prípad zaradený do skupiny podľa klasifikačného systému začínajúcej na písmeno „W“, medicínska služba sa určí podľa skupiny klasifikačného systému, do ktorej je hospitalizačný prípad zaradený a diagnózy podľa prílohy č. 6,

3. ak je poistencovi počas hospitalizácie poskytnutý hlavný zdravotný výkon a jeden alebo viac zdravotných výkonov zo zoznamu ďalších zdravotných výkonov podľa prílohy č. 7, medicínska služba sa určí podľa kombinácie hlavného zdravotného výkonu a vykázaného zdravotného výkonu alebo zdravotných výkonov, ak má poistenec 18 rokov alebo menej podľa prílohy č. 7,

4. ak je poistencovi počas hospitalizácie poskytnutý hlavný zdravotný výkon a jeden alebo viac zdravotných výkonov zo zoznamu ďalších zdravotných výkonov podľa prílohy č. 8, medicínska služba sa určí podľa kombinácie hlavného zdravotného výkonu a vykázaného zdravotného výkonu alebo zdravotných výkonov, ak má poistenec viac ako 18 rokov podľa prílohy č. 8, 

5. ak je poistencovi počas hospitalizácie poskytnutý zdravotný výkon pri vykázanej diagnóze, ktorý zodpovedá kombinácii zdravotného výkonu a diagnózy podľa prílohy č. 9, medicínska služba sa určí podľa kombinácie hlavného zdravotného výkonu a diagnózy podľa prílohy č. 9,

6. ak je poistencovi počas hospitalizácie vykázaná kombinácia hlavnej diagnózy a vedľajšej diagnózy, ktorá zodpovedá kombinácii hlavnej diagnózy a vedľajšej diagnózy podľa prílohy č. 10, medicínska služba sa určí podľa kombinácie hlavnej diagnózy a diagnózy podľa prílohy č. 10,

7. ak je poistencovi počas hospitalizácie poskytnutý zdravotný výkon na pracovisku s definovanou odbornosťou, ktorý zodpovedá kombinácii zdravotnému výkonu a odbornosti podľa prílohy č. 11, medicínska služba sa určí podľa kombinácie hlavného zdravotného výkonu a odbornosti podľa prílohy č. 11,

8. ak má poistenec 18 rokov alebo menej a je mu počas hospitalizácie poskytnutý hlavný zdravotný výkon zo zoznamu podľa prílohy č. 12, medicínska služba sa určí podľa prílohy č. 12,

9. ak má poistenec viac ako 18 rokov a je mu počas hospitalizácie poskytnutý hlavný zdravotný výkon zo zoznamu v prílohe č. 13, medicínska služba sa určí podľa prílohy č. 13,

10. v hospitalizačnýcht prípadoch iných ako podľa písmen a) až c) a e) až h), pre poistenca vo veku 18 rokov alebo menej, sa medicínska služba určí podľa hlavnej diagnózy podľa prílohy č. 14; ak hlavná diagnóza pre hospitalizáciu nie je určená poskytovateľom zdravotnej starostlivosti, za hlavnú diagnózu sa považuje diagnóza pri prepustení poistenca,

11. v hospitalizačných prípadoch iných ako podľa písmen b), d) až g) a i), pre poistencov vo veku viac ako 18 rokov, sa medicínska služba určí podľa hlavnej diagnózy podľa prílohy č. 15;  ak hlavná diagnóza pre hospitalizáciu nie je určená poskytovateľom zdravotnej starostlivosti, za hlavnú diagnózu sa považuje diagnóza pri prepustení poistenca.

(3)	Medicínska služba určená podľa prílohy č. 16, ktorá sa môže vykonať spolu s medicínskymi službami určenými podľa písmen a) až k) je medicínska služba „Identifikácia mŕtveho darcu orgánov“.
