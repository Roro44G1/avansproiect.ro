# „Între bufniță și soare” – dimineața în Dumbrava Sibiului

*Tema: Peisaj sonor AI: dimineața în Dumbrava Sibiului · Artefact-model generat cu AI*

> Un minut și jumătate într-o dimineață imaginată în pădurea de stejar a Dumbravei: pe întuneric se aud vântul în coroane, apa lacurilor și o bufniță; apoi păsările încep, una câte una, iar spre răsărit corul se îndesește. **Toate sunetele sunt sintetizate din formule matematice** (cod Python), fără mostre, fără înregistrări, fără voce și fără muzică. **Sunetele de păsări sunt aproximări sintetizate, nu înregistrări** și nu sunt o identificare ornitologică exactă: un ornitolog ar găsi diferențe de înălțime, ritm și timbru față de păsările adevărate. Animalele care se aud sunt doar cele pe care fișa de fapte a proiectului le numește pentru Dumbrava.

## Fișa piesei

| Element | Detalii |
|---|---|
| Titlu creativ | „Între bufniță și soare” |
| Gen | peisaj sonor sintetizat procedural (sound design), fără voce și fără muzică |
| Fișier audio | `A16_dimineata_in_dumbrava.mp3` – 90 s, MP3 stereo, 44,1 kHz, 192 kbps; loudness măsurat −14,1 LUFS, vârf real (true peak) −1,3 dBTP |
| Ascultare recomandată | cu căști sau pe boxe stereo: păsările sunt așezate în stânga, în centru și în dreapta, unele aproape, altele departe |
| Cod sursă | `_src/A16_dimineata_in_dumbrava.py` (folosește biblioteca comună `audiolib.py` din `04_audio/_src`); marcajele de timp și evenimentele sonore sunt scrise de script în `_src/A16_marcaje.json` |
| Verificare | `_verificare/A16_dimineata_in_dumbrava_spectrograma.png`, `_verificare/A16_dimineata_in_dumbrava_forma_unda.png`, `_verificare/raport_A16_A17.json` (inclusiv o verificare că fiecare eveniment sonor se ridică peste fondul din banda lui de frecvență) |
| Informații zoologice generale | `_fapte_noi_A16_A17.md` (descrieri generale ale vocii păsărilor, după en.wikipedia) |

## Scenariul pe marcaje de timp

Lumina nu se aude: răsăritul este sugerat de corul tot mai des și de briza care se întețește în coroane. Pozițiile (stânga, dreapta, aproape, departe) sunt alegeri de mixaj, nu locuri reale din pădure.

| Secunde | Moment | Ce se aude |
|---|---|---|
| 0–17 | Întuneric | vânt slab în coroanele stejarilor, clipocitul lacului la mal și bulele unui pârâiaș; **bufnița** strigă de trei ori („hu-hu” grav), la 2,5, 8,8 și 15,2 s, din stânga, tot mai departe; o primă adiere în frunze la 11–17 s |
| 17 | Prima mierlă | **mierla** începe: fraze fluierate, joase pentru o pasăre, cu o încheiere ciripită; revine la câteva secunde (stânga-centru) |
| 24 | Pițigoiul | **pițigoiul**, în dreapta: două note repetate, prima înaltă, a doua mai joasă („ți-ciu, ți-ciu”) |
| 30,5 | Presura | **presura**, în stânga, departe: un șir de note scurte, tot mai tari, încheiat cu două note lungi |
| 36 | Ciocănitoarea | **ciocănitoarea**, în dreapta: un rulou rapid de lovituri în lemn; încă unul la 41,5 s; adiere mai puternică la 39–46 s |
| 44–56,5 | Pași pe frunze | un drumeț imaginat (nu se vede, nu vorbește) trece de la stânga la dreapta, pe frunze uscate; de la 46 s cântă și o a doua mierlă, departe, în dreapta |
| 50,5–53 | Gaița | **gaița**, în dreapta: trei țipete aspre, hârșâite, chiar când trece drumețul |
| 57,5 | Ciocănitoarea, din nou | un al treilea rulou |
| 59,5–66,5 | Veverița | **veverița**: gheare pe scoarță, în salturi scurte, cu pauze; urcă pe trunchi și se îndepărtează; câteva bucățele de scoarță cad pe frunze; de la 60 s, un al doilea pițigoi, departe, în stânga |
| 67,5–73 | Corbul | **corbul** trece pe deasupra, din dreapta spre stânga: șase croncănituri grave, rezonante; la 71 s, gaița, departe, în stânga |
| 75–86 | Răsăritul (imaginat) | corul plin: mierle, pițigoi, presura cântă mai des; briza dimineții se întețește în coroane (cel mai tare la 80–84 s); ciocănitoarea la 80,5 s |
| 86–90 | Final | corul și vântul se sting treptat (fade-out în ultimele 4 s) |

