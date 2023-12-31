<h1>Zaraďovanie hospitalizačných prípadov do medicínskych služieb</h1>
<b>[ENG]</b> Algorithm to assign hospital stays to specific medical services within the <a href=https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2021/540>hospital network optimization reform</a>. <br>
<b>[SK]</b> Informatívny algoritmus na zaradovanie hospitalizačných prípadov k medicínskym službám podľa kategorizačnej vyhlášky pre rok 2024. Jedná sa o technickú implementáciu <a href=https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2022/316/20220930#prilohy>Príloh 2 - 12 vyhlášky 316/2022 Z. z.</a> v rámci zákona <a href=https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2021/540> 540/2021 Z. z.</a> o kategorizácii ústavnej zdravotnej starostlivosti a o zmene a doplnení niektorých zákonov. Vyhláška je dostupná v prehladnej podobe na <a href=https://vyhlaska.sietnemocnic.sk/>https://vyhlaska.sietnemocnic.sk/</a>.<br>
<br>
Platnosť pre rok: <b>2024</b>
<br>
<h2>Change log</h2>
V prípade, že identifikujete chyby v rámci kódu, prosím zaznamenajte ich na GitHub cez Issues, navrhnite priamo cez submit zmenu, alebo nám napíšte email na iza@health.gov.sk<br>
<br>
Change log:
<ul>
<li><b>21.12.2023</b>: Prvá verzia technickej implementácie vyhlášok pre rok 2024 publikovaná</li>
</ul>

<h1>Technické readme</h1>

<h2>Časť 1: Základný popis programu</h2>
Skript je určený na priradenie kódov medicínskych služieb podľa vyhlášky platnej pre rok 2024.

Súčasťou skriptu sú prílohy, ktoré boli vytvorené podľa verzie vyhlášky o kategorizácii vo verzii z 18.10.2023 (verzia do MPK). V prípade zmien v prílohách (bez zmien v algoritme), bude potrebné vytvoriť tieto prílohy nanovo v rovnakej štruktúre a s rovnakým názvom.

<h2>Časť 2: Práca so skriptom</h2>
Skript je napísaný v Pythone, na spustenie je potrebná inštalácia Python 3.0.

Program sa spustí z konzoly príkazom: grouperMS(„nazov_suboru.csv“). Vstupný súbor musí byť uložený v rovnakom priečinku ako samotný program a musí mať nižšie uvedenú štruktúru. Výstupom spracovania je csv súbor v rovnakej štruktúre, doplnené o stĺpec s kódom MS.

Popis vstupného súboru
Vstupný súbor musí byť vo formáte csv, kde každý riadok reprezentuje jeden hospitalizačný prípad. Oddeľovačom je bodkodčiarka.

<h1>Funkčné požiadavky</h1>
Z vyhlášky:

(1)	Hlavným zdravotným výkonom je zdravotný výkon, ktorý je poistencovi poskytnutý počas ústavnej zdravotnej starostlivosti v nemocnici (ďalej len „hospitalizácia“), touto nemocnicou je jednoznačne použitý vo vzťahu k diagnostike alebo liečbe hlavnej diagnózy a pri ukončení hospitalizácie je označený ako jej hlavný dôvod.

