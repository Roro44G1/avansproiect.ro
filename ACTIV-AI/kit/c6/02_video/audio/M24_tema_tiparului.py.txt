"""M24 – fundal sonor pentru „Istoria tiparului la Sibiu (1525, 1544) — animație AI” (74 s).

Temă ORIGINALĂ, compusă și sintetizată în cod pentru animația M24 (artefact-model ACTIV AI),
în stil renascentist (dans în 3/4): flaut drept (blockflöte) sintetizat, lăută ciupită (Karplus-Strong),
violă de gambă (bas arcuit) și o tobă cu ramă. Modul re doric, 90 BPM, 3/4 (o măsură = 2 s).
Nu citează și nu imită o melodie existentă; nu are titlu de piesă reală.

Peste muzică: SUNETE DE ATELIER SINTETIZATE (declarate ca atare), sincronizate cu imaginea:
metal topit turnat, clinchet de litere de plumb, ciocănele de lemn (pene), tampoane de cerneală,
foșnet de hârtie, picături, scârțâit de șurub de lemn, bufnitura presei, rularea carului, cusut, copertă.
Totul este sintetizat din formule (oscilatoare, Karplus-Strong, sinteză modală, zgomot filtrat) – fără eșantioane.

Cronologia (aceeași ca în _tools/video/M24_istoria_tiparului.html):
   0– 4 s  titlul                         (măsurile 0–1: introducere, clopot)
   4–32 s  Partea I – 8 pași × 3,5 s      (măsurile 2–15: tema A + A')
  32–34 s  cartonul „Partea a II-a”       (măsura 16: dominantă, urcare)
  34–66 s  Partea a II-a – 8 date         (măsurile 17–24: tema B; 25–32: tema A, tutti)
  66–74 s  cadrul de onestitate           (măsurile 33–36: cadență, acord final)

Folosește biblioteca comună /home/claude/expo/04_audio/_src/audiolib.py.
Rulare: python3 M24_tema_tiparului.py  -> M24_tema_tiparului.mp3 (în același folder)
"""
import os
import sys

import numpy as np
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = "/home/claude/expo/04_audio/_src"
if LIB not in sys.path:
    sys.path.insert(0, LIB)

from audiolib import (add, additive, bp, colored_noise, env_adsr, env_ar, finalize, hp, hz, kick, ks_pluck,
                      limiter, lp, make_ir, match_lufs, modal, ns, report, reverb, rng_of, saw, smooth_random, stereo,
                      t_axis, vibrato)

BPM = 90
BEAT = 60.0 / BPM          # 0,667 s
BAR = 3 * BEAT             # 2,0 s
DUR = 74.0
OUT = os.path.join(HERE, "M24_tema_tiparului.mp3")

# cronologia imaginii (identică cu HTML-ul)
P1, STEP = 4.0, 3.5
TR0, P2 = 32.0, 34.0
EDUR = [5.5, 4.0, 4.0, 4.5, 3.0, 3.5, 4.5, 3.0]
ESTART = [P2 + sum(EDUR[:i]) for i in range(8)]
FIN = 66.0


def b2t(bar, beat=0.0):
    return bar * BAR + beat * BEAT


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-12)


# ------------------------------------------------------------------ instrumente
def recorder(f, dur, rng):
    """Flaut drept: puține armonice, suflu filtrat, „chiff” scurt la atac, vibrato discret."""
    n = ns(dur + 0.1)
    t = t_axis(n)
    fr = vibrato(n, f, rate=5.0, depth_semitones=0.08, delay=0.25, rng=rng)
    x = additive(fr, [1.0, 0.16, 0.07, 0.025])
    breath = bp(rng.standard_normal(n), f * 0.9, min(f * 4.0, 15000)) * 0.045
    chiff = np.exp(-t / 0.025) * bp(rng.standard_normal(n), 1800, 7000) * 0.12
    return (x + breath + chiff) * env_adsr(n, 0.03, 0.08, 0.85, 0.08)


def lute(f, dur, rng, bright=0.42):
    x = ks_pluck(f, dur + 0.4, t60=1.5, bright=bright, pos=0.21, rng=rng, damp=0.25)
    n = len(x)
    return x * env_adsr(n, 0.001, 0.05, 1.0, 0.25)


