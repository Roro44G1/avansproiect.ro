# BRIEF COMUN – Artefacte-model ACTIV AI (expoziția finală)

## Context
- Proiect: ACTIV AI (Asociația AVANS PROIECT Sibiu, cofinanțat de Primăria Municipiului Sibiu – Agenda Comunității 2026). Tema-umbrelă: „Sibiul meu – locuri, povești și oameni prin ochii inteligenței artificiale”.
- Expoziția se afișează EXCLUSIV PE ECRANE (format digital interactiv): galerie animată + piese interactive + cod QR.
- Lista de teme: `/home/claude/expo/_brief/lista_artefacte.md`. Fapte verificate: `/home/claude/expo/_brief/fapte_verificate.md`.

## Regula de onestitate (obligatorie)
- Aceste piese sunt ARTEFACTE-MODEL, generate cu AI (Claude, Anthropic) de echipa de proiect, ca exemple demonstrative pentru clase. NU se atribuie unor elevi reali, nu se inventează nume de elevi, clase sau școli autoare.
- Pe fiecare piesă vizuală, în subsol: „ACTIV AI · Sibiul meu · Artefact-model generat cu AI”.
- Personaje (bunici, strămoși, colegi, profesori, familii) = FICTIVE și declarate ca atare („personaj fictiv”). Fără nume de persoane reale în viață.
- Afirmațiile istorice/statistice se iau DOAR din `fapte_verificate.md`. Ce nu e acolo se formulează explicit ca imaginar/ficțiune sau se omite. Nu inventați date, cifre, citate, nume de localuri sau firme.
- Fără reproducerea textelor protejate (ex.: niciun vers de Blaga; doar stil original „în maniera”).
- Muzică: fie teme originale, numite explicit așa („temă originală în stil de…”), fie melodii tradiționale documentate, cu sursa notată (partitură, culegere, aranjor). NICIODATĂ titluri inventate care sună a piese folclorice reale (ex. „Hora de pe Cibin” – retras). Genul de referință pentru zona Sibiului este jiana de Mărginime (2/4, vioi, fluier/vioară); melodia de referință a expoziției este „Hai, mândruță, la poiană” (partitură N. Bădilă & P. Duca, pusă la dispoziție de coordonator), folosită în A08/M04.

## Limbă și stil
- Limba română corectă, cu diacritice ș, ț (virgulă dedesubt, U+0219/U+021B), ă, â, î. Titluri cu majusculă doar la început și la nume proprii (nu Title Case american).
- Ton: accesibil, cald, potrivit pentru liceeni și public larg. Fără superlative goale.
- Ghilimele românești „…” în texte; în cod JS/Node folosiți ghilimele ASCII pentru delimitarea stringurilor.

## Identitate vizuală ACTIV AI (pentru ecran)
| Rol | Nume | Hex |
|---|---|---|
| Fundal ecran | Noapte Cibin | #0F1720 |
| Suprafață/carduri | Ardezie | #1B2733 |
| Primar | Petrol | #0E7C86 |
| Secundar | Violet AI | #6E56CF |
| Accent | Ocru | #E2A62B |
| Accent cald (doar ilustrații) | Țiglă | #B9583A |
| Text pe fundal închis | Var | #F3EFE6 |
| Text secundar | Ceață | #A9B4C0 |
| Fundal deschis (variantă) | Zid | #F5F1EA |

- Fonturi: titluri „Noto Serif” (bold), text „Inter” (fallback: sans-serif). Ambele există local (fontconfig) – rsvg-convert le găsește.
- Format ecran: 1920×1080 px (16:9). Zone sigure: margini de 80 px.
- Șablon cadru (pentru PNG-uri de ecran): bandă sus (chip categorie cu culoarea categoriei + titlul piesei, Noto Serif 54–64 px), zona artefactului, subsol 40 px cu eticheta de onestitate (Inter 22 px, #A9B4C0) și „#SibiulMeu” la dreapta.
- Culori categorii (chip): Vizual #E2A62B · Video #E5484D · Literar #6E56CF · Audio #12A594 · Spațial #0E7C86 · Date #3E63DD · Interactiv #D6409F · Identitate #F76B15.

## Fișiere
- Rădăcina: `/home/claude/expo/`. Subfoldere: `01_vizual`, `02_video`, `03_literar`, `04_audio`, `05_spatial`, `06_date`, `07_interactiv`, `08_identitate`.
- Denumire: `<cod>_<slug>.<ext>`, ex.: `L03_scrisoare_sibiu_2126.md`, `S01_harta_amintirilor.svg` + `.png`.
- Coduri: V01–V17 vizual static, M01–M09 video, L01–L15 literar, A01–A08 audio, S01–S07 spațial, D01–D05 date, I01–I06 interactiv, P01–P06 identitate (în ordinea din listă).
- Randare SVG → PNG: `rsvg-convert -w 1920 -h 1080 in.svg -o out.png` (verificați vizual PNG-ul cu Read).
- Fiecare agent scrie la final un fișier `<folder>/_manifest.json`: listă de obiecte
  `{"cod","categorie","titlu" (exact ca în listă),"fisiere":[...],"tip":"text|imagine|html|video|audio|scenariu","instrument":"ex. Claude (Anthropic) – text / cod SVG","descriere" (1–2 propoziții pentru vizitator),"status":"realizat|realizat-partial|necesita-material-personal","nota" (opțional)}`.

## HTML interactiv
- Un singur fișier per piesă, autonom (CSS+JS inline, fără resurse externe, fără CDN, fără localStorage obligatoriu), responsive, utilizabil pe ecran tactil și cu mouse, butoane mari (min 56 px), text min 20 px pe ecran mare.
- Paleta și fonturile de mai sus (font-family: "Noto Serif", Georgia, serif / "Inter", system-ui, sans-serif).
- `<html lang="ro">`, `<meta charset="utf-8">`, titlu scurt.
