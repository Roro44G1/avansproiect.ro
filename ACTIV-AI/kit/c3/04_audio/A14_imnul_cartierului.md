# „Unu, doi – Ștrand!” – imnul neoficial al cartierului Ștrand

*Tema: Imnul neoficial al cartierului — cântec AI cu versuri originale · Artefact-model generat cu AI*

> Un cântec vesel pentru cartierul Ștrand din vestul Sibiului, de cântat în clasă: versuri originale (două strofe, refren și punte), o melodie originală și un instrumental demo de 87 de secunde. Melodia este o **temă originală în stil de imn pop/marș vesel**, compusă pentru acest artefact; nu este prelucrarea unei melodii existente. În instrumental, melodia vocii este cântată de un instrument solo (alamă sintetizată), ca ghid pentru cântăreți. **Vocea nu e generată – versurile se cântă în clasă peste instrumental.** Faptele din versuri provin din fișa de fapte verificate a proiectului; ce este doar imagine poetică e marcat în tabelul de la final.

## Fișa piesei

| Element | Detalii |
|---|---|
| Cartierul | Ștrand – în vestul Sibiului, împărțit în Ștrand I și Ștrand II |
| Titlu creativ | „Unu, doi – Ștrand!” |
| Gen | temă originală în stil de imn pop/marș vesel (melodie, acorduri și versuri originale) |
| Măsură și tempo | 4/4, 120 de pătrimi pe minut – o măsură durează exact 2 secunde |
| Tonalitate | Sol major; acorduri G, C, D, D7, Em, Am (toate se pot cânta „deschis” la chitară) |
| Ambitus | D4–E5 (re¹–mi²); vocile de băieți schimbate cântă cu o octavă mai jos |
| Structură | Intro (4 măsuri) – Strofa 1 (8) – Refren (8) – Strofa 2 (8) – Punte (4) – Refren (8) – Final (2) + acordul final |
| Fișier audio | `A14_imnul_cartierului.mp3` – instrumental demo, 87 s, MP3 stereo, 44,1 kHz, 192 kbps; loudness măsurat −14,1 LUFS, vârf real −1,5 dBTP |
| Instrumente (toate sintetizate din cod, fără mostre) | solo de alamă – ghidul pentru voce; glockenspiel – dublează melodia la octavă în intro, refrene și final; chitară acustică (coardă ciupită, sinteză Karplus-Strong); bas; pad; tobe (toba mare, toba mică, hi-hat); bețe (numărătoarea din intro); palme (al doilea refren); cinel (acordul final) |
| Voce | vocea nu e generată – versurile se cântă în clasă peste instrumental |
| Cod sursă | `_src/A14_imnul_cartierului.py` (folosește biblioteca comună `audiolib.py`); comanda `python3 A14_imnul_cartierului.py --notatie` tipărește notația de mai jos din aceleași date din care se sintetizează sunetul |
| Verificare | `_verificare/A14_imnul_cartierului_spectrograma.png`, `_verificare/A14_imnul_cartierului_forma_unda.png`, `_verificare/raport_verificare.json` (inclusiv verificarea notă cu notă a melodiei-ghid: 156 din 156 de note recunoscute) |

## Versuri

**Strofa 1**

Unde-n vest a fost livadă,\
s-a făcut un ștrand aici:\
un bazin olimpic, mare,\
și-unul mic, pentru cei mici!

**Refren**

Unu, doi – Ștrand unu, doi!\
Cartierul cântă-n noi!\
Bloc cu bloc și vis cu vis,\
vestul stă cu geam deschis!

**Strofa 2**

Turnul lui Phleps, pe vremuri,\
trei, cinci, zece metri: sus!\
Vile-ntâi, pe urmă blocuri,\
din șaptezeci, spre apus!

**Punte**

Anii douăzeci? Sau treizeci și șase?\
Două surse, două date!

**Refren** (se repetă; clasa bate din palme pe timpii 2 și 4)

**Final**

Vestul stă cu geam deschis! (ultima silabă se ține peste acordul final)

Lămuriri pentru cântăreți: „Ștrand unu, doi” înseamnă Ștrand I și Ștrand II, cele două părți ale cartierului; „Phleps” se pronunță „Fleps”; „din șaptezeci” înseamnă din 1970; în punte, „anii douăzeci” și „treizeci și șase” sunt cele două date pe care sursele le dau pentru ștrand.

## Versuri cu acorduri