def viol(f, dur, rng):
    """Violă de gambă (bas arcuit): fierăstrău filtrat, atac moale de arcuș, vibrato lent."""
    n = ns(dur + 0.15)
    t = t_axis(n)
    fr = vibrato(n, f, rate=4.6, depth_semitones=0.06, delay=0.3, rng=rng)
    x = saw(fr, phase0=rng.uniform())
    x = lp(x, 900) * 0.8 + lp(x, 2400) * 0.2
    bow = bp(rng.standard_normal(n), 300, 2500) * 0.04 * np.exp(-t / 0.08)
    return (x + bow) * env_adsr(n, 0.07, 0.15, 0.8, 0.14)


def tabor(rng, vel=1.0):
    body = modal([92, 151, 233, 318], [1.0, 0.55, 0.3, 0.15], [0.22, 0.14, 0.09, 0.06], 0.45, rng=rng)
    n = len(body)
    skin = lp(rng.standard_normal(n), 1800) * env_ar(n, 0.001, 0.05) * 0.5
    return vel * norm(body + skin)


def bell(f, rng, dur=4.0):
    ratios = [0.5, 1.0, 1.19, 1.5, 2.0, 2.52, 3.0]
    amps = [0.45, 1.0, 0.5, 0.35, 0.3, 0.18, 0.1]
    t60 = [3.5, 2.8, 2.2, 1.8, 1.3, 1.0, 0.8]
    return norm(modal([f * r for r in ratios], amps, t60, dur, rng=rng, beat_hz=1.2))


# ------------------------------------------------------------------ efecte de atelier (sintetizate)
def click_metal(rng, soft=1.0):
    k = rng.uniform(0.93, 1.07)
    x = modal([2300 * k, 3720 * k, 5180 * k, 6900 * k], [1, .6, .35, .2], [.05, .04, .03, .02], 0.12, rng=rng, attack=0.0002)
    n = len(x)
    x = norm(x) + 0.35 * hp(rng.standard_normal(n), 3000) * env_ar(n, 0.0002, 0.006)
    return soft * norm(x)


def wood_knock(rng, f0=420.0):
    x = modal([f0, f0 * 2.31, f0 * 3.93], [1, .5, .25], [.09, .05, .03], 0.22, rng=rng, attack=0.0003)
    n = len(x)
    x = norm(x) + 0.4 * bp(rng.standard_normal(n), 500, 2500) * env_ar(n, 0.0003, 0.012)
    return norm(x)


def thump_heavy(rng):
    k = kick(dur=0.7, f_hi=105, f_lo=44, pitch_tau=0.03, t60=0.45, click=0.04, rng=rng)
    n = len(k)
    w = np.zeros(n); kn = wood_knock(rng, 175); w[:len(kn)] = kn[:n]
    nz = lp(rng.standard_normal(n), 300) * env_ar(n, 0.001, 0.18)
    return norm(k + 0.55 * w + 0.4 * norm(nz))


def creak(rng, dur, r0=28.0, r1=55.0):
    """Scârțâit de șurub de lemn: impulsuri de tip „stick-slip” trecute prin rezonanțe."""
    n = ns(dur)
    imp = np.zeros(n)
    t = 0.0
    while t < dur:
        i = ns(t)
        if i < n:
            imp[i] = rng.uniform(0.4, 1.0)
        rate = (r0 + (r1 - r0) * t / dur) * (1 + 0.25 * rng.standard_normal())
        t += 1.0 / max(8.0, rate)
    resp = modal([540, 1170, 1930, 2650], [1, .7, .45, .2], [.035, .03, .022, .015], 0.09, rng=rng, attack=0.0002)
    y = signal.oaconvolve(imp, resp)[:n]
    y = norm(y) + 0.12 * bp(rng.standard_normal(n), 900, 3200) * smooth_random(n, rng, 8, 0.3, 1.0)
    e = np.minimum(1, np.minimum(t_axis(n) / 0.06, (dur - t_axis(n)) / 0.08))
    return norm(y * np.clip(e, 0, 1))


def roll(rng, dur):
    n = ns(dur)
    x = lp(colored_noise(n, rng, 2.0), 260)
    bumps = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 6.5 * t_axis(n)))
    e = np.sin(np.pi * np.clip(t_axis(n) / dur, 0, 1)) ** 0.7
    return norm(x * bumps * e)


