# „Piață, pagină, cortină” – uvertură pentru un oraș

*Tema: Uvertură AI pentru un oraș — compoziție instrumentală în 3 mișcări · Artefact-model generat cu AI*

> O uvertură de concert de trei minute și jumătate, în trei mișcări: o dimineață în Piața Mare, o pagină citită la lumina lămpii și o cortină care se ridică. Este o **temă originală în stil de uvertură de concert**: melodiile, armoniile și orchestrația au fost compuse pentru acest artefact și **nu citează nicio lucrare existentă**. Titlul și titlurile mișcărilor sunt inventate. **„Orchestra” este sintetizată în cod**: viorile, flautul, cornii, timpanele sau harpa sunt aproximări calculate din formule (oscilatoare, sinteză aditivă și modală, coarde ciupite, zgomot filtrat), într-o „sală” cu reverberație tot sintetică. **Nu este înregistrarea unei orchestre reale și nu folosește mostre** (sunete înregistrate). Piesa nu a fost cântată de Filarmonica din Sibiu și nici în Sala Thalia; faptele despre Sibiu de mai jos vin din fișa de fapte verificate a proiectului.

## Fișa piesei

| Element | Detalii |
|---|---|
| Titlu creativ | „Piață, pagină, cortină” (inventat; o căutare pe web a titlului exact nu a găsit o lucrare cu acest nume) |
| Gen | temă originală în stil de uvertură de concert, în trei mișcări, în ordinea repede – lent – repede |
| Mișcări | I. „Piața se trezește” · II. „Pagini în lumina lămpii” · III. „Cortina se ridică” (titluri inventate) |
| Tonalități | I – Re major (cu un episod în si minor) · II – Si bemol major · III – Re major |
| Tempo | I – Allegro, 144 de pătrimi pe minut · II – Andante, 72 · III – Maestoso, 76, apoi Allegro, 132 |
| Măsuri | I – 40 de măsuri de 4/4 · II – 26 de măsuri de 3/4 · III – 4 măsuri Maestoso + 28 de măsuri Allegro, de 4/4 |
| Durată | 3:30 (210,3 s): mișcarea I – 1:09,5, mișcarea a II-a – 1:08,8, mișcarea a III-a – 1:08,1 (cu stingerea ultimului acord), plus câte 1,6 s de liniște între mișcări |
| Liant | „motivul orașului” – șase note (treptele 5–1–2–3–6–5 ale gamei), care se aude în toate cele trei mișcări |
| Instrumente (toate sintetizate, aproximări) | viori I (linie legato, 3–4 voci sintetice ușor dezacordate, cu vibrato); viori II și viole (acorduri, tremolo, acorduri scurte); violoncele și contrabași (cu arcușul și pizzicato); flaut; clarinet; corni; trompete; tromboni; tubă; timpane; harpă; glockenspiel; celestă; tobă mică; tobă mare; talgere |
| Fișier audio | `A21_uvertura_pentru_un_oras.mp3` – MP3 stereo, 44,1 kHz, 192 kbps; loudness măsurat −14,1 LUFS, vârf real (true peak) −1,5 dBTP; fără eșantioane la limită (clipping) |
| Cod sursă | `_src/A21_uvertura_pentru_un_oras.py` (folosește biblioteca comună `audiolib.py`); partitura este scrisă în cod, ca text („notă:durată”), iar sunetul se calculează din ea; `--notatie` tipărește tabelele de mai jos din aceleași date; marcajele sunt în `_src/A21_marcaje.json` |
| Verificare | `_verificare/A21_uvertura_pentru_un_oras_spectrograma.png`, `_verificare/A21_uvertura_pentru_un_oras_forma_unda.png`, `_verificare/raport_A21.json` (scriptul `_src/verificare_A21.py`) |
| Termeni verificați | `_fapte_noi_A21.md` (uvertură, mișcare, tempo, timpane – en.wikipedia) |

## Cele trei mișcări

