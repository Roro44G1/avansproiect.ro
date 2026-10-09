# „Duminică, la plită” – ASMR într-o bucătărie transilvăneană

*Tema: ASMR AI: o bucătărie transilvăneană duminică dimineața · Artefact-model generat cu AI*

> O sută de secunde într-o bucătărie imaginată, duminică dimineața, în timp ce se pregătesc sarmalele: focul pornește în sobă, apa e turnată în ceaun, ceapa e tocată pe tocător, umplutura e amestecată cu lingura de lemn, frunzele de varză sunt desfăcute, oala de ceramică e pusă pe plită, iar departe bate un clopot. Nimeni nu vorbește și nu se aude muzică. **Toate sunetele sunt aproximări sintetizate din formule matematice** (cod Python), fără mostre, fără înregistrări și fără voce: **nu este o înregistrare dintr-o bucătărie reală**, iar un bucătar ar găsi diferențe față de sunetele adevărate. Piesa e mixată intenționat mai încet decât celelalte piese audio ale expoziției (−18 LUFS în loc de −14 LUFS), ca să rămână o ascultare liniștită, „de aproape”.

## Fișa piesei

| Element | Detalii |
|---|---|
| Titlu creativ | „Duminică, la plită” |
| Gen | peisaj sonor de tip ASMR, sintetizat procedural (sound design); fără voce și fără muzică |
| Fișier audio | `A19_asmr_bucatarie.mp3` – 100 s, MP3 stereo, 44,1 kHz, 192 kbps; loudness măsurat −18,1 LUFS (țintă −18 LUFS, aleasă intenționat), vârf real (true peak) −1,4 dBTP |
| Ascultare recomandată | cu căști, la volum mic spre mediu; sursele sunt așezate în stereo: ceasul în stânga, soba și plita în dreapta, masa și tocătorul în față, clopotul departe, în stânga |
| Loudness | −18 LUFS, nu −14 LUFS ca restul pieselor audio: sunetele ASMR sunt mici și apropiate, iar o piesă „împinsă” la −14 LUFS ar suna obositor; în galerie, piesa se aude puțin mai încet decât celelalte – e o alegere, nu o greșeală |
| Cod sursă | `_src/A19_asmr_bucatarie.py` (folosește biblioteca comună `audiolib.py` din `04_audio/_src`); marcajele de timp și evenimentele sonore sunt scrise de script în `_src/A19_marcaje.json` |
| Verificare | `_verificare/A19_asmr_bucatarie_spectrograma.png`, `_verificare/A19_asmr_bucatarie_forma_unda.png`, `_verificare/raport_A19_A20.json` (inclusiv o verificare că fiecare eveniment sonor se ridică peste fondul din banda lui de frecvență) |
| Termeni (ASMR, ceaun, bule) | `_fapte_noi_A19_A20.md` (după en.wikipedia) |

## Ce înseamnă ASMR

ASMR (din engleză, „autonomous sensory meridian response”) este numele dat unei senzații de furnicături, plăcute, pe care o descriu unii oameni când ascultă sunete mici și liniștite. Printre declanșatorii raportați de cei care o trăiesc se numără bătăile ușoare în suprafețe tari, foșnetul și mototolirea unor materiale subțiri sau privitul cuiva care face atent o activitate obișnuită, de exemplu pregătirea mâncării (en.wikipedia). Nu toată lumea simte așa ceva – piesa poate fi ascultată și doar ca o „fotografie sonoră” a unei dimineți liniștite.

## Povestea de sunet: o dimineață cu sarmale