## Straturile sonore – cum au fost construite

| Strat | Ce se aude | Cum a fost construit | Ce aproximează |
|---|---|---|---|
| Vânt în coroane | un suflu și un foșnet de frunze care cresc în rafale | zgomot colorat filtrat în două benzi (220–1300 Hz și 1,3–4 kHz) plus un foșnet înalt (2,5–9 kHz) modulat de „pâlpâiri” rapide și neregulate; anvelopă cu patru rafale | vânt în frunzișul unei păduri de foioase (fără o specie anume) |
| Apa lacurilor | clipocit discret la mal și bule mici | zgomot jos (180–1100 Hz) cu valuri lente de intensitate; circa 22 de bule pe secundă, fiecare un ton scurt care urcă în frecvență (380–1700 Hz) | salba de lacuri și pârâul care le drenează (din fișa de fapte); nu e un loc anume |
| Bufnița | „hu-hu” grav, prima silabă mai lungă și accentuată | două tonuri de circa 305 Hz și 285 Hz, cu armonice slabe și puțin „suflu”, depărtate prin filtrare și reverberație lungă | descrierea generală a cântecului buhei (en.wikipedia: „ooh-hu”, 250–350 Hz) |
| Mierla | fraze fluierate, variate, cu o încheiere ciripită | 4–7 note pe frază, între circa 1,5 și 3,5 kHz, cu glisări în sus, în jos sau în arc, plus 3–6 ciripituri scurte, înalte | „cântec variat, melodios, ca un fluier jos” (en.wikipedia) |
| Pițigoiul | două note repetate de 3–5 ori | o notă scurtă de circa 5,3–6,1 kHz, apoi una de circa 3,4–3,9 kHz, repetate | „teacher, teacher” al pițigoiului mare (en.wikipedia) |
| Presura | 7–10 note scurte, tot mai tari, apoi două note lungi | note de circa 5,4–6,2 kHz, de 45 ms fiecare, cu volum crescător; apoi o notă de 0,22 s și una de 0,55 s, mai joasă (circa 4,2–4,8 kHz), ușor „bâzâită” | cântecul presurii galbene („a little bit of bread and no cheese”, en.wikipedia) |
| Ciocănitoarea | rulouri scurte de lovituri în lemn | 13–17 lovituri, tot mai dese (de la circa 17 la circa 25 pe secundă); fiecare lovitură e o rezonanță de lemn gol (sinteză modală: 380, 905, 1640, 2750 Hz) plus un clic | „tobele” ciocănitorilor: lovituri repetate, foarte rapide, într-o suprafață care rezonează (en.wikipedia) |
| Pași pe frunze | strivirea frunzelor uscate, ritmic | pentru fiecare pas, două „nori” de sute de micro-pocnete filtrate (0,9–9 kHz) și o bufnitură joasă; un pas la 0,62 s; panoramare din stânga în dreapta | un drumeț imaginat – personaj fictiv, nevăzut |
| Gaița | țipete aspre, hârșâite | zgomot filtrat (1,1–5,2 kHz) cu modulație aspră de circa 85 Hz și un ton armonic care coboară ușor | „țipăt aspru, hârșâit” (en.wikipedia) |
| Veverița | zgârieturi scurte pe scoarță | grupuri de 4–8 zgârieturi (zgomot de 8–20 ms, 1,8–8,5 kHz), cu pauze; filtrare tot mai închisă, ca un sunet care urcă și se depărtează | o veveriță care urcă pe un trunchi (imaginat); veverița e în lista faunei din fișă |
| Corbul | croncănit grav, rezonant, cu „r” la început | ton de dinte de fierăstrău de circa 200 Hz care coboară puțin, cu rezonanțe (formanți) la 720, 1100–1600 și 2300–2900 Hz și o modulație de 28 Hz la început | „croncănit grav… prruk-prruk-prruk” (en.wikipedia) |

Sunetele apropiate (pași, veveriță, apă) trec printr-o reverberație scurtă; păsările și ciocănitoarea, printr-una mai lungă și mai întunecată, ca să sune „din adâncul pădurii”.

## Ce e real, ce e aproximat și ce e imaginat

**Real – din fișa de fapte verificate** (secțiunea „Pădurea / Parcul natural Dumbrava Sibiului”):