| Mișcarea | Titlu | Indicație | Tonalitate | Măsura | Tempo | Măsuri | Începe la |
|---|---|---|---|---|---|---|---|
| I | „Piața se trezește” | Allegro (repede, luminos) | Re major | 4/4 | 144 de pătrimi pe minut | 40 | 0:00,3 |
| II | „Pagini în lumina lămpii” | Andante (în pas de plimbare) | Si bemol major | 3/4 | 72 de pătrimi pe minut | 26 | 1:11,4 |
| III | „Cortina se ridică” | Maestoso (maiestuos), apoi Allegro | Re major | 4/4 | 76, apoi 132 de pătrimi pe minut | 4 + 28 | 2:21,8 |

Indicațiile de tempo sunt cuvinte italiene, ca în partiturile clasice; intervalele de viteză date de en.wikipedia sunt orientative (Allegro – circa 120–156 de bătăi pe minut, Andante – circa 56–108), iar tempourile alese se încadrează în ele.

## „Motivul orașului”

Șase note care urcă și se opresc pe o notă ținută, ca o chemare: treptele 5 – 1 – 2 – 3 – 6 – 5 ale gamei. Sunt compuse pentru această piesă și leagă cele trei mișcări:

| Unde | Cine cântă | Note (solfegiu) |
|---|---|---|
| I, măsurile 1–2 (0:00,3) | cornii, dublați la octava de jos | la – re – mi – fa diez – si – la (Re major) |
| I, coda, măsurile 37–38 (1:00,3) | trompetele, cu cornii | la – re – mi – fa diez – si – la |
| II, coda, măsurile 23–24 (2:06,4) | clarinetul, încet, în 3/4 | fa – si bemol – do – re – sol – fa (Si bemol major) |
| III, Maestoso, măsurile 2–3 (2:24,9) | trompete, corni și tromboni, în octave | la – re – mi – fa diez – si – la |
| III, punte, măsurile 21–23 (3:03,5) | începutul motivului (trei note), trecut din voce în voce: viori – corni – viori | în si minor, Sol major și mi minor |
| III, final, măsurile 29–30 (3:18,0) | tutti (toată orchestra) | la – re – mi – fa diez – si – la |

## Ce se aude, cu marcaje de timp

### I. „Piața se trezește” – Allegro, Re major, 4/4 (0:00,3–1:09,8)

O dimineață imaginată în Piața Mare: orașul se trezește, vocile se încrucișează, piața se umple.

| Timp | Măsurile | Ce se aude |
|---|---|---|
| 0:00,3 | 1–4 | **Introducere.** Timpanele bat Re și La; cornii cântă motivul orașului peste un tremolo de coarde; flautul și clarinetul răspund, harpa urcă un arpegiu; un rulou de timpane pregătește tema |
| 0:07,0 | 5–12 | **Tema A** la viori, vioaie, în optimi; dedesubt – pizzicato la contrabași și violoncele (pe timpii 1 și 3), acorduri scurte de coarde (pe timpii 2 și 4) și note lungi, discrete, la corni |
| 0:20,3 | 13–20 | **Tema A, a doua oară:** flautul se alătură viorilor, cornii cântă acorduri scurte pe timpii 2 și 4, timpanele marchează timpii 1 și 3, glockenspielul sclipește pe notele lungi |
| 0:33,6 | 21–28 | **Episod în si minor**, mai ușor: clarinetul cântă o melodie nouă peste arpegii în pizzicato; din măsura 25 îi răspunde flautul, mai sus; tremolo și rulou de timpane spre revenire |
| 0:47,0 | 29–36 | **Revenirea temei A, tutti:** viori, flaut și (în primele patru măsuri) trompete; talgerele deschid secțiunea |
| 1:00,3 | 37–40 | **Coda:** motivul orașului la trompete și corni, un avânt al viorilor și al flautului spre o notă înaltă, rulou de timpane; încheiere „ta – taaa” pe acordul de Re major (1:05,3) |
| 1:07,0–1:09,8 | – | acordul final se stinge în „sală” |
| 1:09,8–1:11,4 | – | liniște |