def sizzle(rng, dur):
    n = ns(dur)
    x = hp(rng.standard_normal(n), 2500) * smooth_random(n, rng, 14, 0.3, 1.0)
    bub = np.zeros(n)
    for _ in range(int(dur * 18)):
        t0 = rng.uniform(0, dur - 0.05); f = rng.uniform(280, 900); m = ns(0.03)
        tt = t_axis(m); i = ns(t0)
        bub[i:i + m] += np.sin(2 * np.pi * f * tt * (1 + 2 * tt)) * np.exp(-tt / 0.008) * rng.uniform(.3, 1)
    e = np.minimum(1, np.minimum(t_axis(n) / 0.1, (dur - t_axis(n)) / 0.25))
    return norm((0.5 * norm(x) + 0.5 * norm(bub)) * np.clip(e, 0, 1))


def scrape(rng, dur):
    n = ns(dur)
    x = bp(rng.standard_normal(n), 1500, 6500) * smooth_random(n, rng, 20, 0.2, 1.0)
    e = np.sin(np.pi * np.clip(t_axis(n) / dur, 0, 1))
    return norm(x * e)


def paper(rng, dur):
    n = ns(dur)
    crack = np.zeros(n)
    k = int(dur * 260)
    idx = rng.integers(0, n, k)
    crack[idx] = rng.uniform(-1, 1, k)
    crack = bp(crack, 1500, 9000)
    hiss = bp(rng.standard_normal(n), 900, 6000) * smooth_random(n, rng, 10, 0.1, 1.0)
    e = np.sin(np.pi * np.clip(t_axis(n) / dur, 0, 1)) ** 0.6
    return norm((norm(crack) + 0.5 * norm(hiss)) * e)


def swish(rng, dur):
    n = ns(dur)
    x = bp(rng.standard_normal(n), 700, 5000)
    e = np.sin(np.pi * np.clip(t_axis(n) / dur, 0, 1)) ** 2
    return norm(x * e)


def dab(rng):
    x = modal([105, 185, 320], [1, .5, .25], [.07, .045, .03], 0.22, rng=rng, attack=0.002)
    n = len(x)
    tack = bp(rng.standard_normal(n), 1200, 4200) * env_ar(n, 0.001, 0.02)
    pad = lp(rng.standard_normal(n), 700) * env_ar(n, 0.002, 0.05)
    return norm(norm(x) + 0.35 * norm(tack) + 0.5 * norm(pad))


def drip(rng):
    m = ns(0.08)
    t = t_axis(m)
    f0 = rng.uniform(900, 1300)
    ph = 2 * np.pi * np.cumsum(f0 * (1 + 1.2 * (1 - np.exp(-t / 0.012)))) / 44100
    return norm(np.sin(ph) * np.exp(-t / 0.018))


def thread(rng):
    n = ns(0.16)
    t = t_axis(n)
    x = bp(rng.standard_normal(n), 2500, 8000) * (t / 0.16) ** 1.5 * (t < 0.15)
    return norm(x)


def leather_thud(rng):
    x = modal([130, 240, 410], [1, .45, .2], [.08, .05, .03], 0.25, rng=rng, attack=0.002)
    n = len(x)
    return norm(norm(x) + 0.5 * norm(lp(rng.standard_normal(n), 500) * env_ar(n, 0.002, 0.06)))


# ------------------------------------------------------------------ materialul muzical (original)
THEME_A = [
    [("D5", 2), ("E5", 1)], [("F5", 1.5), ("E5", .5), ("D5", 1)], [("C5", 2), ("D5", 1)], [("A4", 3)],
    [("D5", 1), ("F5", 1), ("G5", 1)], [("A5", 1.5), ("G5", .5), ("F5", 1)], [("E5", 1), ("D5", 1), ("C#5", 1)], [("D5", 3)],
]
CH_A = ["Dm", "F", "C", "Am", "Dm", "F", "A", "Dm"]
THEME_A2 = [
    [("F5", 1), ("G5", 1), ("A5", 1)], [("Bb5", 2), ("A5", 1)], [("G5", 1.5), ("F5", .5), ("E5", 1)],
    [("F5", 1), ("E5", 1), ("D5", 1)], [("E5", 2), ("C#5", 1)], [("D5", 3)],
]
CH_A2 = ["F", "Gm", "C", "Dm", "A", "Dm"]
THEME_B = [
    [("A5", 2), ("G5", 1)], [("F5", 1), ("G5", 1), ("A5", 1)], [("C6", 2), ("Bb5", 1)], [("A5", 3)],
    [("G5", 1), ("A5", 1), ("Bb5", 1)], [("A5", 1.5), ("G5", .5), ("F5", 1)], [("E5", 1), ("F5", 1), ("G5", 1)], [("A5", 3)],
]
CH_B = ["F", "F", "C", "F", "Gm", "F", "C", "A"]
for ph in THEME_A + THEME_A2 + THEME_B:
    assert abs(sum(d for _, d in ph) - 3) < 1e-9

