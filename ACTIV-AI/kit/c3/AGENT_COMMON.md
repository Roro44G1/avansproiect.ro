# Instrucțiuni comune pentru agenții Calupului 3 (ACTIV AI – „Cartierele Sibiului”)

Lucrezi la artefacte-model pentru expoziția digitală ACTIV AI („Sibiul meu – locuri, povești și oameni prin ochii AI”), proiect al Asociației AVANS PROIECT Sibiu. Piesele sunt exemple realizate cu AI de echipa de proiect, NU lucrări ale elevilor. Lucrezi autonom, fără întrebări, în limba română.

## Citește înainte de orice
1. `/home/claude/expo/_brief/BRIEF.md` – reguli comune (onestitate, identitate vizuală, fișiere, manifest, HTML interactiv).
2. `/home/claude/expo/c3/BRIEF_C3.md` – reguli ale calupului, lista celor 20 de teme (titlurile EXACTE), așezarea cartierelor pe hărți.
3. `/home/claude/expo/_brief/fapte_verificate.md` – singura sursă de fapte. Secțiunile esențiale: „Date generale”, „Cartiere – originea numelor”, „Terezian – completări”, „Tramvaiul”, „Cartierele Sibiului – completări pentru Calupul 3”. Ce nu e în fișă NU se afirmă ca fapt: se declară imaginat sau se omite. Nu inventa cifre, date, citate, nume de localuri/firme/persoane. Fără cifre de populație pe cartiere. Divergențele între surse se arată ca atare.