### II. „Pagini în lumina lămpii” – Andante, Si bemol major, 3/4 (1:11,4–2:20,2)

O pagină de liniște: cineva citește, filele se întorc încet. Tonalitatea se mută departe de Re major, ca o lumină care se schimbă.

| Timp | Măsurile | Ce se aude |
|---|---|---|
| 1:11,4 | 1–2 | **Introducere:** harpa singură, în arpegii legănate pe optimi, peste coarde foarte moi |
| 1:16,4 | 3–10 | **Tema lirică** la clarinet; harpa continuă legănarea |
| 1:36,4 | 11–14 | **Mijlocul:** flautul urcă pe trepte (sol, si bemol, do), cornii țin acorduri moi |
| 1:46,4 | 15–22 | **Tema, la viori**, cu o octavă mai sus; clarinetul ține note lungi dedesubt, ca o a doua voce |
| 2:06,4 | 23–26 | **Coda:** motivul orașului, încet, la clarinet (dublat discret de celestă), apoi flautul urcă spre ultima notă; harpa în acorduri rulate; sclipiri de celestă și un rulou foarte încet de timpane pe acordul final |
| 2:16,4–2:20,2 | – | acordul final se stinge |
| 2:20,2–2:21,8 | – | liniște |

### III. „Cortina se ridică” – Maestoso, apoi Allegro, Re major, 4/4 (2:21,8–3:29,9)

Momentul dinaintea unui spectacol imaginat: sala se liniștește, cortina urcă, scena se luminează.

| Timp | Măsurile | Ce se aude |
|---|---|---|
| 2:21,8 | 1 | **Maestoso:** rulou de timpane pe Re, care crește, și un talger care „se umflă” |
| 2:24,9 | 2–3 | motivul orașului la alămuri, în octave (trompete, corni, tromboni), cu lovitură de timpane, tobă mare și talgere |
| 2:31,2 | 4 | **cortina se ridică:** glissando de harpă de jos până sus, tremolo de coarde, rulouri de timpane și de tobă mică |
| 2:34,4 | 5–12 | **Allegro, tema festivă** la trompete și viori, cu acompaniament de marș: tubă și violoncele pe timpii 1 și 3, corni pe timpii 2 și 4, tobă mică și tobă mare |
| 2:48,9 | 13–20 | **Tema festivă, tutti:** flautul se alătură, glockenspielul sclipește, cornii cântă note lungi dedesubt, trompetele revin în a doua jumătate |
| 3:03,5 | 21–24 | **Punte:** începutul motivului trece de la viori la corni și înapoi; arpegiu urcător și rulou de timpane |
| 3:10,8 | 25–28 | **Tema A din mișcarea I**, acum la trompete, viori și flaut: dimineața din piață revine ca o amintire festivă |
| 3:18,0 | 29–32 | **Final:** motivul orașului, tutti (toată orchestra); o figură care urcă la viori și flaut, rulouri de timpane și de tobă mică; acordul lung de Re major (3:23,5) și lovitura de încheiere (3:25,3) |
| 3:25,3–3:29,9 | – | ultimul acord se stinge în „sală” |

## Temele, notate

Notație internațională a notelor: C = do, D = re, E = mi, F = fa, G = sol, A = la, B = si; „#” = diez, „b” = bemol (Bb = si bemol); cifra arată octava (C4 = do central). Durate: **ș** = șaisprezecime, **o** = optime, **o.** = optime cu punct, **p** = pătrime, **p.** = pătrime cu punct, **d** = doime, **d.** = doime cu punct, **n** = notă întreagă. Acorduri: litera = nota de bază; fără alt semn – acord major (D = Re major), „m” – minor (Bm = si minor), „7” – cu septimă (A7 = La major cu septimă); între paranteze – câți timpi ține acordul, când într-o măsură sunt mai multe. Timpii din tabele sunt rotunjiți la zecimi de secundă.

