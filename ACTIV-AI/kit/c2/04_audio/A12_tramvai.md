# Coloana sonoră a primului tramvai – reconstituire sonoră

*Tema: Coloana sonoră a primului tramvai — reconstituire sonoră AI · Artefact-model generat cu AI*

O călătorie imaginată de un minut cu tramvaiul electric al Sibiului, în 1905: vatmanul sună de două ori din clopoțel, motorul electric prinde viteză, roțile bat ritmic pe rosturile șinelor, un scârțâit scurt anunță curba, la captatorul de curent pocnesc scântei, undeva pe stradă trec cai, apoi frâna pneumatică șuieră și tramvaiul oprește în stație, cu un ultim clopoțel. **Toate sunetele sunt sintetizate din formule matematice** (cod Python), fără nicio înregistrare și fără mostre. Nu este o înregistrare istorică: nimeni nu a înregistrat tramvaiul din 1905, iar sunetul lui real nu este descris în fișa de fapte a proiectului.

## Fișier audio

| Element | Detalii |
|---|---|
| Fișier | `A12_tramvai.mp3` |
| Durată | aproximativ 52 de secunde |
| Format | MP3 stereo, 44,1 kHz, 192 kbps, loudness măsurat −14,2 LUFS, vârf real −1,2 dBTP |
| Cod sursă | `_src/A12_tramvai.py` (folosește biblioteca comună `audiolib.py` din `04_audio/_src`) |
| Verificare | `_verificare/A12_tramvai_spectrograma.png`, `_verificare/A12_tramvai_forma_unda.png`, `_verificare/raport_verificare.json` |

## Straturile sonore

| Strat | Ce se aude | Cum a fost construit | Când apare |
|---|---|---|---|
| Murmur de stradă | un fond nedeslușit, ca o piață animată auzită de la distanță | zgomot colorat trecut prin filtre trece-bandă (120–1400 Hz), cu „valuri” lente de intensitate; canalele pornesc din zgomote diferite | permanent, mai evident la început și la final |
| Cai la distanță | trapul unei trăsuri, în stânga la început, apoi în dreapta, mai departe | fiecare lovitură de potcoavă: un mic „ciocănit” modal (380–520 Hz) plus zgomot scurt, înfundat; ritm în patru timpi | 0,5–9 s și 25–32 s |
| Clopoțelul vatmanului | două lovituri limpezi, apoi, la final, alte două | sinteză modală cu șapte parțiale (prima la 1760 Hz) și bătăi lente între perechi; un clic de atac din zgomot filtrat | 2,0 s și 46,0 s |
| Motorul electric | un zumzet care urcă în înălțime odată cu viteza și coboară la frânare | sumă de zece armonice pe o fundamentală care glisează de la 42 la 230 Hz, cu modulație în amplitudine la dublul fundamentalei; un „scâncet” de angrenaj la armonicele 7 și 11; filtrul trece-jos se deschide cu viteza; brum jos al caroseriei | 3,2–44,5 s |
| Roțile pe rosturi | clicuri duble („ta-tac… ta-tac”), rare la pornire și tot mai dese la viteză | pentru fiecare rost: lovitură joasă (70–95 Hz), ping metalic scurt (sinteză modală) și zgomot granular; două boghiuri, câte două osii; intervalul scade de la 1,4 s la 0,42 s | 5–44,5 s |
| Scârțâit la curbă | un sunet subțire, oscilant, în două rafale | ton de 2900–3600 Hz cu patru armonice și vibrato neregulat, plus o bandă îngustă de zgomot | 18,5 s și 19,9 s (și unul mic la frânare, 42,7 s) |
| Scântei la captator | pocnete foarte scurte, în rafale de unul până la trei | zgomot filtrat trece-bandă (2,5–9 kHz) cu anvelopă de câteva milisecunde | între 9 și 43,5 s, numai la viteză |
| Frâna pneumatică | un șuierat lung care se stinge, apoi un „pșșș” scurt la oprire | zgomot alb filtrat (700–9000 Hz) cu atac rapid și decădere exponențială; filtrul se închide pe măsură ce „presiunea” scade | 40,5–43,9 s și 44,7–46,3 s |