Acordul se schimbă pe silaba de sub el; fiecare acord ține o măsură (în final, Do și Re7 câte o jumătate de măsură).

```
[Strofa 1]
G             Em
Unde-n vest a fost livadă,
C            D
s-a făcut un ștrand aici:
G         C
un bazin olimpic, mare,
Am                      D7
și-unul mic, pentru cei mici!

[Refren]
G                      C
Unu, doi – Ștrand unu, doi!
G         D7
Cartierul cântă-n noi!
G               C
Bloc cu bloc și vis cu vis,
D7            G
vestul stă cu geam deschis!

[Strofa 2]
G                     Em
Turnul lui Phleps, pe vremuri,
C                 D
trei, cinci, zece metri: sus!
G             C
Vile-ntâi, pe urmă blocuri,
Am                   D7
din șaptezeci, spre apus!

[Punte]
Em             C
Anii douăzeci? Sau treizeci și șase?
Am          D7
Două surse, două date!

[Refren] – ca mai sus

[Final]
C      D7     G
vestul stă cu geam deschis!
```

## Melodia notată

Notație internațională a notelor: C = do, D = re, E = mi, F = fa, G = sol, A = la, B = si; F# = fa diez; cifra arată octava (C4 = do central = do¹ în notația școlară, deci D4 = re¹, E5 = mi²). Durate: **o** = optime, **p** = pătrime, **p.** = pătrime cu punct, **d** = doime, **d.** = doime cu punct. Silabele accentuate cad pe timpii 1 și 3 ai măsurii.

### Intro (0:00–0:08) – instrumentul solo cântă „cârligul” refrenului

| Măs. | Timp | Acord | Silabe | Note (durată) |
|---|---|---|---|---|
| 1 | 0:00 | G | (instrumental) | G4 o · G4 o · B4 p · D5 p · E5 o · D5 o |
| 2 | 0:02 | C | (instrumental) | C5 d · pauză d |
| 3 | 0:04 | D7 | (instrumental) | C5 p · B4 p · A4 p · A4 p |
| 4 | 0:06 | G | (instrumental; bețele numără 1, 2, 3, 4) | B4 p · A4 p · G4 d |

### Strofa 1 (0:08–0:24)

| Măs. | Timp | Acord | Silabe | Note (durată) |
|---|---|---|---|---|
| 5 | 0:08 | G | Un-de-n vest a | D4 p. · E4 o · G4 p. · G4 o |
| 6 | 0:10 | Em | fost li-va-dă, | B4 p. · A4 o · G4 p · E4 p |
| 7 | 0:12 | C | s-a fă-cut un | E4 p · G4 p · C5 p · B4 p |
| 8 | 0:14 | D | ștrand a-ici: | A4 p · B4 p · A4 d |
| 9 | 0:16 | G | un ba-zin o- | G4 p. · A4 o · B4 p. · D5 o |
| 10 | 0:18 | C | lim-pic, ma-re, | E5 p. · D5 o · C5 p · A4 p |
| 11 | 0:20 | Am | și-u-nul mic, pen-tru cei | E4 o · E4 o · A4 p · C5 p · B4 o · A4 o |
| 12 | 0:22 | D7 | mici! | D5 d. · pauză p |

### Refren (0:24–0:40)

| Măs. | Timp | Acord | Silabe | Note (durată) |
|---|---|---|---|---|
| 13 | 0:24 | G | U-nu, doi – Ștrand u-nu, | G4 o · G4 o · B4 p · D5 p · E5 o · D5 o |
| 14 | 0:26 | C | doi! | C5 d · pauză d |
| 15 | 0:28 | G | Car-ti-e-rul | B4 p · B4 p · D5 p · B4 p |
| 16 | 0:30 | D7 | cân-tă-n noi! | C5 p · B4 p · A4 d |
| 17 | 0:32 | G | Bloc cu bloc și | D5 p. · D5 o · D5 p · B4 p |
| 18 | 0:34 | C | vis cu vis, | E5 p. · E5 o · C5 d |
| 19 | 0:36 | D7 | ves-tul stă cu | C5 p · B4 p · A4 p · A4 p |
| 20 | 0:38 | G | geam des-chis! | B4 p · A4 p · G4 d |

### Strofa 2 (0:40–0:56) – aceeași melodie, cu două mici variante (măsura 21 și finalul măsurii 24, „sus!” urcă la D5)