### I. Motivul orașului (introducere, corni – sună cu o octavă mai jos decât e scris aici)

| Măs. | Timp | Acorduri | Note (durată) |
|---|---|---|---|
| 1 | 0:00,3 | D | A4 p · D5 p. · E5 o · F#5 p |
| 2 | 0:02,0 | G (1 timp) – D (3 timpi) | B5 p · A5 d. |

### I. Tema A (viori I)

| Măs. | Timp | Acorduri | Note (durată) |
|---|---|---|---|
| 5 | 0:07,0 | D | A4 o · D5 o · F#5 o · E5 o · D5 p · A5 p |
| 6 | 0:08,6 | A7 (2 timpi) – D (2 timpi) | G5 o · F#5 o · E5 o · F#5 o · D5 d |
| 7 | 0:10,3 | G | B4 o · D5 o · G5 o · F#5 o · E5 p · B5 p |
| 8 | 0:12,0 | A | A5 o. · G5 ș · F#5 o · G5 o · A5 d |
| 9 | 0:13,6 | D (2 timpi) – Bm (2 timpi) | A4 o · D5 o · F#5 o · E5 o · D5 p · B5 p |
| 10 | 0:15,3 | D | A5 o · G5 o · F#5 o · G5 o · A5 p · D6 p |
| 11 | 0:17,0 | G (2 timpi) – A7 (2 timpi) | B5 o · A5 o · G5 o · F#5 o · E5 p · C#6 p |
| 12 | 0:18,6 | D | D6 p · A5 o · F#5 o · D5 p · pauză p |

### I. Episodul în si minor (clarinet, apoi flaut)

| Măs. | Timp | Acorduri | Note (durată) |
|---|---|---|---|
| 21 | 0:33,6 | Bm | F#4 o · B4 o · C#5 o · D5 o · C#5 p · B4 p |
| 22 | 0:35,3 | F#m | A4 o · B4 o · C#5 o · A4 o · F#4 d |
| 23 | 0:37,0 | G (2 timpi) – D (2 timpi) | G4 o · B4 o · D5 o · E5 o · F#5 p · E5 p |
| 24 | 0:38,6 | F#7 (2 timpi) – Bm (2 timpi) | D5 o · C#5 o · B4 o · A#4 o · B4 d |
| 25 | 0:40,3 | Bm | F#5 o · B5 o · C#6 o · D6 o · C#6 p · B5 p |
| 26 | 0:42,0 | A7 | E5 o · F#5 o · G5 o · E5 o · C#5 d |
| 27 | 0:43,6 | D | D5 o · E5 o · F#5 o · G5 o · A5 p · G5 o · F#5 o |
| 28 | 0:45,3 | A7 | E5 p · C#5 p · A4 p · pauză p |

### II. Tema lirică (clarinet)

| Măs. | Timp | Acorduri | Note (durată) |
|---|---|---|---|
| 3 | 1:16,4 | Bb | F4 p. · G4 o · Bb4 p |
| 4 | 1:18,9 | Gm | D5 d · C5 p |
| 5 | 1:21,4 | Eb | Bb4 p · A4 o · G4 o · Eb4 p |
| 6 | 1:23,9 | F | C5 d · A4 p |
| 7 | 1:26,4 | Bb | F4 p. · G4 o · Bb4 p |
| 8 | 1:28,9 | Dm | F5 d · D5 p |
| 9 | 1:31,4 | Cm (2 timpi) – F7 (1 timp) | Eb5 p · D5 o · C5 o · A4 p |
| 10 | 1:33,9 | Bb | Bb4 d. |

### II. Mijlocul (flaut)