(2)	Ak v odseku 3 nie je ustanovené inak, medicínska služba sa určuje týmto spôsobom v tomto poradí:
<ol>
<li>ak má poistenec v deň prijatia na hospitalizáciu vek najviac 28 dní, medicínska služba sa určí podľa skupiny klasifikačného systému diagnosticko-terapeutických skupín (ďalej len ,,klasifikačný systém“), do ktorej je poskytnutá ústavná zdravotná starostlivosť, na ktorú sa vzťahuje povinnosť poskytovateľa ústavnej starostlivosti zasielať v elektronickej podobe centru pre klasifikačný systém diagnosticko-terapeutických skupín údaje o poskytnutej zdravotnej starostlivosti a povinnosť zdravotnej poisťovne uhrádzať zdravotnú starostlivosť podľa klasifikačného systému (ďalej len ,,hospitalizačný prípad“), zaradená alebo podľa skupiny klasifikačného systému a zdravotného výkonu alebo diagnózy podľa doplňujúceho kritéria podľa prílohy č. 5,</li>
<li>ak je hospitalizačný prípad zaradený do skupiny podľa klasifikačného systému začínajúcej na písmeno „W“, medicínska služba sa určí podľa skupiny klasifikačného systému, do ktorej je hospitalizačný prípad zaradený a diagnózy podľa prílohy č. 6,</li>
<li>ak je poistencovi počas hospitalizácie poskytnutý hlavný zdravotný výkon a jeden alebo viac zdravotných výkonov zo zoznamu ďalších zdravotných výkonov podľa prílohy č. 7, medicínska služba sa určí podľa kombinácie hlavného zdravotného výkonu a vykázaného zdravotného výkonu alebo zdravotných výkonov, ak má poistenec 18 rokov alebo menej podľa prílohy č. 7,</li>
<li>ak je poistencovi počas hospitalizácie poskytnutý hlavný zdravotný výkon a jeden alebo viac zdravotných výkonov zo zoznamu ďalších zdravotných výkonov podľa prílohy č. 8, medicínska služba sa určí podľa kombinácie hlavného zdravotného výkonu a vykázaného zdravotného výkonu alebo zdravotných výkonov, ak má poistenec viac ako 18 rokov podľa prílohy č. 8, </li>
<li>ak je poistencovi počas hospitalizácie poskytnutý zdravotný výkon pri vykázanej diagnóze, ktorý zodpovedá kombinácii zdravotného výkonu a diagnózy podľa prílohy č. 9, medicínska služba sa určí podľa kombinácie hlavného zdravotného výkonu a diagnózy podľa prílohy č. 9,</li>
<li>ak je poistencovi počas hospitalizácie vykázaná kombinácia hlavnej diagnózy a vedľajšej diagnózy, ktorá zodpovedá kombinácii hlavnej diagnózy a vedľajšej diagnózy podľa prílohy č. 10, medicínska služba sa určí podľa kombinácie hlavnej diagnózy a diagnózy podľa prílohy č. 10,</li>
<li>ak je poistencovi počas hospitalizácie poskytnutý zdravotný výkon na pracovisku s definovanou odbornosťou, ktorý zodpovedá kombinácii zdravotnému výkonu a odbornosti podľa prílohy č. 11, medicínska služba sa určí podľa kombinácie hlavného zdravotného výkonu a odbornosti podľa prílohy č. 11,</li>
<li>ak má poistenec 18 rokov alebo menej a je mu počas hospitalizácie poskytnutý hlavný zdravotný výkon zo zoznamu podľa prílohy č. 12, medicínska služba sa určí podľa prílohy č. 12,</li>
<li>ak má poistenec viac ako 18 rokov a je mu počas hospitalizácie poskytnutý hlavný zdravotný výkon zo zoznamu v prílohe č. 13, medicínska služba sa určí podľa prílohy č. 13,</li>
<li>v hospitalizačnýcht prípadoch iných ako podľa písmen a) až c) a e) až h), pre poistenca vo veku 18 rokov alebo menej, sa medicínska služba určí podľa hlavnej diagnózy podľa prílohy č. 14; ak hlavná diagnóza pre hospitalizáciu nie je určená poskytovateľom zdravotnej starostlivosti, za hlavnú diagnózu sa považuje diagnóza pri prepustení poistenca,</li>
<li>v hospitalizačných prípadoch iných ako podľa písmen b), d) až g) a i), pre poistencov vo veku viac ako 18 rokov, sa medicínska služba určí podľa hlavnej diagnózy podľa prílohy č. 15;  ak hlavná diagnóza pre hospitalizáciu nie je určená poskytovateľom zdravotnej starostlivosti, za hlavnú diagnózu sa považuje diagnóza pri prepustení poistenca.</li>
</ol>
(3)	Medicínska služba určená podľa prílohy č. 16, ktorá sa môže vykonať spolu s medicínskymi službami určenými podľa písmen a) až k) je medicínska služba „Identifikácia mŕtveho darcu orgánov“.