Fișa de fapte a proiectului spune despre sarmale (en.wikipedia, Romanian cuisine): frunze de varză sau de viță umplute cu carne tocată, orez, ceapă și verdețuri, fierte ore în șir, tradițional în oale de ceramică; în Transilvania se pun în oală, printre sarmale, picioare de porc afumate sau șorici. Din aceste fapte vin sunetele piesei: **ceapa** tocată, **umplutura** amestecată (carnea, orezul, ceapa), **frunzele de varză**, **oala de ceramică**. Restul este imaginat: ordinea pașilor, ceaunul cu apă, soba, ceasul, clopotul și cana. Timpul este comprimat – sarmalele fierb ore în șir, iar piesa se oprește chiar la început, când oala abia a fost pusă pe plită.

## Scenariul pe marcaje de timp

Pozițiile (stânga, dreapta, aproape, departe) sunt alegeri de mixaj, nu planul unei bucătării reale.

| Secunde | Moment | Ce se aude |
|---|---|---|
| 0–3 | Liniște | liniștea camerei; **ceasul de perete**, în stânga – tic-tac, o bătaie pe secundă, până la final |
| 3–4 | Ușița sobei | zăvorul ușiței de fontă sare, apoi balamaua scârțâie (dreapta) |
| 4,6–6 | Chibritul | zgârietura chibritului, apoi flacăra care pornește („fâsss”) |
| 5,6–11,5 | Focul pornește | un „vuuf” scurt și moale, apoi surcelele încep să trosnească, tot mai des (până la circa zece trosnete pe secundă) |
| 11,5 | Ușița se închide | bufnitura ușiței de fontă și zăvorul; de acum **focul** se aude înfundat, prin fontă: **lemnele trosnesc** rar, cu câte un pocnet mai mare, până la final |
| 15–21,5 | Apa turnată în ceaun | întâi apa lovește fundul gol, de fontă (sunet metalic), apoi gâlgâie tot mai „sus” pe măsură ce ceaunul se umple; la sfârșit, trei picături (dreapta) |
| 24–28 | Cuțitul pe tocător | opt felii de **ceapă**, rar: crănțănitul foilor, apoi lama care lovește lemnul tocătorului |
| 29,5–34,5 | Tocat mărunt | 18 lovituri de cuțit, mai dese |
| 34 | Ceaunul începe să fiarbă | primele bule în ceaun, rare; până la final devin tot mai dese |
| 35,8–37 | Ceapa adunată | lama trage de două ori ceapa tocată pe tocător |
| 40–48 | Lingura de lemn | **umplutura** e amestecată în castron: un sunet moale, lipicios, cu „boabe” mărunte (orezul) și lingura care atinge castronul, cam o rotire pe secundă; la 48,3 s și 48,7 s lingura bate de două ori în marginea castronului |
| 51–62 | Frunzele de varză | cinci **frunze de varză** desfăcute (la 51,0, 53,4, 55,9, 58,3 și 60,8 s): un scârțâit crocant, pocnetul nervurii, foșnetul, apoi frunza pusă pe masă |
| 63–68 | Pauză | se aud doar ceasul, focul și ceaunul (sarmalele se rulează – imaginat, fără sunet) |
| 68–69,7 | Oala de ceramică pe plită | **oala de ceramică** e trasă pe plită și așezată (bufnitură de ceramică pe fontă); la 69,3 s capacul clinchetește de câteva ori, până se liniștește (dreapta) |
| 73–89 | Clopotul de duminică | departe, în stânga, un **clopot** bate de șapte ori, rar, cu ecou lung |
| 86,5 | Cana pe masă | o **cană** pusă pe masă, aproape: o atingere ușoară, lemnul mesei, ceramica și un mic clipocit |
| 93–100 | Final | ceaunul fierbe încet, focul trosnește, ceasul merge; totul se stinge treptat în ultimele 6 secunde |

## Straturile sonore – cum au fost construite