| Măs. | Timp | Acorduri | Note (durată) |
|---|---|---|---|
| 11 | 1:36,4 | Gm | D5 p · G5 p. · F5 o |
| 12 | 1:38,9 | Eb | Eb5 p · Bb5 p. · G5 o |
| 13 | 1:41,4 | F7 | F5 p · C6 p. · A5 o |
| 14 | 1:43,9 | Bb (2 timpi) – F7 (1 timp) | Bb5 d · A5 p |

### II. Coda: motivul orașului (clarinet, apoi flaut)

| Măs. | Timp | Acorduri | Note (durată) |
|---|---|---|---|
| 23 | 2:06,4 | Bb | F4 p · Bb4 p. · C5 o |
| 24 | 2:08,9 | Gm7 | D5 p · G5 p · F5 p |
| 25 | 2:11,4 | Eb (2 timpi) – F7 (1 timp) | Eb5 p · G5 p · A5 p |
| 26 | 2:13,9 | Bb | Bb5 d. |

### III. Maestoso: motivul orașului (trompete; corni și tromboni în octave, dedesubt)

| Măs. | Timp | Acorduri | Note (durată) |
|---|---|---|---|
| 2 | 2:24,9 | D | A4 p · D5 p. · E5 o · F#5 p |
| 3 | 2:28,1 | G (1 timp) – D (3 timpi) | B5 p · A5 d. |

### III. Tema festivă (trompete și viori)

| Măs. | Timp | Acorduri | Note (durată) |
|---|---|---|---|
| 5 | 2:34,4 | D | D5 p. · A4 o · D5 p · F#5 p |
| 6 | 2:36,2 | A7 | E5 o. · F#5 ș · G5 p · E5 p · C#5 p |
| 7 | 2:38,0 | D | D5 p. · F#5 o · A5 p · D6 p |
| 8 | 2:39,9 | G (2 timpi) – D (2 timpi) | B5 p. · A5 o · A5 d |
| 9 | 2:41,7 | Em (2 timpi) – D (2 timpi) | G5 p. · B5 o · A5 p · F#5 p |
| 10 | 2:43,5 | A7 | E5 p · A5 p · G5 p · E5 p |
| 11 | 2:45,3 | D (2 timpi) – A7 (2 timpi) | F#5 o · G5 o · A5 p · G5 o · E5 o · C#5 p |
| 12 | 2:47,1 | D | D5 d · pauză d |


## Legătura cu Sibiul

Piesa nu descrie un concert real; imaginile ei pornesc de la câteva fapte despre viața culturală a orașului (fișa de fapte verificate a proiectului):

- **Muzica de orchestră are la Sibiu o istorie lungă.** În 1774 a avut loc primul concert al unei orchestre profesioniste la curtea lui Samuel von Brukenthal; tot la Sibiu s-au cântat, în 1792, „Răpirea din Serai” de Mozart și, în 1800, „Creațiunea” de Haydn (en.wikipedia, pagina Filarmonicii de Stat Sibiu). Sursele nu spun ce s-a cântat la concertul din 1774, de aceea piesa nu imită acea muzică.
- **Filarmonica de Stat Sibiu** a fost fondată la 1 ianuarie 1949. Din 2004 are sediul în Sala Thalia (inaugurarea oficială – 7 octombrie 2004).
- **Sala Thalia** este prima clădire de teatru de pe actualul teritoriu al României. A fost ridicată de tipograful Martin Hochmeister în zona Turnului Gros: după en.wikipedia, construcția a început în 1787 și s-a terminat în iunie 1788; după altă sursă din fișă (tnrs.ro), teatrul a fost inaugurat la 1 iunie 1788, după un an de lucru. De aici vine imaginea mișcării a III-a – cortina care se ridică.
- **Lectura:** în 1869 s-a deschis la Sibiu prima bibliotecă publică românească din Transilvania, Biblioteca Asociațiunii. Mișcarea a II-a e o pagină de liniște gândită pentru o sală de lectură, fără să descrie o bibliotecă anume.
- **Piața Mare** din mișcarea I este o dimineață imaginată, nu descrierea unei zile reale.