## Reguli de bază
- Română corectă, diacritice ș/ț cu virgulă (U+0219/U+021B), ă, â, î. Titluri cu majusculă doar la început (fără Title Case). Ghilimele „…”.
- Pe fiecare piesă vizuală: subsol „ACTIV AI · Sibiul meu · Artefact-model generat cu AI” (Inter 22 px, #A9B4C0) și „#SibiulMeu” în dreapta (ocru #E2A62B); chip de categorie sus („SPAȚIAL · S13”). Cadru 1920×1080, margini 80 px.
- Paleta: fundal #0F1720, carduri #1B2733, petrol #0E7C86, violet #6E56CF, ocru #E2A62B, țiglă #B9583A, var #F3EFE6, ceață #A9B4C0, zid #F5F1EA. Culori chip: Vizual #E2A62B · Video #E5484D · Literar #6E56CF · Audio #12A594 · Spațial #0E7C86 · Date #3E63DD · Interactiv #D6409F · Identitate #F76B15. Fonturi: „Noto Serif” (titluri, bold) și „Inter” (text) – instalate local.
- Personaje fictive, declarate. Fără personalități politice în viață. Persoane istorice doar cu faptele din fișă.
- Hărțile sunt schematice, cu poziții aproximative (declarat pe piesă). Coordonate normalizate COMUNE (x spre est, y spre sud, centrul istoric = 0,0; scalează-le cum vrei, dar păstrează-le relativ):
  Centrul istoric (0,0) · Trei Stejari (0.05,0.28) · Terezian (0,-0.45) · Țiglari (-0.3,-0.78) · Lazaret (0.45,-0.15) · Broscărie (0.82,0.05) · Vasile Aaron (0.62,0.45) · Ștrand (-0.62,0.1) · Turnișor (-0.88,-0.3) · Valea Aurie (-0.55,0.78) — verificate de surse ca direcție;
  Gușterița (0.75,-0.62) · Hipodrom (0.25,0.65) · Dumbrăvii (-0.15,0.72) · Piața Cluj (-0.48,-0.45) — „poziție orientativă” (marcată ca atare);
  Lupeni, Reșița, Tilișca, Tineretului, Veteranilor de Război, Viile Sibiului — NU se pun pe hartă; apar într-o casetă separată („de localizat de elevi pe o hartă reală”) sau deloc.
- Nu modifica fișiere în afara folderului tău de lucru, cu excepția scripturilor NOI pe care le creezi (ex. `/home/claude/expo/_tools/svg/s13.py`, `/home/claude/expo/_tools/video/M15_*.html`). NU modifica `lib.py`, `lib.js`, `audiolib.py`, `mapbase.py`, `sibiu_map.py` – importă-le sau copiază funcții în scriptul tău.

## Unelte disponibile
- SVG: `/home/claude/expo/_tools/svg/lib.py` (frame_head, frame_foot, text, para, card, pin, svg_open/close, write), `sibiu_map.py` (geometria centrului istoric), `mapbase.py`; modele `s11.py`, `s12.py`, `d08.py`, `d09.py`, `d10.py`, `p09.py`–`p11.py`. Randare: `rsvg-convert -w 1920 -h 1080 in.svg -o out.png`. librsvg NU redă `textPath` (așază literele manual). Evită fonturi/emoji care lipsesc (folosește forme SVG, nu emoji).
- Video: `/home/claude/expo/_tools/video/lib.js` (setupCanvas, text, serif, chip, footer, roundRect, rgba, smooth, inv, lerp, easeInOut, rng, PAL; `mix()` NU acceptă hex scurt ca „#000”), modele `M12_sibiul_primelor.html`, `M13_primul_muzeu.html`, `M14_primul_tramvai.html` (HTML Canvas determinist: `window.render(t)`, `window.READY=true`). Previzualizare: `python3 /home/claude/expo/_tools/preview_frames.py in.html out.jpg 2,15,30,55`; randare: `python3 /home/claude/expo/_tools/render_video.py in.html out.mp4 --dur S --audio x.mp3 --fadeout 2 [--env]`.
- Audio: `/home/claude/expo/04_audio/_src/audiolib.py` (sinteză, −14 LUFS, true peak ≤ −1 dBTP, MP3 192 kbps, `finalize`, `report`; vezi `A08_remix_modern.py` și `/home/claude/expo/c2/04_audio/_src/A12_tramvai.py`). Fără TTS online (blocat): vocea se redă în galerie prin Web Speech API din fișierul `.txt` (cifre scrise în litere, „Activ A I”, replici prefixate cu numele vorbitorului).
- HTML interactiv: un singur fișier autonom (fără CDN, fără resurse externe), `lang="ro"`, butoane ≥ 56 px, text ≥ 20 px, paleta de mai sus; testat cu Playwright (Python, Chromium din /opt/pw-browsers) la 1920×1080 și 390×844, fără erori în consolă; captura ecranului de start salvată ca `IXX_preview.png` (1920×1080). Modele: `/home/claude/expo/_ref/I10_memorie_premiere.html`, `/home/claude/expo/_ref/I11_masina_timpului.html`.
- Instrumente: python3 (numpy, scipy, PIL, matplotlib, playwright), ffmpeg/ffprobe, rsvg-convert, pandoc, hunspell.

## Verificare obligatorie (înainte de a raporta)
- Privește fiecare PNG cu Read (text care iese din chenare, suprapuneri, lizibilitate). Corectează și re-randează până e curat.
- Ortografie: `cat f | sed 's/`[^`]*`//g' | hunspell -d ro_RO -i utf-8 -l | sort -u` (pentru SVG: `grep -o '>[^<]*<' f.svg | hunspell -d ro_RO -i utf-8 -l | sort -u`; pentru HTML extrage textul). Corectează greșelile reale (numele proprii pot rămâne). Fără „ş/ţ” cu sedilă: `grep -c '[şţŞŢ]' f` trebuie să dea 0.
- Fapte: fiecare afirmație istorică are corespondent în fișa de fapte.

## Manifest
La final scrie `/home/claude/expo/c3/<folderul tău>/_manifest.json` (dacă alt agent lucrează în același folder, scrie `_manifest_<coduri>.json`, ex. `_manifest_I14.json`): listă JSON de obiecte
`{"cod","categorie","titlu" (EXACT din BRIEF_C3, după „COD ”),"fisiere":[căi relative la /home/claude/expo/c3, ex. "05_spatial/S13_harta_numelor.svg","05_spatial/S13_harta_numelor.png"],"tip":"text|imagine|html|video|audio|scenariu","instrument","descriere" (1–2 propoziții pentru vizitator),"status":"realizat","nota" (surse, ce e fictiv, ce e aproximativ)}`; pentru audio și: `"audio"` (cale relativă), `"tts_text"`, `"tts_lang":"ro-RO"`, `"durata_s"`, `"loudness_lufs"`, `"true_peak_dbtp"`, `"titlu_creativ"`; pentru video: `"durata_s"`; pentru literar: `"titlu_creativ"`.
Categoriile: „Vizual”, „Video”, „Literar”, „Audio”, „Spațial”, „Date”, „Interactiv”, „Identitate”.

## Raport final (răspunsul tău)
Maximum 150 de cuvinte: fișierele produse, ce ai verificat, orice problemă rămasă sau decizie de onestitate (ce ai declarat fictiv/aproximativ).