| Strat | Ce se aude | Cum a fost construit | Ce aproximează |
|---|---|---|---|
| Liniștea camerei | un fond foarte discret | zgomot colorat, „întunecat”, filtrat sub 600 Hz | aerul unei încăperi liniștite |
| Ceasul de perete | tic-tac | pentru fiecare bătaie, rezonanțe metalice scurte (circa 2,3–7,6 kHz; la „tac”, cu circa patru semitonuri mai jos) și o rezonanță joasă de cutie de lemn | un ceas de perete cu pendul (imaginat) |
| Ușița sobei | zăvor, scârțâit, bufnitură | zăvorul și ușa: sinteză modală (frecvențe de rezonanță ale unei bucăți de metal); scârțâitul: un șir de impulsuri tot mai dese (60–125 pe secundă), trecut prin rezonanțe înguste (circa 0,9–4 kHz) | o ușiță de fontă cu balama |
| Chibritul | zgârietură, flacără | un nor scurt de micro-pocnete (1,5–8,5 kHz), apoi zgomot filtrat care izbucnește și se stinge în circa o secundă | aprinderea unui chibrit |
| Focul | „vuuf”, vuiet moale, trosnete, pocnete | aprinderea: zgomot filtrat care se deschide de la circa 300 la circa 1400 Hz și se stinge în circa o secundă și jumătate; vuiet: zgomot jos (55–320 Hz), cu fluctuații lente; trosnete: grupuri de 1–6 impulsuri de zgomot foarte scurte (0,2–2 ms), la întâmplare; după închiderea ușiței, totul e filtrat (sub circa 3,2 kHz) și mai încet | surcele și lemne care ard în sobă |
| Apa turnată | jet, gâlgâit, picături | un rezonator a cărui frecvență urcă de la circa 380 la circa 930 Hz (aerul din ceaun „se scurtează” când apa se ridică), circa 90 de bule pe secundă și, la început, zgomot metalic | apă turnată într-un ceaun (oală mare de gătit pe foc) |
| Fierberea | bule tot mai dese | fiecare bulă e un ton scurt (circa 220–750 Hz, 30–90 ms) care urcă puțin, cu un mic „pocnet” la suprafață; de la circa o bulă la două secunde până la circa 14 pe secundă | apa care începe să fiarbă încet (o bulă de gaz în lichid „sună” la frecvența ei naturală – rezonanța Minnaert, en.wikipedia) |
| Cuțitul pe tocător | crănțănit și lovituri în lemn | crănțănit: un nor dens de micro-pocnete (1,5–9,5 kHz), de 30–50 ms; lovitura: rezonanțe de lemn (185, 440, 960, 1850 Hz) și o urmă metalică slabă | ceapă tăiată pe un tocător de lemn |
| Lingura de lemn | amestec lipicios, boabe, atingeri | zgomot moale (sub 2 kHz) care urcă și coboară de 1,15 ori pe secundă, mici pocnete „lipicioase”, micro-pocnete înalte (boabele) și o frecare scurtă la fiecare rotire; la final, două lovituri de lemn în ceramică | umplutura de carne tocată, orez și ceapă (ingrediente din fișă), amestecată într-un castron |
| Frunzele de varză | scârțâit crocant, pocnet, foșnet | un scârțâit (impulsuri tot mai dese, 160–600 pe secundă, prin rezonanțe de circa 1,4–4,1 kHz), un pocnet scurt, un foșnet care se stinge și o bufnitură moale | frunze desfăcute de pe căpățână; sunetul a fost făcut „crocant”, ca să se audă – piesa nu spune dacă varza e proaspătă sau murată |
| Oala de ceramică | târșâit, bufnitură, clinchete de capac | frecare scurtă (0,9–4,5 kHz), apoi rezonanțe de ceramică (360–3850 Hz) peste rezonanțe joase de plită; capacul: cinci clinchete tot mai slabe și mai dese | o oală de ceramică pusă pe plita de fontă |
| Clopotul | bătăi grave, lungi, departe | sinteză modală cu parțialele obișnuite ale unui clopot mare (de la circa 131 Hz la circa 1 kHz), stingere de câteva secunde, filtrat și cu ecou lung | un clopot de biserică, duminică (imaginat; nu e o biserică anume) |
| Cana | atingere, lemn, ceramică, clipocit | o atingere slabă, apoi rezonanțe de lemn (135–700 Hz) și de ceramică (1,7–6,2 kHz) și un clipocit scurt | o cană de ceramică, plină, pusă pe o masă de lemn |