## Ce înseamnă o uvertură

Verificat pe en.wikipedia (paginile „Overture”, „Movement (music)” și „Tempo”; detalii în `_fapte_noi_A21.md`):

- Cuvântul vine din franceză: *ouverture* înseamnă „deschidere”.
- În secolul al XVII-lea, uvertura era introducerea instrumentală a unui balet, a unei opere sau a unui oratoriu. În opera secolului al XIX-lea, uvertura este, în general, muzica de dinainte de ridicarea cortinei.
- Două forme vechi: **uvertura franceză** (legată de Jean-Baptiste Lully) începe lent, într-un ritm „punctat”, și continuă repede; **uvertura italiană** (din anii 1680, impusă mai ales de operele lui Alessandro Scarlatti) are, de regulă, trei părți: repede – lent – repede. Uverturile italiene erau adesea cântate separat, în concert, și au contat în istoria timpurie a simfoniei.
- **Uvertura de concert**, apărută la începutul epocii romantice, este o piesă de sine stătătoare, fără spectacol după ea; prima e socotită, în general, „Visul unei nopți de vară” de Mendelssohn.
- O **mișcare** este o parte de sine stătătoare a unei compoziții; de cele mai multe ori mișcările se succedă în ordinea repede – lent – repede sau în altă ordine care creează contrast.

„Piață, pagină, cortină” este, așadar, o uvertură de concert (nu deschide nicio operă), cu trei mișcări în ordinea repede – lent – repede, ca uvertura italiană – dar cu mișcări mai lungi și cu un final festiv. Timpanele sintetizate sunt „acordate” pe Re (tonica) și La (dominanta): en.wikipedia notează că în secolele al XVII-lea și al XVIII-lea timpanele erau aproape întotdeauna acordate așa.

## Ce e real și ce e imaginat

| Element | Statut | Sursa / explicația |
|---|---|---|
| Melodiile, armoniile, orchestrația | **originale** – compuse pentru acest artefact | temă originală în stil de uvertură de concert; fără citate din lucrări existente |
| Titlul și titlurile mișcărilor | **inventate** | o căutare pe web a titlului exact (8 octombrie 2026) nu a găsit o lucrare cu acest nume |
| Sunetul orchestrei | **sintetizat în cod** – aproximare, nu înregistrare | oscilatoare, sinteză aditivă și modală, coarde ciupite Karplus-Strong, zgomot filtrat, reverberație sintetică; fără mostre |
| Piața, sala de lectură, cortina | **imagini evocate**, nu locuri sau spectacole descrise | piesa nu a fost cântată la Sibiu, de Filarmonică sau în Sala Thalia |
| 1774, 1792, 1800, 1949, 2004, 1787–1788, 1869 | **fapte** | fișa de fapte, secțiunile „Cultură vie… – Muzică / Teatru / Biblioteci” și „Teatrul din 1788” |
| Uvertură, mișcare, tempo, timpane | **informații generale verificate** | en.wikipedia, în `_fapte_noi_A21.md` |

**O precizare cinstită:** game, arpegii și cadențe scurte se găsesc în multe piese tonale. Temele au fost scrise notă cu notă pentru această uvertură, fără să copieze vreo melodie cunoscută, dar nu putem garanta că nicio succesiune scurtă de note nu seamănă, întâmplător, cu ceva existent.

## Cum a fost făcută (pe scurt)