| Măs. | Timp | Acord | Silabe | Note (durată) |
|---|---|---|---|---|
| 21 | 0:40 | G | Tur-nul lui Phleps, pe | D4 p · E4 o · F#4 o · G4 p. · G4 o |
| 22 | 0:42 | Em | vre-mu-ri, | B4 p. · A4 o · G4 d |
| 23 | 0:44 | C | trei, cinci, ze-ce | E4 p · G4 p · C5 p · B4 p |
| 24 | 0:46 | D | me-tri: sus! | A4 p · B4 p · D5 d |
| 25 | 0:48 | G | Vi-le-ntâi, pe | G4 p. · A4 o · B4 p. · D5 o |
| 26 | 0:50 | C | ur-mă blo-curi, | E5 p. · D5 o · C5 p · A4 p |
| 27 | 0:52 | Am | din șap-te-zeci, spre a- | E4 o · E4 o · A4 p · C5 p · B4 o · A4 o |
| 28 | 0:54 | D7 | pus! | D5 d. · pauză p |

### Punte (0:56–1:04) – se poate cânta sau rosti ritmic, ca întrebare și răspuns

| Măs. | Timp | Acord | Silabe | Note (durată) |
|---|---|---|---|---|
| 29 | 0:56 | Em | A-nii dou-ă-zeci? | E4 o · E4 o · G4 o · G4 o · B4 p · pauză p |
| 30 | 0:58 | C | Sau trei-zeci și șa-se? | G4 o · G4 o · A4 o · B4 o · C5 p · D5 p |
| 31 | 1:00 | Am | Dou-ă sur-se, | E5 p. · E5 o · C5 p. · C5 o |
| 32 | 1:02 | D7 | dou-ă da-te! | D5 p. · D5 o · A4 p · F#4 p |

### Refren, reluare (1:04–1:20)

Măsurile 33–40 sunt identice cu măsurile 13–20 (aceleași note, aceleași acorduri); în instrumental se adaugă palmele pe timpii 2 și 4.

### Final (1:20–1:24) și acordul final (1:24–1:27)

| Măs. | Timp | Acord | Silabe | Note (durată) |
|---|---|---|---|---|
| 41 | 1:20 | C / D7 | ves-tul stă cu | C5 p · B4 p · A4 p · A4 p |
| 42 | 1:22 | G | geam des-chis! | B4 p · A4 p · G4 d, ținut (coroană) peste acordul final, până la circa 1:27 |

## Structura și marcajele de timp

| Timp | Secțiune | Ce se aude în instrumental | Ce face clasa |
|---|---|---|---|
| 0:00–0:08 | Intro (măsurile 1–4) | alama și glockenspielul cântă „cârligul” refrenului; chitară, bas și pad; în măsura 4 (0:06–0:08) bețele numără „1, 2, 3, 4” | ascultă; la bețe se pregătește să cânte |
| 0:08–0:24 | Strofa 1 (5–12) | ritm de marș: basul face „um-pa” (fundamentala pe 1, cvinta pe 3), chitara bate scurt pe 2 și 4, toba mare pe 1 și 3; la 0:23, un rulou scurt de tobă mică anunță refrenul | cântă strofa 1 |
| 0:24–0:40 | Refren (13–20) | tobe pop complete, chitară pe optimi, bas pe optimi, glockenspielul dublează melodia | cântă refrenul |
| 0:40–0:56 | Strofa 2 (21–28) | ca strofa 1, plus toba mică pe 2 și 4 și un pad discret; rulou scurt spre punte la 0:55 | cântă strofa 2 |
| 0:56–1:04 | Punte (29–32) | acorduri lungi, toba mică pe 2 și 4; de la 1:00, rulou de marș în crescendo | cântă (sau rostește) puntea: o grupă întreabă, cealaltă răspunde |
| 1:04–1:20 | Refren, reluare (33–40) | ca primul refren, plus palme pe 2 și 4 | cântă refrenul și bate din palme pe 2 și 4 |
| 1:20–1:24 | Final (41–42) | ultimul vers al refrenului, încă o dată; palme în măsura 41, rulou scurt de tobă la 1:23 | cântă „vestul stă cu geam deschis!” |
| 1:24–1:27 | Acord final | lovitură de tobă, cinel, acordul de Sol care se stinge | ține ultima silabă („-chis”) până se stinge acordul |

## Ce e real și ce e imaginat