Sunetele apropiate trec printr-o reverberație scurtă, de încăpere mică; clopotul, printr-una lungă și întunecată, ca să sune „de afară, de departe”.

## Ce e real, ce e aproximat și ce e imaginat

**Real – din fișa de fapte verificate** (secțiunea „Preparate”): ingredientele sarmalelor (frunze de varză sau de viță, carne tocată, orez, ceapă, verdețuri), fierberea îndelungată și oalele de ceramică (en.wikipedia, Romanian cuisine).

**Aproximat:**

- toate sunetele sunt construite din cod; nimic nu a fost înregistrat într-o bucătărie;
- frecvențele, ritmurile și duratele sunt alese „după ureche”, ca să sugereze sunetul, nu măsurate pe înregistrări;
- frunzele de varză sună „crocant”; piesa nu spune dacă varza e proaspătă sau murată, pentru că fișa nu precizează.

**Imaginat:**

- bucătăria, soba, plita, ceaunul, ceasul, clopotul și cana; persoana care gătește (un personaj fictiv, nevăzut, care nu vorbește);
- ordinea pașilor și timpul comprimat (în realitate, pregătirea și fierberea sarmalelor durează mult mai mult);
- ce se face cu apa din ceaun nu se spune – e doar un sunet al dimineții.

**Ce nu spune piesa:** nu dă o rețetă, cantități sau timpi de fierbere; nu reproduce sunetul picioarelor de porc afumate sau al șoriciului din oală (sunt în fișă, dar au rămas deoparte); nu numește un sat, o casă sau o biserică.

## Idei pentru o clasă

- Ascultați piesa cu căști, cu ochii închiși, și notați, cu secunde, fiecare sunet recunoscut; comparați apoi cu scenariul de mai sus. Care sunet a fost cel mai greu de ghicit?
- Desenați „harta sonoră” a bucătăriei: unde ați așezat soba, masa, ceasul și fereastra prin care se aude clopotul?
- Înregistrați, cu un telefon, două–trei sunete reale din bucătăria de acasă (cu acordul familiei; fără voci) și comparați-le cu aproximările sintetizate: ce e diferit?

## Prompt-model pentru clasă

1. Alegeți un preparat tradițional și găsiți într-o sursă de încredere ingredientele și modul general de preparare; notați sursa.
2. Faceți lista sunetelor care se potrivesc cu acele fapte (de exemplu: ceapa tocată, apa care fierbe) și, separat, lista sunetelor de atmosferă imaginate (ceasul, ploaia, un clopot).
3. Cereți unui generator de efecte sonore cu AI care are plan gratuit (verificați condițiile actuale și vârsta minimă) câte un sunet scurt pentru fiecare element: „cuțit care toacă ceapă pe un tocător de lemn, de aproape, fără voci, 5 secunde”. Mixați sunetele într-un editor audio gratuit (de exemplu, Audacity), în ordinea poveștii voastre, cu pauze de liniște.
4. Scrieți pe eticheta piesei: „sunete generate cu AI, nu înregistrări”, ce e real (cu sursa) și ce e imaginat.

### Întrebări de reflecție

1. Un sunet sintetizat „sună credibil”, dar nu e o înregistrare dintr-o bucătărie reală. De ce e important ca eticheta să spună asta, chiar și pentru o piesă de relaxare?
2. Piesa „comprimă” timpul: o dimineață întreagă de gătit în 100 de secunde. Ce alte alegeri ale piesei ar putea fi luate drept informație, deși sunt doar poveste?