1. **Planul:** trei imagini ale orașului, trei mișcări contrastante (repede – lent – repede), un motiv comun de șase note.
2. **Partitura, ca text:** fiecare măsură e scrisă în cod ca un șir „notă:durată” (de exemplu „A4:1 D5:1.5 E5:.5 F#5:1”), cu acordurile alături; programul verifică singur că fiecare măsură are numărul corect de timpi.
3. **Orchestrația:** fiecărui instrument i se dă o formulă de sunet (de exemplu, viorile – mai multe unde „dinte de fierăstrău” ușor dezacordate, cu vibrato și filtre care imită cutia de rezonanță; timpanele – vibrațiile unei membrane, ca sumă de sinusoide care se sting).
4. **Mixajul:** fiecare grup de instrumente primește nivelul și locul lui în stereo, apoi o reverberație de sală, tot sintetică; la final, nivelul general este adus la −14 LUFS, fără ca vârfurile să treacă de −1 dBTP.
5. **Verificarea, „cu urechea” unui program:** spectrograma (mișcările se văd clar separate), loudness-ul, căutarea de clipping și de salturi bruște (tăieturi), tonalitatea estimată a fiecărei mișcări (Re major, Si bemol major, Re major – confirmate), tempoul estimat din atacurile notelor (mișcarea I: circa 72 de bătăi pe minut, adică o bătaie la fiecare două pătrimi din cele 144; mișcarea a II-a: 72; partea Allegro a mișcării a III-a: 132 – toate compatibile cu tempourile scrise) și recunoașterea notelor melodiilor principale în MP3 (217 din 217 note recunoscute; 207 exact la octava scrisă, restul la octava de jos, unde tema e dublată de corni sau tromboni).

## Cum se folosește în clasă

1. **Prima ascultare, cu ochii închiși:** ce imagine vă trezește fiecare mișcare? Abia apoi citiți titlurile.
2. **A doua ascultare, cu tabelul de marcaje:** urmăriți intrările instrumentelor; ridicați mâna când auziți motivul orașului (de cel puțin cinci ori în toată piesa).
3. **Comparați mișcările:** tempo (bateți pătrimile), măsura (numărați „1-2-3-4” sau „1-2-3”), tonalitate (luminos sau mai „umbrit”), instrumentele principale.
4. **Cântați motivul orașului** la un instrument din clasă sau cu vocea: la – re – mi – fa diez – si – la.

## Prompt-model pentru clasă

1. Alegeți trei locuri sau momente din orașul vostru, potrivite pentru trei mișcări contrastante (repede – lent – repede).
2. Cereți unui asistent AI gratuit: „Ajută-mă să plănuiesc o uvertură instrumentală originală de circa 3 minute, în 3 mișcări (repede – lent – repede), despre orașul [X]. Pentru fiecare mișcare propune un titlu scurt, inventat, o tonalitate, un tempo în bătăi pe minut, măsura și instrumentele principale. Propune și un motiv scurt, de 5–6 note, care să revină în toate mișcările. Nu cita și nu imita melodii existente și nu folosi titluri care sună a cântece populare reale.”
3. Pentru sunet: compuneți melodiile la un instrument sau într-un editor de partituri gratuit; sau folosiți un generator de muzică cu AI care are plan gratuit (verificați condițiile actuale și vârsta minimă), cerând „uvertură orchestrală instrumentală, fără voce, trei mișcări: vioaie – lentă și lirică – festivă, circa 3 minute”.
4. Dacă legați piesa de istoria orașului, luați faptele (ani, instituții) dintr-o sursă verificată și notați sursa.
5. Pe eticheta piesei scrieți: „temă originală”, cine sau ce a compus melodiile, cu ce s-a produs sunetul (instrumente reale, sinteză sau generator AI) și ce titluri sunt inventate.

### Întrebări de reflecție

1. Prin ce se deosebește mișcarea a II-a de celelalte două: tempo, măsură, tonalitate, instrumente? Care dintre ele v-a schimbat cel mai mult starea?
2. Motivul orașului revine în toate mișcările. Ce face muzica, schimbându-i instrumentul, tempoul sau tonalitatea, ca să sune altfel de fiecare dată?
3. O orchestră sintetizată nu este o orchestră reală. Ce s-ar schimba dacă piesa ar fi cântată de muzicieni într-o sală? De ce e important să spunem pe etichetă cum a fost făcut sunetul?