- Dumbrava Sibiului are 993 ha (sibiul.ro, ecomagazin.ro) și este, în principal, un stejăret de terasă: gorun, carpen, ulm, cireș pădureț, jugastru, tei (dssibiu.ro; sibiul.ro);
- fauna numită de surse: căprior, veveriță, mistreț, vulpe; păsări: pițigoi, mierlă, presură, ciocănitoare, gaiță, bufniță, corb (sibiul.ro; ecomagazin.ro) – piesa folosește doar păsările acestea și veverița;
- lacurile: o salbă de lacuri drenate de pârâul Valea Aurie (dssibiu.ro) sau trei lacuri artificiale formate de pârâul Trinkbach (sibiul.ro) – sursele dau nume diferite pârâului.

**Aproximat:**

- toate sunetele sunt construite din cod; nimic nu a fost înregistrat în Dumbrava;
- fișa numește păsările doar generic (pițigoi, mierlă, presură, ciocănitoare, bufniță), fără specie; aproximările au pornit de la descrierea generală a vocii unor specii reprezentative (pițigoiul mare, mierla, presura galbenă, buha, gaița, corbul), după en.wikipedia (vezi `_fapte_noi_A16_A17.md`). Nu se afirmă că aceste specii anume trăiesc în Dumbrava;
- frecvențele, ritmurile și duratele sunt alese „după ureche”, ca să sugereze pasărea, nu măsurate pe înregistrări.

**Imaginat:**

- dimineața întreagă: ordinea în care încep păsările, momentele, distanțele, vântul de la răsărit;
- anotimpul: corul dimineții e de regulă cel mai bogat primăvara (en.wikipedia), de aceea scena e gândită ca o dimineață de primăvară; dacă bufnița din fișă este buha, ea se aude mai ales în lunile reci, din toamna târzie până în iarnă (en.wikipedia) – alăturarea bufniței și a corului de primăvară este o alegere artistică, nu o observație;
- drumețul care calcă pe frunze este un personaj fictiv; gaița care strigă „la trecerea lui” este o mică poveste sonoră, nu un comportament afirmat;
- veverița care urcă pe trunchi și bucățelele de scoarță care cad.

**Ce nu spune piesa:** nu indică un loc precis din pădure și nu reproduce sunetele căpriorului, mistrețului sau vulpii (sunt în fișă, dar au rămas deoparte); nu adaugă alte animale (de exemplu rațe sau broaște), pentru că fișa nu le numește; nu conține niciun sunet de oraș.

## Idei pentru o clasă

- Ascultați piesa cu ochii închiși și notați, cu secunde, fiecare animal recunoscut; comparați apoi cu scenariul de mai sus. Care sunet a fost cel mai greu de ghicit?
- Desenați „harta sonoră”: unde ați așezat fiecare pasăre (stânga, dreapta, aproape, departe)?
- Ascultați apoi înregistrări reale ale acelorași păsări (de exemplu, din colecții publice de sunete de păsări) și scrieți trei diferențe față de aproximările sintetizate.

## Prompt-model pentru clasă

1. Alegeți un loc din natură apropiat (un parc, o pădure, un mal de râu) și găsiți într-o sursă oficială lista animalelor care trăiesc acolo; notați sursa.
2. Cereți unui generator de efecte sonore cu AI care are plan gratuit (verificați condițiile actuale și vârsta minimă): „Pădure de stejar în zori, fără muzică și fără voci: vânt ușor în frunze, apă liniștită, apoi păsări care încep să cânte una câte una, 90 de secunde.” Generați separat sunetele pe care le doriți clare: „rulou de ciocănitoare pe un trunchi”, „pași pe frunze uscate”.
3. Folosiți DOAR animale din lista voastră. Mixați straturile într-un editor audio gratuit (de exemplu, Audacity), în ordinea unei dimineți: întuneric, primele păsări, corul plin.
4. Scrieți pe eticheta piesei: „sunete generate cu AI, nu înregistrări”, lista animalelor cu sursa și ce ați imaginat (ordinea, anotimpul, personajele).

### Întrebări de reflecție

1. O pasăre sintetizată „sună credibil”, dar nu e o înregistrare. De ce e important ca eticheta să spună asta, mai ales pentru cineva care învață să recunoască păsările după cântec?
2. Piesa pune împreună o bufniță și corul de primăvară, deși sursele spun că se aud de regulă în anotimpuri diferite. Când e acceptabilă o astfel de alegere artistică și cum o semnalați cinstit?