Straturile apropiate (clopoțel, motor, roți, frână) trec printr-o reverberație scurtă; strada și caii, printr-una mai lungă, ca să sune „de peste piață”.

## Harta în timp

| Secunde | Ce se întâmplă |
|---|---|
| 0–2 | piața: murmur de stradă și o trăsură care trece în stânga |
| 2,0 | clopoțelul vatmanului – două lovituri |
| 3,2–22 | motorul pornește și accelerează; roțile încep să bată pe rosturi, tot mai des; primele scântei |
| 18,5–20,5 | scârțâit la curbă |
| 22–34 | viteză de croazieră: zumzet constant, clicuri regulate, scântei; a doua trăsură, în dreapta |
| 34–44,5 | încetinire: motorul coboară, clicurile se răresc |
| 40,5–44 | frâna pneumatică șuieră |
| 44,5–46 | oprire; „pșșș” de eliberare a aerului |
| 46,0 | clopoțelul final – două lovituri |
| 46–52 | rămâne murmurul străzii, care se stinge (fade-out în ultimele 3 s) |

## Ce e real și ce e imaginat

Faptele din fișa verificată a proiectului, pe care se sprijină scena:

- prima linie de tramvai electric din Sibiu a fost inaugurată în 1905 (8 septembrie conform patrimoniu.sibiu.ro; tribuna.ro dă 9 august), pe traseul Piața Gării – Parcul Sub Arini (zona Spitalului Militar);
- vagoanele au fost aduse de la Budapesta, iar linia a fost construită de o firmă din Budapesta;
- în 1925 existau 14 vagoane-motor, cu 30 de locuri fiecare (16 pe scaun); în primii 20 de ani tramvaiul a transportat 3.950.197 de călători;
- în oraș, tramvaiul a dispărut în 1966–1967.

Tot ce se aude este imaginat: nu știm cum suna clopoțelul, motorul sau frâna vagoanelor din 1905, dacă aveau frână pneumatică, dacă pe traseu era o curbă care scârțâia sau câți cai treceau pe stradă. Acestea sunt alegeri artistice, nu afirmații istorice. Scena nu descrie un loc precis de pe traseu.

## Idei pentru o clasă

- Ascultați piesa fără să citiți fișa și notați, cu secunde, fiecare sunet recunoscut; comparați apoi cu harta în timp.
- Alegeți un mijloc de transport de azi (autobuzul, trenul, bicicleta) și descrieți-i „coloana sonoră” în șase–opt straturi, cu momente de început și sfârșit.

## Prompt-model pentru clasă

1. Căutați în surse oficiale două sau trei fapte verificate despre subiect (an, traseu, număr de vagoane) și notați sursa.
2. Cereți unui generator de efecte sonore cu AI care are plan gratuit (verificați condițiile actuale și vârsta minimă): „Tramvai electric vechi care pornește din stație: clopoțel, motor electric care accelerează, roți pe șine, fără muzică, 50 de secunde.” Generați separat: „scârțâit scurt de roți la curbă”, „frână pneumatică de tramvai”, „murmur de piață de oraș, început de secol douăzeci”.
3. Mixați straturile într-un editor audio gratuit (de exemplu, Audacity), în ordinea unei călătorii: plecare, accelerare, croazieră, frânare, oprire; țintiți un volum confortabil, fără vârfuri care distorsionează.
4. Scrieți în descriere că este o reconstituire imaginată, nu o înregistrare istorică, și enumerați faptele verificate pe care le-ați folosit, cu sursa.

### Întrebări de reflecție

1. Piesa sună „credibil”, dar niciun sunet nu e autentic. Ce ar trebui să scrie pe eticheta ei, ca un vizitator să nu o ia drept înregistrare din 1905?
2. Care dintre straturi v-a ajutat cel mai mult să „vedeți” tramvaiul? Ce sunet lipsește și de ce credeți că a fost lăsat deoparte?
