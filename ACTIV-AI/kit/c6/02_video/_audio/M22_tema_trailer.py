"""M22 – fundal muzical pentru „Trailer AI pentru o piesă de teatru despre Podul Minciunilor” (60 s).

Temă originală, compusă și sintetizată în cod pentru trailerul piesei IMAGINARE „Fontă și adevăr”
(artefact-model ACTIV AI), în stil de muzică de trailer – comedie cu mister: cutie muzicală (celestă),
ostinato de pizzicato, clarinet și fagot sintetizați, alămuri, „lovituri” de trailer, tobe.
Nu citează și nu imită o melodie existentă; nu are titlu de piesă reală.

Tempo 96 BPM, 4/4 (o măsură = 2,5 s), Re minor (finalul – Re major). Secțiunile urmăresc tăieturile:
  0,0 s  cutia muzicală + bâzâit grav                 – cortina închisă
  3,7 s  foșnetul cortinei                           – cortina se deschide
  5,0 s  ostinato de pizzicato + ceas (tic-tac)       – podul, 1859, 1860, inscripțiile
 10,0 s  „clang” de fontă, clarinetul                 – prim-planul inscripțiilor
 15,0 s  cutia muzicală, din nou                     – „Leagă Orașul de Sus…”, „Și are o legendă.”
 20,0 s  tremolo + rafală de tobă care crește         – „Dacă minți pe el…”
 22,5 s  lovitură de trailer + scârțâit de metal      – „…se prăbușește.” (legenda)
 25,0 s  trei ciupituri                               – „Trei personaje fictive…”
 27,5 s  tema personajelor (clarinet, fagot, tubă)    – Ucenica, Negustorul de umbrele, Podul
 42,5 s  două lovituri scurte                         – „Un secret.” „Un pariu.”
 45,0 s  sclipiri de celestă (câte una pe „ochi”)      – „Orașul cu ochi vede tot.”
 47,5 s  tobe care accelerează + scârțâit + pocnet    – „Cine minte… cade?”
 50,0 s  lovitură + tema la alămuri, final în Re major – titlul „Fontă și adevăr”
 55,0 s  cutia muzicală, în Re major                  – cadrul de onestitate

Totul este sintetizat din formule (oscilatoare cu bandă limitată, Karplus-Strong, sinteză modală,
zgomot filtrat) – fără eșantioane. Efectele (cortina, fonta, scârțâitul, pocnetul) sunt sintetizate, nu înregistrări.
Folosește biblioteca comună /home/claude/expo/04_audio/_src/audiolib.py.

Rulare: python3 M22_tema_trailer.py  -> M22_tema_trailer.mp3 (în același folder)
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = "/home/claude/expo/04_audio/_src"
if LIB not in sys.path:
    sys.path.insert(0, LIB)

from audiolib import (SR, add, additive, bp, env_adsr, env_ar, env_exp, finalize, hp, hz, kick, ks_pluck,
                      lp, make_ir, match_lufs, modal, ns, peaking, report, reverb, rng_of, saw, stereo,
                      t_axis, vibrato)

BPM = 96
BEAT = 60.0 / BPM          # 0,625 s
BAR = 4 * BEAT             # 2,5 s
DUR = 60.0
OUT = os.path.join(HERE, "M22_tema_trailer.mp3")


def b2t(bar, beat=0.0):
    return bar * BAR + beat * BEAT


def ramp(x, ms):
    """Atac rotunjit de câteva milisecunde (fără vârfuri la recodarea AAC)."""
    k = max(2, ns(ms / 1000.0))
    x = x.copy()
    x[:k] *= 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, k))
    return x


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-12)


# ------------------------------------------------------------------ instrumente
def celesta(f, dur, rng, vel=1.0):
    x = modal([f, 2.0 * f, 3.98 * f, 9.85 * f], [1.0, 0.12, 0.22, 0.05], [2.4, 1.3, 0.7, 0.22], dur, rng=rng,
              attack=0.0015)
    n = len(x)
    x = x + bp(rng.standard_normal(n), 2500, 9000) * env_exp(n, 0.01) * 0.04
    return x * vel


def pizz(f, rng, t60=0.45, bright=0.45):
    """Pizzicato: sinteză modală (armonice care se sting repede) + un ciupit scurt de zgomot."""
    ks = np.arange(1, 9)
    freqs = [f * k * (1 + 0.0003 * k * k) for k in ks]
    amps = [(1.0 / k ** 1.3) * (bright + (1 - bright) * np.exp(-(k - 1) / 1.5)) for k in ks]
    t60s = [t60 / (1 + 0.5 * (k - 1)) for k in ks]
    x = modal(freqs, amps, t60s, max(0.6, t60 * 1.5), rng=rng, attack=0.003)
    n = len(x)
    x = x + bp(rng.standard_normal(n), min(f * 2, 3000), min(f * 10, 9000)) * env_exp(n, 0.01) * 0.2 * np.max(np.abs(x))
    return ramp(norm(x), 3)


def clarinet(f, dur, rng):
    n = ns(dur + 0.1)
    fr = vibrato(n, f, rate=5.2, depth_semitones=0.08, delay=0.25, rng=rng)
    x = additive(fr, [1.0, 0.05, 0.55, 0.04, 0.3, 0.03, 0.15, 0.02, 0.07])
    x = x + bp(rng.standard_normal(n), 1500, 5000) * 0.015
    return lp(x, 3400) * env_adsr(n, 0.04, 0.1, 0.85, 0.08)


def bassoon(f, dur, rng):
    n = ns(dur + 0.1)
    fr = vibrato(n, f, rate=5.0, depth_semitones=0.06, delay=0.3, rng=rng)
    x = 0.7 * saw(fr) + 0.3 * additive(fr, [1.0, 0.6, 0.3])
    x = peaking(lp(x, 1500), 480, 6.0, 1.2)
    return x * env_adsr(n, 0.05, 0.1, 0.85, 0.08)


def brass(f, dur, rng, bright=1.0):
    n = ns(dur + 0.12)
    t = t_axis(n)
    scoop = 2 ** ((-0.35 * np.exp(-t / 0.03)) / 12)
    vib = 2 ** ((0.07 * np.clip((t - 0.3) / 0.3, 0, 1) * np.sin(2 * np.pi * 5.2 * t + rng.uniform(0, 6))) / 12)
    fr = f * scoop * vib
    x = 0.5 * saw(fr * 2 ** (0.05 / 12)) + 0.5 * saw(fr * 2 ** (-0.05 / 12), phase0=0.37)
    eb = (1 - np.exp(-t / 0.035)) * (0.55 + 0.45 * np.exp(-t / 0.25))
    y = lp(x, 600) * (1 - eb) + lp(x, 600 + 3200 * bright) * eb
    return y * env_adsr(n, 0.025, 0.12, 0.8, 0.12)


def tuba(f, dur, rng):
    n = ns(dur + 0.1)
    t = t_axis(n)
    x = 0.6 * lp(saw(np.full(n, f), phase0=rng.uniform()), 520) + 0.7 * np.sin(2 * np.pi * f * t)
    return x * env_adsr(n, 0.03, 0.1, 0.75, 0.1)


def strings(notes, dur, rng, attack=0.5, cutoff=1800, trem=0.0, release=0.6):
    n = ns(dur + release)
    t = t_axis(n)
    out = np.zeros(n)
    for nm in notes:
        f = hz(nm)
        for det in (-0.003, 0.0, 0.003):
            fv = vibrato(n, f * (1 + det), rate=5.0 + rng.uniform(-.4, .4), depth_semitones=0.07, delay=0.3, rng=rng)
            out += saw(fv, phase0=rng.uniform())
    out = lp(out, cutoff) / (len(notes) * 3) ** 0.5
    env = env_adsr(n, attack, 0.3, 0.9, release)
    if trem > 0:
        env = env * (0.62 + 0.38 * np.sin(2 * np.pi * trem * t))
    return out * env


def boom(rng, f_hi=110, f_lo=36, dur=1.6, t60=1.1):
    x = kick(dur=dur, f_hi=f_hi, f_lo=f_lo, pitch_tau=0.06, t60=t60, click=0.05, rng=rng)
    n = len(x)
    x = x + 0.4 * lp(rng.standard_normal(n), 140) * env_ar(n, 0.002, 0.35)
    return ramp(norm(x), 1.5)


def tom(f, rng):
    return ramp(norm(kick(dur=0.6, f_hi=f * 1.7, f_lo=f, pitch_tau=0.03, t60=0.38, click=0.06, rng=rng)), 1)


def woodblock(rng, f=1100.0):
    x = modal([f, f * 2.71, f * 4.2], [1.0, 0.3, 0.1], [0.09, 0.05, 0.03], 0.16, rng=rng, attack=0.0015)
    return ramp(norm(x), 1.5)


def snare(rng, vel=1.0, dur=0.3):
    n = ns(dur)
    body = modal([185, 330, 460], [1.0, 0.5, 0.25], [0.09, 0.06, 0.04], dur, rng=rng, attack=0.0005)
    nz = bp(rng.standard_normal(n), 1800, 8000) * env_ar(n, 0.002, 0.2)
    return vel * norm(0.6 * body + 0.9 * nz)


def cymbal(rng, dur=2.2):
    n = ns(dur)
    nz = hp(rng.standard_normal(n), 4200) * env_ar(n, 0.002, dur * 0.8)
    metal = modal([3150, 4370, 5230, 6810, 7940, 9120], [1, .8, .7, .6, .5, .4],
                  [1.2, 1.0, .9, .8, .7, .6], dur, rng=rng, beat_hz=3)
    return norm(0.8 * norm(nz) + 0.25 * norm(metal))


def clang(rng, f=196.0, dur=2.8):
    """Lovitură în fontă (sinteză modală, parțiale inarmonice) – efect sintetizat."""
    x = modal([f, f * 2.38, f * 4.27, f * 6.33, f * 9.1, f * 12.4], [1, .75, .55, .4, .25, .12],
              [2.2, 1.7, 1.2, .8, .5, .3], dur, rng=rng, attack=0.001, beat_hz=1.3)
    return ramp(norm(x), 1)


def creak(rng, dur=1.8, r0=16.0, r1=48.0):
    """Scârțâit de metal: impulsuri de tip „lipire–alunecare” care excită rezonanțe joase (sintetizat)."""
    n = ns(dur)
    out = np.zeros(n)
    res = modal([170, 395, 720, 1130, 1610], [1, .7, .5, .3, .18], [.07, .06, .05, .04, .03], 0.14, rng=rng,
                attack=0.0004)
    t = 0.0
    while t < dur - 0.15:
        u = t / dur
        rate = r0 + (r1 - r0) * u
        amp = np.sin(np.pi * min(1.0, u * 1.25)) * rng.uniform(0.4, 1.0)
        k = ns(t)
        seg = res * amp * (1 + 0.3 * rng.uniform(-1, 1))
        out[k:k + len(seg)] += seg[:n - k]
        t += (1.0 / rate) * rng.uniform(0.6, 1.4)
    return norm(lp(out, 2600))


def riser(rng, dur, f0=250.0, f1=6000.0, up=True):
    """Zgomot filtrat cu bandă care urcă (sau coboară): filtrare pe bucăți suprapuse."""
    n = ns(dur)
    nz = rng.standard_normal(n + ns(0.2))
    out = np.zeros(n)
    hop = ns(0.04)
    win = np.hanning(2 * hop)
    for s in range(0, n, hop):
        u = s / n
        fc = f0 * (f1 / f0) ** (u if up else 1 - u)
        seg = bp(nz[s:s + 2 * hop + ns(0.05)], fc * 0.7, min(fc * 1.4, 18000))[ns(0.05):ns(0.05) + 2 * hop]
        e = min(len(seg), n - s, 2 * hop)
        out[s:s + e] += seg[:e] * win[:e]
    env = np.linspace(0, 1, n) ** 2 if up else np.linspace(1, 0, n) ** 1.5
    return norm(out * env)


def snap(rng):
    n = ns(1.2)
    t = t_axis(n)
    burst = hp(rng.standard_normal(n), 1500) * np.exp(-t / 0.012)
    ring = modal([2400, 3710, 5150, 6900], [1, .7, .5, .3], [.5, .35, .25, .15], 1.2, rng=rng, attack=0.0003)
    return ramp(norm(0.8 * norm(burst) + 0.35 * norm(ring)), 0.5)


def debris(rng, dur=1.6, density=90):
    """Firimituri care cad (granule scurte de zgomot), tot mai rare."""
    n = ns(dur)
    out = np.zeros(n)
    k = int(density * dur)
    for _ in range(k):
        t0 = (rng.uniform() ** 1.8) * (dur - 0.05)
        g = ns(0.004 + rng.uniform() * 0.01)
        s = ns(t0)
        grain = bp(rng.standard_normal(g + 64), 1200 + rng.uniform() * 3000, 7000)[64:] * np.hanning(g)
        out[s:s + g] += grain * rng.uniform(0.2, 1.0) * (1 - t0 / dur)
    return norm(out)


# ------------------------------------------------------------------ material muzical
MB = ["A5", "D6", "F6", "E6", "D6", "C#6", "D6", "A5", "Bb5", "D6", "G6", "F6", "E6", "C#6", "A5", None]
MB_MAJ = ["A5", "D6", "F#6", "E6", "D6", "C#6", "D6", "A5"]
OST = [["D3", "A3", "F3", "A3"] * 2, ["Bb2", "F3", "D3", "F3"] * 2, ["G2", "D3", "Bb2", "D3"] * 2,
       ["A2", "E3", "C#3", "E3"] * 2]
OST_ROOT = ["D2", "Bb1", "G1", "A1"]
OST_CH = [["D3", "F3", "A3"], ["D3", "F3", "Bb3"], ["D3", "G3", "Bb3"], ["C#3", "E3", "A3"]]
CLAR_A = [(None, .5), ("D5", .5), ("F5", .5), ("G5", .5), ("A5", 1), ("Bb5", .5), ("A5", .5)]
CLAR_B = [("G5", .75), ("F5", .25), ("E5", .5), ("C#5", .5), ("E5", 1.5), (None, .5)]
# tema personajelor (2 măsuri)
TA = [("D5", .5), ("E5", .5), ("F5", .5), ("G#5", .5), ("A5", 1), ("F5", .5), ("D5", .5)]
TB = [("Bb5", .75), ("A5", .25), ("G5", .5), ("F5", .5), ("E5", 1), ("C#5", .5), ("A4", .5)]
TB_END = [("Bb5", .75), ("A5", .25), ("G5", .5), ("E5", .5), ("F#5", 2)]
WALK_A = ["D2", "F2", "A2", "G#2"]
WALK_B = ["G2", "Bb2", "A2", "A1"]
for ph in (CLAR_A, CLAR_B, TA, TB, TB_END):
    assert abs(sum(d for _, d in ph) - 4) < 1e-9


def render(seed=1859):
    rng = rng_of(seed)
    names = ["box", "pizz", "bass", "lead", "brass", "str", "perc", "boom", "cym", "fx", "tick"]
    S = {k: stereo(DUR) for k in names}

    def phrase(buf, ph, t0, inst, gain, pan=0.0, transpose=0, legato=0.92):
        pos = 0.0
        for nm, d in ph:
            if nm is not None:
                x = inst(hz(nm, transpose), d * BEAT * legato, rng)
                add(buf, x, t0 + pos * BEAT + rng.uniform(-0.003, 0.003), gain=gain * rng.uniform(0.9, 1.0), pan=pan)
            pos += d

    def box(seq, t0, step, gain, transpose=0):
        for i, nm in enumerate(seq):
            if nm is None:
                continue
            add(S["box"], celesta(hz(nm, transpose), 2.2, rng, 1.0 if i % 2 == 0 else 0.8), t0 + i * step,
                gain=gain, pan=rng.uniform(-0.3, 0.3))

    def ticks(t0, t1, gain=1.0):
        k = 0
        for t in np.arange(t0, t1 - 1e-6, BEAT):
            add(S["tick"], woodblock(rng, 1250 if k % 2 == 0 else 880), t, gain=gain * (1.0 if k % 2 == 0 else 0.8),
                pan=0.35 if k % 2 == 0 else -0.35)
            k += 1

    def roll(t0, t1, g0, g1, step=0.045):
        for t in np.arange(t0, t1, step):
            u = (t - t0) / max(1e-6, t1 - t0)
            add(S["perc"], snare(rng, 1.0, 0.18), t, gain=g0 + (g1 - g0) * u, pan=-0.1)

    def braam(t0, notes, dur=2.3, gain=1.0):
        for k, nm in enumerate(notes):
            add(S["brass"], brass(hz(nm), dur, rng, 0.9), t0, gain=gain / len(notes) ** 0.5, pan=(k - 1.5) * 0.15)
        add(S["boom"], boom(rng), t0, gain=1.0)
        add(S["cym"], cymbal(rng, 2.6), t0, gain=0.8, pan=0.2)

    # ---------------- 0–5 s: cutia muzicală, bâzâit grav, cortina
    box(MB, 0.35, BEAT / 2, 0.9)
    add(S["str"], strings(["D2", "A2"], 4.6, rng, attack=1.8, cutoff=900), 0.0, gain=0.8)
    add(S["fx"], riser(rng, 1.0, 400, 5000, up=True), 3.6, gain=0.55, pan=-0.3)
    add(S["fx"], riser(rng, 0.8, 5000, 500, up=False), 4.6, gain=0.45, pan=0.3)
    roll(3.9, 4.98, 0.05, 0.6)

    # ---------------- 5–15 s: ostinato, ceas, lovituri
    for k in range(4):
        bar = 2 + k
        for i, nm in enumerate(OST[k]):
            add(S["pizz"], pizz(hz(nm), rng), b2t(bar, i * 0.5), gain=1.0 if i % 2 == 0 else 0.75, pan=-0.2)
        for beat in (0, 2):
            add(S["bass"], pizz(hz(OST_ROOT[k]), rng, t60=0.9, bright=0.3), b2t(bar, beat), gain=1.0)
        add(S["str"], strings(OST_CH[k], BAR, rng, attack=0.6, cutoff=1500), b2t(bar), gain=0.55)
    ticks(5.0, 15.0, 0.55)
    phrase(S["lead"], CLAR_A, b2t(4), clarinet, 1.0, 0.15)
    phrase(S["lead"], CLAR_B, b2t(5), clarinet, 1.0, 0.15)
    add(S["boom"], boom(rng), 5.0, gain=1.0)
    add(S["cym"], cymbal(rng, 1.8), 5.0, gain=0.4)
    add(S["boom"], boom(rng, dur=1.0), 7.5, gain=0.55)
    add(S["fx"], clang(rng, 196), 10.0, gain=0.9, pan=0.1)
    add(S["boom"], boom(rng), 10.0, gain=0.8)
    add(S["boom"], boom(rng, dur=1.0), 12.5, gain=0.55)

    # ---------------- 15–20 s: cutia muzicală, din nou
    add(S["str"], strings(["D2", "A2", "D3"], 5.0, rng, attack=0.8, cutoff=1000), 15.0, gain=0.8)
    add(S["str"], strings(["F3", "A3"], 2.5, rng, attack=0.6, cutoff=1400), 15.0, gain=0.45)
    add(S["str"], strings(["F3", "Bb3"], 2.5, rng, attack=0.6, cutoff=1400), 17.5, gain=0.45)
    box(MB[:8], 15.2, BEAT / 2, 0.7)
    box(MB[8:15], 17.7, BEAT / 2, 0.7)
    ticks(15.0, 20.0, 0.35)
    add(S["boom"], boom(rng), 15.0, gain=0.8)
    add(S["boom"], boom(rng), 17.5, gain=0.9)

    # ---------------- 20–22,5 s: tensiune
    add(S["str"], strings(["A3", "Bb3", "D4"], 2.5, rng, attack=2.0, cutoff=2600, trem=12.0, release=0.1), 20.0,
        gain=0.9)
    roll(20.6, 22.45, 0.08, 0.9)
    rc = cymbal(rng, 1.6)[::-1].copy()
    add(S["cym"], rc * np.linspace(0, 1, len(rc)) ** 2, 22.5 - 1.6, gain=0.6)
    add(S["fx"], riser(rng, 2.4, 200, 4000), 20.1, gain=0.5)
    for t0 in (20.0, 21.25):
        add(S["boom"], boom(rng, f_hi=80, f_lo=40, dur=0.5, t60=0.3), t0, gain=0.5)
        add(S["boom"], boom(rng, f_hi=80, f_lo=40, dur=0.5, t60=0.3), t0 + 0.22, gain=0.35)

    # ---------------- 22,5 s: lovitura „…se prăbușește.”
    braam(22.5, ["D2", "A2", "D3", "F3"], 2.4, 1.2)
    add(S["fx"], creak(rng, 1.9), 22.7, gain=0.75, pan=-0.15)
    add(S["fx"], debris(rng, 1.8), 22.6, gain=0.4, pan=0.2)

    # ---------------- 25–27,5 s: trei ciupituri
    ticks(25.0, 27.5, 0.4)
    for t0, nm in ((25.1, "A3"), (25.75, "C4"), (26.4, "E4")):
        add(S["pizz"], pizz(hz(nm), rng, t60=0.6), t0, gain=1.1, pan=0.1)
        add(S["bass"], pizz(hz(nm, -24), rng, t60=0.7, bright=0.3), t0, gain=0.6)
    add(S["pizz"], pizz(hz("A2"), rng, t60=0.5), b2t(10, 3.5), gain=0.9)

    # ---------------- 27,5–42,5 s: tema personajelor
    def theme_bed(bar, k, lvl=1.0, chords=True):
        walk = WALK_A if k % 2 == 0 else WALK_B
        for i, nm in enumerate(walk):
            add(S["bass"], pizz(hz(nm), rng, t60=0.8, bright=0.35), b2t(bar, i), gain=lvl)
        if chords:
            chs = [["D3", "F3", "A3"], ["D3", "F3", "A3"]] if k % 2 == 0 else [["D3", "G3", "Bb3"], ["C#3", "E3", "G3"]]
            for j, beat in enumerate((1, 3)):
                for nm in chs[j]:
                    add(S["pizz"], pizz(hz(nm), rng, t60=0.3), b2t(bar, beat), gain=0.5 * lvl, pan=-0.25)
        for e in range(8):  # mături (hi-hat moale)
            n = ns(0.09)
            hh = hp(rng.standard_normal(n), 6000) * env_ar(n, 0.002, 0.06)
            add(S["perc"], ramp(hh, 1), b2t(bar, e * 0.5), gain=0.12 * (1.0 if e % 2 == 0 else 0.6) * lvl, pan=0.3)

    # Ucenica: clarinet + celestă
    for k in range(2):
        theme_bed(11 + k, k)
    phrase(S["lead"], TA, b2t(11), clarinet, 1.0, 0.1)
    phrase(S["lead"], TB, b2t(12), clarinet, 1.0, 0.1)
    phrase(S["box"], TA, b2t(11), lambda f, d, r: celesta(f, 1.5, r), 0.35, -0.2, transpose=12)
    phrase(S["box"], TB, b2t(12), lambda f, d, r: celesta(f, 1.5, r), 0.35, -0.2, transpose=12)
    # Negustorul: fagot (o octavă mai jos)
    for k in range(2):
        theme_bed(13 + k, k)
    phrase(S["lead"], TA, b2t(13), bassoon, 1.0, -0.1, transpose=-12)
    phrase(S["lead"], TB, b2t(14), bassoon, 1.0, -0.1, transpose=-12)
    add(S["pizz"], pizz(hz("D5"), rng, t60=0.5), b2t(14, 3.5), gain=0.6, pan=0.4)
    # Podul: tubă/alămuri grave, rezonanță de fontă, sclipiri pentru „ochi”
    for k in range(2):
        theme_bed(15 + k, k, 0.8, chords=False)
    phrase(S["brass"], TA, b2t(15), lambda f, d, r: tuba(f, d, r), 1.0, 0.0, transpose=-24)
    phrase(S["brass"], TB, b2t(16), lambda f, d, r: tuba(f, d, r), 1.0, 0.0, transpose=-24)
    add(S["str"], strings(["D3", "F3", "A3"], 2.5, rng, attack=0.5, cutoff=1300), b2t(15), gain=0.55)
    add(S["str"], strings(["D3", "G3", "Bb3"], 1.25, rng, attack=0.3, cutoff=1300), b2t(16), gain=0.55)
    add(S["str"], strings(["C#3", "E3", "A3"], 1.25, rng, attack=0.3, cutoff=1300), b2t(16, 2), gain=0.55)
    add(S["fx"], clang(rng, 98, 3.0), 37.6, gain=0.5)
    for i, nm in enumerate(["D6", "F6", "A6", "D7"]):
        add(S["box"], celesta(hz(nm), 2.0, rng), 38.0 + i * 0.07, gain=0.6, pan=-0.4 + 0.25 * i)
    for i, nm in enumerate(["A6", "D6"]):
        add(S["box"], celesta(hz(nm), 1.5, rng), 40.42 + i * 0.12, gain=0.5, pan=0.2)

    # ---------------- 42,5–45 s: „Un secret.” „Un pariu.”
    for t0, ch in ((42.5, ["D3", "F3", "A3", "D4"]), (43.75, ["E3", "G3", "Bb3", "C#4"])):
        for k, nm in enumerate(ch):
            add(S["brass"], brass(hz(nm), 0.45, rng, 1.0), t0, gain=0.8, pan=(k - 1.5) * 0.2)
        add(S["boom"], boom(rng, dur=1.2), t0, gain=0.9)
        cy = cymbal(rng, 0.9)
        add(S["cym"], cy * np.exp(-t_axis(len(cy)) / 0.18), t0, gain=0.7)
    ticks(42.5, 45.0, 0.45)

    # ---------------- 45–47,5 s: „ochii” se deschid
    add(S["str"], strings(["D3", "A3", "E4", "F4"], 2.5, rng, attack=1.5, cutoff=2400, release=0.3), 45.0, gain=0.8)
    pings = ["D5", "E5", "F5", "A5", "D6", "E6", "F6", "A6", "C7", "D7", "E7", "F7", "A7", "D6", "A6"]
    for j, nm in enumerate(pings):
        add(S["box"], celesta(hz(nm), 1.6, rng, 0.9), 45.15 + j * 0.085, gain=0.55, pan=-0.6 + 0.085 * j)

    # ---------------- 47,5–50 s: construcție, scârțâit, pocnet, liniște
    for i in range(4):   # optimi
        add(S["perc"], tom(110 if i % 2 == 0 else 82, rng), 47.5 + i * BEAT / 2, gain=0.55 + 0.04 * i, pan=0.15)
    for i in range(5):   # șaisprezecimi
        add(S["perc"], tom(130 if i % 2 == 0 else 95, rng), 48.75 + i * BEAT / 4, gain=0.72 + 0.04 * i, pan=-0.15)
    for k, nm in enumerate(["A3", "Bb3", "B3", "C4"]):
        add(S["str"], strings([nm, hz_name_up(nm)], BEAT, rng, attack=0.05, cutoff=3000, trem=14.0, release=0.05),
            47.5 + k * BEAT, gain=0.7 + 0.1 * k)
    add(S["fx"], riser(rng, 2.05, 300, 9000), 47.5, gain=0.6)
    add(S["fx"], creak(rng, 1.0, 25, 60), 48.4, gain=0.6, pan=0.2)
    add(S["fx"], snap(rng), 49.55, gain=1.0)
    add(S["boom"], boom(rng, dur=0.8, t60=0.4), 49.55, gain=0.7)

    # ---------------- 50–55 s: titlul – lovitură + tema la alămuri, final în Re major
    braam(50.0, ["D2", "A2", "D3", "F3"], 1.6, 1.1)
    phrase(S["brass"], TA, b2t(20), lambda f, d, r: brass(f, d, r, 0.9), 0.9, 0.05, transpose=-12)
    phrase(S["brass"], TB_END, b2t(21), lambda f, d, r: brass(f, d, r, 0.9), 0.9, 0.05, transpose=-12)
    add(S["str"], strings(["D3", "F3", "A3", "D4"], 2.5, rng, attack=0.2, cutoff=2200), b2t(20), gain=0.7)
    add(S["str"], strings(["D3", "G3", "Bb3"], 1.25, rng, attack=0.15, cutoff=2200), b2t(21), gain=0.7)
    add(S["str"], strings(["D3", "F#3", "A3", "D4"], 2.2, rng, attack=0.15, cutoff=2400, release=0.8), b2t(21, 2), gain=0.75)
    for i, nm in enumerate(WALK_A):
        add(S["bass"], pizz(hz(nm), rng, t60=0.8, bright=0.35), b2t(20, i), gain=1.0)
    add(S["bass"], pizz(hz("G1"), rng, t60=0.9, bright=0.3), b2t(21), gain=1.0)
    add(S["bass"], pizz(hz("D2"), rng, t60=1.4, bright=0.3), b2t(21, 2), gain=1.0)
    roll(b2t(21, 1), b2t(21, 2) - 0.03, 0.1, 0.7)
    add(S["boom"], boom(rng), b2t(21, 2), gain=0.9)
    add(S["cym"], cymbal(rng, 2.4), b2t(21, 2), gain=0.6)

    # ---------------- 55–60 s: cutia muzicală în Re major
    box(MB_MAJ, 55.2, BEAT / 2, 0.75)
    for i, nm in enumerate(["D6", "F#6", "A6"]):
        add(S["box"], celesta(hz(nm), 3.0, rng, 0.9), 57.8 + i * 0.05, gain=0.6)
    add(S["str"], strings(["D3", "F#3", "A3"], 4.2, rng, attack=1.0, cutoff=1200), 55.4, gain=0.5)

    ir = make_ir(t60=1.9, predelay=0.02, seed=1860)
    ir_big = make_ir(t60=2.8, predelay=0.03, seed=1859)
    for k in ("cym", "box", "tick"):
        S[k] = lp(S[k], 9500)
    stems = [("box", -21.0, ir, .35), ("pizz", -22.0, ir, .2), ("bass", -22.5, ir, .1), ("lead", -20.0, ir, .25),
             ("brass", -19.5, ir_big, .25), ("str", -23.5, ir_big, .3), ("perc", -24.0, ir, .15),
             ("boom", -22.5, ir_big, .2), ("cym", -29.0, ir_big, .25), ("fx", -24.0, ir_big, .25),
             ("tick", -29.0, ir, .15)]
    mix = None
    for k, target, irx, wet in stems:
        x = match_lufs(hp(S[k], 28), target)
        report(x, k)
        y = reverb(x, irx, wet=wet)
        mix = y if mix is None else mix + y
    return lp(mix, 14000)


def hz_name_up(nm):
    """Nota cu o terță mică mai sus (pentru tremolo-ul care urcă)."""
    order = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    name, octv = nm[:-1], int(nm[-1])
    i = order.index(name) + 3
    return order[i % 12] + str(octv + i // 12)


if __name__ == "__main__":
    mix = render()
    out = finalize(mix, OUT, "M22 – temă originală în stil de trailer (comedie cu mister) pentru „Fontă și adevăr”",
                   "Temă originală, sintetizată în cod; piesa de teatru e imaginară – ACTIV AI",
                   target_lufs=-14.0, fin=0.02, fout=2.0, ceiling_db=-3.8, max_tp=-3.2)  # rezervă pentru recodarea AAC din MP4
    report(out, "M22 final")
