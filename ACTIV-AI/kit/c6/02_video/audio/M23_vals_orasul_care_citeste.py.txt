"""M23 – fundal muzical pentru „Orașul care citește” – cărți care zboară peste acoperișuri (60 s).

Temă originală, compusă și sintetizată în cod pentru videoclipul M23 (artefact-model ACTIV AI),
în stil de vals poetic: harpă (Karplus-Strong), flaut și celestă sintetizate, coarde, bas ciupit.
Nu citează și nu imită o melodie existentă; nu are titlu de piesă reală.

Tempo 90 BPM, măsura de 3/4 = 2 s, Fa major (secțiunea B în re minor). Secțiunile urmăresc imaginea:
  0 s   introducere: harpă în ritm de vals             – titlul, acoperișurile la apus
  6 s   foșnet de aripi-pagini, sclipiri              – cărțile își iau zborul din „ochi”
 12 s   tema A (flaut)                                 – „1525”
 20 s   tema A' (flaut + celestă)                      – „1544”
 28 s   tema B, în re minor                            – „1869”
 36 s   tema B' (coardele cresc)                       – „300.000”
 44 s   tema A, în registru înalt                      – „813.551”
 51 s   glissando de harpă în jos, aterizarea         – cărțile se întorc în „ochi”
 52 s   acord ținut                                    – „Deschide o carte.”
 56 s   coda                                           – cadrul de onestitate
La fiecare formare de cifre: un arpegiu de celestă care urcă.

Totul este sintetizat din formule (Karplus-Strong, sinteză aditivă și modală, zgomot filtrat) – fără eșantioane;
foșnetul „aripilor” (paginilor) este zgomot filtrat, sintetizat, nu o înregistrare.
Folosește biblioteca comună /home/claude/expo/04_audio/_src/audiolib.py.

Rulare: python3 M23_vals_orasul_care_citeste.py  -> M23_vals_orasul_care_citeste.mp3 (în același folder)
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = "/home/claude/expo/04_audio/_src"
if LIB not in sys.path:
    sys.path.insert(0, LIB)

from audiolib import (SR, add, additive, bp, env_adsr, env_ar, env_exp, finalize, hp, hz, ks_pluck, lp,
                      make_ir, match_lufs, modal, ns, report, reverb, rng_of, saw, stereo, t_axis, vibrato)

BPM = 90
BEAT = 60.0 / BPM          # 0,667 s
BAR = 3 * BEAT             # 2,0 s
DUR = 60.0
OUT = os.path.join(HERE, "M23_vals_orasul_care_citeste.mp3")
FORM_T = [12.2, 20.2, 28.2, 36.2, 44.2]   # începutul formațiilor de cifre (din animație)


def b2t(bar, beat=0.0):
    return bar * BAR + beat * BEAT


def ramp(x, ms):
    k = max(2, ns(ms / 1000.0))
    x = x.copy()
    x[:k] *= 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, k))
    return x


def norm(x):
    return x / (np.max(np.abs(x)) + 1e-12)


# ------------------------------------------------------------------ instrumente
def harp(f, rng, t60=1.6, bright=0.55):
    """Harpă: sinteză modală (armonice care se sting tot mai repede) + un „ciupit” scurt de zgomot."""
    ks = np.arange(1, 11)
    freqs = [f * k * (1 + 0.0004 * k * k) for k in ks]
    amps = [(1.0 / k ** 1.25) * (bright + (1 - bright) * np.exp(-(k - 1) / 2.0)) for k in ks]
    t60s = [t60 / (1 + 0.35 * (k - 1)) for k in ks]
    dur = max(1.2, t60 * 1.1)
    x = modal(freqs, amps, t60s, dur, rng=rng, attack=0.003)
    n = len(x)
    x = x + bp(rng.standard_normal(n), min(f * 2, 4000), min(f * 8, 12000)) * env_exp(n, 0.012) * 0.25 * np.max(np.abs(x))
    return ramp(norm(x), 3)


def celesta(f, dur, rng, vel=1.0):
    x = modal([f, 2.0 * f, 3.98 * f, 9.85 * f], [1.0, 0.12, 0.22, 0.05], [2.4, 1.3, 0.7, 0.22], dur, rng=rng,
              attack=0.0015)
    n = len(x)
    x = x + bp(rng.standard_normal(n), 2500, 9000) * env_exp(n, 0.01) * 0.04
    return x * vel


def flute(f, dur, rng):
    n = ns(dur + 0.25)
    tt = t_axis(n)
    fr = f * 2 ** (0.16 * np.clip((tt - 0.22) / 0.3, 0, 1) * np.sin(2 * np.pi * 5.0 * tt + rng.uniform(0, 6)) / 12)
    ph = 2 * np.pi * np.cumsum(fr) / SR
    tone = np.sin(ph) + 0.14 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph)
    breath = bp(rng.standard_normal(n), 1600, 7000) * 0.05
    return lp(tone + breath, 7000) * env_adsr(n, 0.07, 0.15, 0.85, 0.25)


def strings(notes, dur, rng, attack=0.6, cutoff=1700, release=0.8):
    n = ns(dur + release)
    out = np.zeros(n)
    for nm in notes:
        f = hz(nm)
        for det in (-0.003, 0.0, 0.003):
            fv = vibrato(n, f * (1 + det), rate=5.0 + rng.uniform(-.4, .4), depth_semitones=0.06, delay=0.3, rng=rng)
            out += saw(fv, phase0=rng.uniform())
    out = lp(out, cutoff) / (len(notes) * 3) ** 0.5
    return out * env_adsr(n, attack, 0.3, 0.9, release)


def pizz_bass(f, rng):
    x = ks_pluck(f, 1.4, t60=1.0, bright=0.3, pos=0.25, rng=rng)
    n = len(x)
    x = x + 0.5 * np.sin(2 * np.pi * f * t_axis(n)) * env_exp(n, 0.9)
    return ramp(lp(x, 900), 3)


def flap(rng, big=1.0):
    """Un „bătut de aripă” al unei cărți: rafală scurtă de zgomot filtrat (foșnet de hârtie)."""
    d = 0.05 + 0.04 * big
    n = ns(d)
    t = t_axis(n)
    e = (t / 0.008) * np.exp(1 - t / 0.008) * np.exp(-t / (0.02 + 0.02 * big))
    x = bp(rng.standard_normal(n), 700 + rng.uniform() * 600, 3500 + rng.uniform() * 2500) * e
    return norm(x)


# ------------------------------------------------------------------ material muzical
CH = {"F": ["F3", "A3", "C4"], "Dm": ["D3", "F3", "A3"], "Bb": ["Bb2", "D3", "F3"], "C": ["C3", "E3", "G3"],
      "C7": ["C3", "E3", "Bb3"], "Am": ["A2", "C3", "E3"], "Gm": ["G2", "Bb2", "D3"], "Gm7": ["G2", "Bb2", "F3"],
      "A7": ["A2", "C#3", "G3"], "Bbmaj7": ["Bb2", "D3", "A3"]}
ROOT = {"F": "F2", "Dm": "D2", "Bb": "Bb1", "C": "C2", "C7": "C2", "Am": "A1", "Gm": "G1", "Gm7": "G1", "A7": "A1",
        "Bbmaj7": "Bb1"}
PROG = ["F", "Dm", "Bb", "C", "F", "C7",                 # 0–5: introducere, decolare
        "F", "Am", "Bb", "C7", "F", "Dm", "Gm7", "C7",   # 6–13: A, A'
        "Dm", "Bb", "C", "F", "Dm", "Bb", "Gm", "A7",    # 14–21: B, B'
        "F", "Am", "Bb", "C7", "F", "Bbmaj7", "F", "F"]  # 22–29: A înalt, aterizare, coda
assert len(PROG) == 30
MEL = {
    6: [("C5", 1), ("F5", 1), ("A5", 1)], 7: [("G5", 2), ("E5", 1)], 8: [("F5", 1), ("D5", 1), ("Bb5", 1)],
    9: [("A5", 1.5), ("G5", .5), ("E5", 1)],
    10: [("C5", 1), ("F5", 1), ("A5", 1)], 11: [("C6", 2), ("A5", 1)], 12: [("Bb5", 1), ("G5", 1), ("F5", 1)],
    13: [("E5", 2), ("G5", 1)],
    14: [("A5", 1.5), ("G5", .5), ("F5", 1)], 15: [("D5", 2), ("F5", 1)], 16: [("E5", 1), ("G5", 1), ("C6", 1)],
    17: [("A5", 3)],
    18: [("A5", 1.5), ("Bb5", .5), ("A5", 1)], 19: [("F5", 2), ("D5", 1)], 20: [("G5", 1), ("Bb5", 1), ("D6", 1)],
    21: [("C#6", 2), ("E5", 1)],
    22: [("F5", 1), ("A5", 1), ("C6", 1)], 23: [("E6", 2), ("C6", 1)], 24: [("D6", 1), ("Bb5", 1), ("F5", 1)],
    25: [("G5", 1.5), ("A5", .5), ("Bb5", 1)],
    26: [("A5", 3)],
}
for b, ph in MEL.items():
    assert abs(sum(d for _, d in ph) - 3) < 1e-9, b


def render(seed=1544):
    rng = rng_of(seed)
    names = ["harp", "fl", "cel", "str", "bass", "flut", "shim"]
    S = {k: stereo(DUR) for k in names}

    # ---------------- acompaniament de vals: bas pe 1, acord de harpă pe 2 și 3
    for bar, ch in enumerate(PROG):
        t0 = b2t(bar)
        if bar >= 28:   # coda: arpegiu lent
            for i, nm in enumerate(CH[ch] + [hz_oct(CH[ch][0], 1)]):
                add(S["harp"], harp(hz(nm, 12), rng, 2.4), t0 + i * BEAT * 0.5, gain=0.5,
                    pan=-0.3 + 0.2 * i)
            if bar == 28:
                add(S["bass"], pizz_bass(hz(ROOT[ch]), rng), t0, gain=0.8)
            continue
        if bar in (26, 27):   # aterizarea: acorduri ținute, harpă rară
            add(S["bass"], pizz_bass(hz(ROOT[ch]), rng), t0, gain=0.8)
            add(S["harp"], harp(hz(CH[ch][1], 12), rng, 2.0), t0 + BEAT, gain=0.5, pan=0.2)
            continue
        add(S["bass"], pizz_bass(hz(ROOT[ch]), rng), t0, gain=1.0)
        add(S["harp"], harp(hz(ROOT[ch], 12), rng, 1.2, 0.45), t0, gain=0.55, pan=-0.25)
        for beat in (1, 2):
            for k, nm in enumerate(CH[ch]):
                add(S["harp"], harp(hz(nm, 12), rng, 0.9, 0.5), t0 + beat * BEAT + k * 0.012,
                    gain=(0.42 if beat == 1 else 0.34), pan=-0.1 + 0.15 * k)
    # harpă: arpegiu urcător la începutul introducerii
    for i, nm in enumerate(["F3", "A3", "C4", "F4", "A4", "C5", "F5"]):
        add(S["harp"], harp(hz(nm), rng, 2.2, 0.6), 0.25 + i * 0.11, gain=0.35, pan=-0.4 + 0.12 * i)

    # ---------------- melodia
    for bar, ph in MEL.items():
        pos = 0.0
        for nm, d in ph:
            t0 = b2t(bar, pos)
            lg = 0.95 if bar not in (17, 26) else 1.0
            add(S["fl"], flute(hz(nm), d * BEAT * lg, rng), t0 + rng.uniform(-0.004, 0.004),
                gain=(0.9 if bar < 22 else 1.0) * rng.uniform(0.92, 1.0), pan=0.12)
            if 10 <= bar <= 13 or 22 <= bar <= 25:
                add(S["cel"], celesta(hz(nm, 12), 1.8, rng, 0.8), t0, gain=0.4, pan=-0.25)
            pos += d
    # în B' îi răspunde celesta, sus, pe timpul 3
    for bar in (18, 19, 20, 21):
        add(S["cel"], celesta(hz(CH[PROG[bar]][2], 24), 2.0, rng, 0.7), b2t(bar, 2), gain=0.35, pan=0.35)

    # ---------------- coardele
    for bar in range(14, 26):
        ch = PROG[bar]
        lvl = 0.45 + 0.4 * (bar - 14) / 11
        add(S["str"], strings([hz_oct(n, 1) for n in CH[ch]], BAR, rng, attack=0.5, cutoff=1500 + 80 * (bar - 14)),
            b2t(bar), gain=lvl)
    add(S["str"], strings(["F3", "A3", "C4", "G4"], 4.2, rng, attack=1.2, cutoff=1600, release=1.5), b2t(26), gain=0.7)
    add(S["str"], strings(["F3", "A3", "C4"], 3.6, rng, attack=1.0, cutoff=1300, release=1.5), b2t(28), gain=0.45)
    add(S["str"], strings(["F2", "C3", "A3"], 6.0, rng, attack=2.5, cutoff=1100, release=1.0), 0.0, gain=0.4)

    # ---------------- sclipiri: decolarea și formarea cifrelor
    for i, nm in enumerate(["C6", "F6", "A6", "C7", "F7"]):
        add(S["shim"], celesta(hz(nm), 1.8, rng, 0.8), 6.1 + i * 0.09, gain=0.6, pan=-0.5 + 0.25 * i)
    for k, tf in enumerate(FORM_T):
        seq = ["F5", "A5", "C6", "E6", "G6", "A6"] if k != 2 and k != 3 else ["D5", "F5", "A5", "C6", "E6", "F6"]
        for i, nm in enumerate(seq):
            add(S["shim"], celesta(hz(nm), 1.8, rng, 0.85), tf + 1.0 + i * 0.07, gain=0.55, pan=-0.5 + 0.2 * i)
    # aterizarea: glissando de harpă în jos (51–53 s) și „pling”-uri când cărțile intră în „ochi”
    gl = ["F6", "E6", "D6", "C6", "Bb5", "A5", "G5", "F5", "E5", "D5", "C5", "Bb4", "A4", "G4", "F4", "E4", "D4", "C4"]
    for i, nm in enumerate(gl):
        add(S["harp"], harp(hz(nm), rng, 1.2, 0.55), 50.9 + i * 0.09, gain=0.22, pan=0.4 - 0.045 * i)
    for i in range(14):
        add(S["shim"], celesta(hz(["A5", "C6", "F6", "A6"][i % 4]), 1.2, rng, 0.6), 52.0 + i * 0.13 + rng.uniform(0, .05),
            gain=0.35, pan=rng.uniform(-0.6, 0.6))

    # ---------------- foșnetul „aripilor” (densitate după imagine)
    def flutter_rate(t):
        r = 0.0
        r += 90 * np.clip((t - 6.0) / 3.0, 0, 1) * np.clip((53.5 - t) / 1.5, 0, 1)   # stolul în zbor
        for tf in FORM_T:                                                            # formare / risipire
            r += 60 * np.exp(-((t - (tf + 0.6)) / 0.7) ** 2)
        r += 90 * np.exp(-((t - 52.0) / 0.8) ** 2)                                   # aterizarea
        return r

    def flutter_amp(t, tf_list=FORM_T):
        a = 0.35 + 0.65 * np.exp(-((t - 8.5) / 1.8) ** 2)
        for tf in tf_list:
            a += 0.4 * np.exp(-((t - (tf + 0.6)) / 0.7) ** 2)
        a += 0.5 * np.exp(-((t - 52.0) / 0.8) ** 2)
        # în timpul formațiilor (cifre stabile) stolul e mai liniștit
        for tf in tf_list:
            a *= 1 - 0.55 * np.clip((t - (tf + 1.6)) / 0.5, 0, 1) * np.clip(((tf + 6.0) - t) / 0.5, 0, 1)
        return a

    t = 6.0
    while t < 54.5:
        r = flutter_rate(t)
        if r < 1:
            t += 0.05
            continue
        add(S["flut"], flap(rng, rng.uniform(0.3, 1.0)), t, gain=flutter_amp(t) * rng.uniform(0.3, 1.0),
            pan=rng.uniform(-0.8, 0.8))
        t += rng.exponential(1.0 / r)
    # primele cărți care ies din „ochi” – bătăi de aripă mai mari, mai rare
    for i in range(16):
        t0 = 6.0 + i * 0.3 + rng.uniform(0, 0.1)
        for j in range(3):
            add(S["flut"], flap(rng, 1.0), t0 + j * 0.13, gain=1.0, pan=rng.uniform(-0.5, 0.5))

    ir = make_ir(t60=2.4, predelay=0.025, seed=1869)
    S["flut"] = hp(S["flut"], 400)
    for k in ("cel", "shim"):
        S[k] = lp(S[k], 9000)
    stems = [("harp", -20.5, .3), ("fl", -18.5, .3), ("cel", -26.0, .35), ("str", -24.0, .35), ("bass", -24.5, .15),
             ("flut", -31.0, .2), ("shim", -25.5, .4)]
    mix = None
    for k, target, wet in stems:
        x = match_lufs(hp(S[k], 30), target)
        report(x, k)
        y = reverb(x, ir, wet=wet)
        mix = y if mix is None else mix + y
    return lp(mix, 14000)


def hz_oct(nm, k):
    """Nota mutată cu k octave (nume de notă)."""
    return nm[:-1] + str(int(nm[-1]) + k)


if __name__ == "__main__":
    mix = render()
    out = finalize(mix, OUT, "M23 – temă originală în stil de vals pentru „Orașul care citește”",
                   "Temă originală, sintetizată în cod (harpă, flaut, celestă, coarde; foșnet sintetizat) – ACTIV AI",
                   target_lufs=-14.0, fin=0.05, fout=2.0, ceiling_db=-2.6, max_tp=-2.0)
    report(out, "M23 final")