| Vers | Ce spune | Statut | Sursa (fișa de fapte verificate, „Ștrandul și cartierul Ștrand”) |
|---|---|---|---|
| „Unde-n vest a fost livadă” | zona se numea „Fleischhauer Wiese” – Pajiștea / Livada Măcelarilor; cartierul Ștrand este în vestul orașului | fapt | old.tribuna.ro; en.wikipedia |
| „s-a făcut un ștrand aici” | în această zonă s-a construit ștrandul, de la care și-a luat numele cartierul | fapt | turnulsfatului.ro (2014); old.tribuna.ro |
| „un bazin olimpic, mare, / și-unul mic, pentru cei mici” | planurile arhitectului Walther Schöpp: un bazin de dimensiuni olimpice și un bazin pentru copii („bazin olimpic” = de dimensiuni olimpice) | fapt | old.tribuna.ro |
| „Turnul lui Phleps, pe vremuri, / trei, cinci, zece metri” | trambulina „Turnul lui Phleps”, cu sărituri de la 3, 5 și 10 m; platforma de 10 m a fost demontată în 2008 – de aceea „pe vremuri” | fapt | old.tribuna.ro |
| „Vile-ntâi, pe urmă blocuri, / din șaptezeci” | 1970: încep lucrările la cartierul Ștrand – întâi vile pe pantă, apoi blocuri tip | fapt | turnulsfatului.ro (2016); en.wikipedia |
| „spre apus” | cartierul este în vestul orașului | fapt, spus poetic | en.wikipedia |
| „Anii douăzeci? Sau treizeci și șase? / Două surse, două date!” | divergența surselor: ștrandul construit „în anii 1920” (turnulsfatului.ro, 2014; en.wikipedia: 1920) sau inaugurat la 12 iulie 1936 (old.tribuna.ro) – cântecul le spune pe amândouă, „după sursă” | fapt, cu divergența arătată ca atare | turnulsfatului.ro; en.wikipedia; old.tribuna.ro |
| „Ștrand unu, doi” | cartierul este împărțit în Ștrand I și Ștrand II | fapt | en.wikipedia; turnulsfatului.ro (2016) |
| „sus!”, „Cartierul cântă-n noi”, „Bloc cu bloc și vis cu vis”, „vestul stă cu geam deschis” | imagini poetice, fără valoare de informație | imaginat | – |

Ce nu spune cântecul: nu dă cifre de locuitori, nu spune dacă ștrandul este deschis azi sau ce program are, nu spune că se mai sare de la 10 m, nu numește firme sau localuri și nu alege „data care sună mai bine” dintre cele două ale surselor.

## Cum se folosește în clasă

1. Ascultați o dată instrumentalul urmărind versurile cu acorduri; observați cum alama cântă exact melodia vocii.
2. Învățați întâi refrenul (introducerea îl anunță), apoi strofele; puntea poate fi rostită ritmic, pe două grupe.
3. În al doilea refren, bateți din palme pe timpii 2 și 4, odată cu palmele din instrumental.
4. Cine cântă la chitară poate acompania cu acordurile de mai sus, toate deschise; cine cântă la un instrument melodic (flaut, xilofon, clape) poate cânta melodia după tabelul cu note.

## Prompt-model pentru clasă

1. Alegeți cartierul vostru și scrieți patru–șase fapte verificate, fiecare cu sursa: originea numelui, un an, o clădire sau un loc cunoscut.
2. Cereți unui asistent AI gratuit: „Scrie versurile unui imn vesel pentru cartierul [X], de cântat de o clasă: două strofe de câte patru versuri, un refren de patru versuri ușor de reținut și o punte de două versuri. Folosește DOAR faptele din lista mea; dacă sursele nu se potrivesc, spune asta în versuri. Versuri de 7–8 silabe, cu rimă la versurile 2 și 4. Nu inventa ani, nume sau cifre.”
3. Pentru muzică: compuneți o melodie simplă pe patru acorduri (de exemplu Sol – Do – Re – Sol) sau folosiți un generator de muzică cu AI care are plan gratuit (verificați condițiile actuale și vârsta minimă), cerând „instrumental vesel, marș pop, 120 BPM, fără voce, 90 de secunde”. Scrieți în descriere cine sau ce a compus melodia.
4. Verificați fiecare vers cu lista de fapte și completați un tabel „ce e real și ce e imaginat”, ca acesta.

### Întrebări de reflecție

1. Puntea cântă două date pentru același ștrand. De ce e mai cinstit așa decât să alegem una singură, „care sună mai bine”?
2. Care vers din imnul vostru ar putea fi luat drept fapt, deși e doar imagine poetică? Cum l-ați marca pentru cei care îl ascultă?