CH = {"Dm": ["D3", "A3", "D4", "F4"], "F": ["F3", "A3", "C4", "F4"], "C": ["C3", "G3", "C4", "E4"],
      "Am": ["A2", "E3", "A3", "C4"], "A": ["A2", "E3", "A3", "C#4"], "Gm": ["G2", "D3", "G3", "Bb3"],
      "Bb": ["Bb2", "F3", "Bb3", "D4"], "D": ["D3", "A3", "D4", "F#4"]}
ROOT = {"Dm": "D2", "F": "F2", "C": "C2", "Am": "A2", "A": "A2", "Gm": "G2", "Bb": "Bb2", "D": "D2"}


def render(seed=1544):
    rng = rng_of(seed)
    rec, lut, vio, tab, bel, sfx = (stereo(DUR) for _ in range(6))

    def phrase(buf, ph, bar, inst, gain, pan, transpose=0, legato=0.95):
        pos = 0.0
        for nm, d in ph:
            if nm is not None:
                x = inst(hz(nm, transpose), d * BEAT * legato, rng)
                add(buf, x, b2t(bar, pos) + rng.uniform(-0.004, 0.004), gain=gain * rng.uniform(0.9, 1.0), pan=pan)
            pos += d

    def strum(t0, name, gain, up=True):
        notes = CH[name] if up else CH[name][::-1]
        for k, nm in enumerate(notes):
            add(lut, lute(hz(nm), BEAT * 1.6, rng), t0 + k * 0.018, gain=gain * (0.8 + 0.2 * k / 3), pan=-0.25 + 0.12 * k)

    def accomp(bar, name, lvl=1.0):
        strum(b2t(bar), name, 0.9 * lvl)
        add(lut, lute(hz(CH[name][2]), BEAT * 0.9, rng), b2t(bar, 1), gain=0.55 * lvl, pan=0.0)
        for k, nm in enumerate(CH[name][2:]):
            add(lut, lute(hz(nm), BEAT * 0.9, rng), b2t(bar, 2) + k * 0.015, gain=0.6 * lvl, pan=0.1 * k)
        add(vio, viol(hz(ROOT[name]), BAR * 0.92, rng), b2t(bar), gain=lvl)

    def drum(bar, lvl=1.0):
        add(tab, tabor(rng, 1.0), b2t(bar), gain=lvl, pan=0.15)
        add(tab, tabor(rng, 0.55), b2t(bar, 2), gain=lvl, pan=0.15)
        add(tab, tabor(rng, 0.35), b2t(bar, 2.5), gain=lvl, pan=0.15)

    # ---- introducere (măsurile 0–1): clopot, arpegii la lăută, flautul ține nota
    add(bel, bell(hz("D4"), rng), 0.25, gain=0.8, pan=0.1)
    for k, nm in enumerate(["D3", "A3", "D4", "F4", "A4", "D5"]):
        add(lut, lute(hz(nm), 1.2, rng), 0.2 + k * BEAT / 2, gain=0.75, pan=-0.2 + 0.08 * k)
    for k, nm in enumerate(["C3", "G3", "C4", "E4"]):
        add(lut, lute(hz(nm), 1.0, rng), b2t(1) + k * BEAT / 2, gain=0.7, pan=-0.2 + 0.1 * k)
    strum(b2t(1, 2), "A", 0.8)
    add(rec, recorder(hz("A4"), BAR * 0.95, rng), b2t(1), gain=0.7, pan=0.1)
    add(vio, viol(hz("D2"), BAR * 0.95, rng), b2t(0), gain=0.8)
    add(vio, viol(hz("A2"), BAR * 0.95, rng), b2t(1), gain=0.8)

    # ---- Partea I (măsurile 2–15): tema A și A', discret (efectele de atelier sunt în față)
    for k in range(8):
        phrase(rec, THEME_A[k], 2 + k, recorder, 0.85, 0.1)
        accomp(2 + k, CH_A[k], 0.8)
    for k in range(6):
        phrase(rec, THEME_A2[k], 10 + k, recorder, 0.85, 0.1)
        accomp(10 + k, CH_A2[k], 0.8)

    # ---- măsura 16: cartonul „Partea a II-a” – dominanta (La) și urcarea flautului
    phrase(rec, [("A4", 1), ("C#5", 1), ("E5", 1)], 16, recorder, 0.95, 0.1, legato=0.9)
    strum(b2t(16), "A", 1.0)
    strum(b2t(16, 1.5), "A", 0.7, up=False)
    add(vio, viol(hz("A2"), BAR * 0.95, rng), b2t(16), gain=1.0)
    for j, g in enumerate([0.3, 0.4, 0.5, 0.65, 0.8, 1.0]):
        add(tab, tabor(rng, 0.6), b2t(16, 1.5 + j * 0.25), gain=g, pan=0.15)

    # ---- Partea a II-a (măsurile 17–24): tema B, cu toba
    for k in range(8):
        phrase(rec, THEME_B[k], 17 + k, recorder, 1.0, 0.1)
        accomp(17 + k, CH_B[k], 1.0)
        drum(17 + k, 0.8)
    # ---- măsurile 25–32: tema A, tutti (lăuta dublează melodia o octavă mai jos)
    for k in range(8):
        phrase(rec, THEME_A[k], 25 + k, recorder, 1.0, 0.1)
        phrase(lut, THEME_A[k], 25 + k, lambda f, d, r: lute(f, d, r, 0.55), 0.55, -0.3, transpose=-12)
        accomp(25 + k, CH_A[k], 1.0)
        drum(25 + k, 0.9)

    # ---- final (măsurile 33–36): Si bemol – La – Re major, încet
    for bar, name, mel in ((33, "Bb", "F5"), (34, "A", "E5")):
        strum(b2t(bar), name, 0.8)
        add(rec, recorder(hz(mel), BAR * 0.95, rng), b2t(bar), gain=0.8, pan=0.1)
        add(vio, viol(hz(ROOT[name]), BAR * 0.95, rng), b2t(bar), gain=0.85)
    add(tab, tabor(rng, 0.6), b2t(33), gain=0.6, pan=0.15)
    strum(b2t(35), "D", 0.85)
    for k, nm in enumerate(["D4", "F#4", "A4", "D5"]):
        add(lut, lute(hz(nm), 2.0, rng), b2t(35, 1) + k * BEAT / 2, gain=0.5, pan=-0.1 + 0.1 * k)
    add(rec, recorder(hz("D5"), BAR * 1.9, rng), b2t(35), gain=0.75, pan=0.1)
    add(vio, viol(hz("D2"), BAR * 1.9, rng), b2t(35), gain=0.8)
    add(bel, bell(hz("D4"), rng, 4.5), b2t(35), gain=0.6, pan=0.1)

    # ------------------------------------------------------------ efecte de atelier, sincronizate cu imaginea
    def S(x, t, g=1.0, pan=0.0):
        add(sfx, x, t, gain=g, pan=pan)

    s = [P1 + k * STEP for k in range(8)]
    # 1 · literele turnate
    S(sizzle(rng, 1.0), s[0] + 0.5, 0.55, -0.2)
    S(swish(rng, 0.5), s[0] + 1.5, 0.08, -0.1)
    S(wood_knock(rng, 380), s[0] + 2.02, 0.7, -0.15)
    S(scrape(rng, 0.6), s[0] + 2.35, 0.3, 0.1)
    S(click_metal(rng), s[0] + 2.95, 0.6, 0.15)
    # 2 · culegerea: clinchetul literelor în vingalac, apoi spațiile
    for k in range(5):
        S(click_metal(rng), s[1] + 0.25 + k * 0.4 + 0.34, 0.75, -0.3 + 0.12 * k)
    for i in range(5):
        S(click_metal(rng, 0.6), s[1] + 2.3 + i * 0.12 + 0.2, 0.5, 0.2)
    # 3 · forma: rândul alunecă, pagina trece în ramă, pene bătute
    S(scrape(rng, 0.7), s[2] + 0.15, 0.35, -0.3)
    S(scrape(rng, 0.9), s[2] + 1.15, 0.4, 0.0)
    S(wood_knock(rng, 300), s[2] + 2.2, 0.55, 0.2)
    for j, tt in enumerate([2.5, 2.66, 2.82]):
        S(wood_knock(rng, 470 + 30 * j), s[2] + tt, 0.75, 0.3)
    # 4 · cerneala: tampoanele se freacă, apoi tamponează forma (două deodată)
    for j in range(5):
        S(dab(rng), s[3] + 0.25 + j * 0.13, 0.35, -0.3)
    for k in range(5):
        tk = s[3] + 1.05 + k * 0.36 + 0.06
        S(dab(rng), tk, 0.8, -0.15)
        S(dab(rng), tk + 0.012, 0.7, 0.15)
    # 5 · coala: foșnet, picături, rama, coborârea
    S(paper(rng, 0.6), s[4] + 0.1, 0.55, 0.3)
    for i in range(6):
        S(drip(rng), s[4] + 0.6 + i * 0.08 + 0.25, 0.25, 0.1 + 0.05 * i)
    S(wood_knock(rng, 520), s[4] + 1.7, 0.45, 0.25)
    S(swish(rng, 0.8), s[4] + 2.05, 0.35, 0.0)
    S(wood_knock(rng, 340), s[4] + 2.85, 0.8, -0.1)
    # 6 · presa: carul intră, șurubul scârțâie, bufnitura, revenirea, carul iese
    S(roll(rng, 0.75), s[5] + 0.0, 0.6, 0.3)
    S(creak(rng, 0.55, 30, 60), s[5] + 0.8, 0.5, 0.0)
    S(thump_heavy(rng), s[5] + 1.35, 0.7, 0.0)
    S(creak(rng, 0.45, 50, 26), s[5] + 1.85, 0.35, 0.0)
    S(roll(rng, 0.75), s[5] + 2.4, 0.55, 0.3)
    # 7 · uscarea: foi agățate, litere puse la loc în casetă
    for k in range(8):
        S(paper(rng, 0.3), s[6] + 0.12 + k * 0.28 + 0.15, 0.35, -0.7 + 0.2 * k)
    for i in range(9):
        S(click_metal(rng, 0.5), s[6] + 1.0 + i * 0.25 + 0.45, 0.35, -0.3)
    # 8 · legarea: împăturire, caietul pe grămadă, cusut, coperta
    S(swish(rng, 0.4), s[7] + 0.05, 0.4, -0.2)
    S(swish(rng, 0.4), s[7] + 0.5, 0.4, -0.2)
    S(paper(rng, 0.45), s[7] + 0.95, 0.35, 0.1)
    for tt in (1.55, 1.75, 1.95):
        S(thread(rng), s[7] + tt, 0.4, 0.15)
    S(leather_thud(rng), s[7] + 2.5, 0.75, 0.15)
    # carton și Partea a II-a: „ștampila” fiecărei date; clopot la 1544
    S(thump_heavy(rng), TR0 + 0.2, 0.3, 0.0)
    for i, t0 in enumerate(ESTART):
        S(thump_heavy(rng), t0 + 0.22, 0.38, 0.0)
        S(paper(rng, 0.25), t0 + 0.24, 0.2, 0.2)
    add(bel, bell(hz("D5"), rng, 3.5), ESTART[3] + 0.25, gain=0.9, pan=0.1)

    ir = make_ir(t60=1.5, predelay=0.016, seed=1525)
    ir_room = make_ir(t60=0.5, predelay=0.006, seed=1583)
    tab, bel = lp(tab, 9000), lp(bel, 9000)
    stems = [(rec, -20.0, 0.22, ir), (lut, -22.0, 0.18, ir), (vio, -25.0, 0.15, ir), (tab, -29.0, 0.12, ir),
             (bel, -27.0, 0.3, ir), (sfx, -18.0, 0.12, ir_room)]
    mix = None
    for x, target, wet, irx in stems:
        y = match_lufs(hp(x, 30), target)
        if x is sfx:  # tranzitorii foarte scurte (clinchete, ciocănele): le rotunjim vârfurile înainte de mix
            y = limiter(y, ceiling_db=-8.0, look_ms=3.0, release_ms=60.0)
        y = reverb(y, irx, wet=wet)
        mix = y if mix is None else mix + y
    return lp(mix, 13000)


if __name__ == "__main__":
    mix = render()
    out = finalize(mix, OUT, "M24 – temă originală în stil renascentist pentru Istoria tiparului la Sibiu",
                   "Temă originală și sunete de atelier sintetizate în cod (flaut drept, lăută, violă, tobă) – ACTIV AI",
                   target_lufs=-14.0, fin=0.02, fout=2.0, ceiling_db=-2.6, max_tp=-2.0)
    report(out, "M24 final")
