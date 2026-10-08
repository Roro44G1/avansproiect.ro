"""A21 – Uvertură AI pentru un oraș: „Piață, pagină, cortină” (compoziție instrumentală în 3 mișcări, ~3:30).

Temă originală în stil de uvertură de concert (ordinea repede – lent – repede, ca în uvertura
italiană): melodiile, armoniile și orchestrația au fost compuse pentru expoziția ACTIV AI și nu
citează nicio lucrare existentă. „Orchestra” este SINTETIZATĂ în cod (oscilatoare, sinteză aditivă și
modală, coarde ciupite Karplus-Strong, zgomot filtrat, reverberație de sală sintetică) – nu este o
înregistrare a unei orchestre reale și nu folosește mostre.

Mișcările (titluri inventate pentru această piesă):
  I.   „Piața se trezește”        – Allegro, Re major, 4/4, 144 de pătrimi pe minut, 40 de măsuri
  II.  „Pagini în lumina lămpii”  – Andante, Si bemol major, 3/4, 72 de pătrimi pe minut, 26 de măsuri
  III. „Cortina se ridică”        – Maestoso (76) – Allegro (132), Re major, 4/4, 4 + 28 de măsuri
Între mișcări: liniște (pauză de circa 1,6 s după stingerea ultimului acord).

„Motivul orașului” (șase note: treptele 5–1–2–3–6–5 ale gamei) leagă cele trei mișcări:
la corni în introducerea mișcării I, la clarinet în coda mișcării a II-a, la alămuri în
Maestoso-ul mișcării a III-a și în final.

Notație în cod: fiecare șir = o măsură; token = „notă:durată în pătrimi” („R” = pauză).
Acordurile: un acord pe măsură („D”) sau mai multe, împărțite egal („G:2 A7:2” = câte doi timpi).

Instrumente (toate aproximate prin sinteză): viori I (linie legato cu glisări mici și vibrato, 3–4
voci ușor dezacordate), viori II/viole (acorduri susținute, tremolo, acorduri scurte), violoncele și
contrabași (arcuș și pizzicato), flaut și clarinet (sinteză aditivă cu suflu), corni, trompete,
tromboni și tubă (dinți de fierăstrău filtrați), timpane (sinteză modală, acordate pe Re și La –
tonica și dominanta), harpă (Karplus-Strong), glockenspiel și celestă (sinteză modală), tobă mică,
tobă mare, talgere.

Folosește biblioteca comună /home/claude/expo/04_audio/_src/audiolib.py.
Rulare:  python3 A21_uvertura_pentru_un_oras.py             -> ../A21_uvertura_pentru_un_oras.mp3 + A21_marcaje.json
         python3 A21_uvertura_pentru_un_oras.py --marcaje   -> doar A21_marcaje.json (fără sinteză)
         python3 A21_uvertura_pentru_un_oras.py --notatie   -> tabelele cu temele, pentru fișa .md
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/claude/expo/04_audio/_src")

from audiolib import (SR, add, additive, bp, env_adsr, env_ar, env_exp, finalize, hp, kick,  # noqa: E402
                      ks_pluck, lp, make_ir, match_lufs, mhz, midi, modal, ns, peaking, report,
                      reverb, rng_of, saw, stereo, t_axis)

OUT = os.path.join(HERE, "..", "A21_uvertura_pentru_un_oras.mp3")
LEAD_IN = 0.3       # liniște la început (s)
GAP = 1.6           # liniște între mișcări, după stingerea fiecărei mișcări (s)

# ================================================================== teorie: acorduri, voci
PCS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
QUAL = {"": (0, 4, 7), "m": (0, 3, 7), "7": (0, 4, 7, 10), "m7": (0, 3, 7, 10)}


def _pc(s):
    r = PCS[s[0]]
    k = 1
    if len(s) > 1 and s[1] in "#b":
        r += 1 if s[1] == "#" else -1
        k = 2
    return r % 12, s[k:]


def chord_info(name):
    """'F#7' -> ([6, 10, 1, 4], 6): clasele de înălțime și basul."""
    main, _, bass = name.partition("/")
    r, q = _pc(main)
    pcs = [(r + i) % 12 for i in QUAL[q]]
    b = _pc(bass)[0] if bass else r
    return pcs, b


def voicing(name, lo, hi, maxn=4):
    """Notele acordului din registrul [lo, hi] (MIDI), cel mult maxn, alese uniform."""
    pcs, _ = chord_info(name)
    notes = [m for m in range(lo, hi + 1) if m % 12 in pcs]
    if len(notes) > maxn:
        idx = np.round(np.linspace(0, len(notes) - 1, maxn)).astype(int)
        notes = [notes[i] for i in idx]
    return notes


def root_in(name, lo):
    _, b = chord_info(name)
    m = lo
    while m % 12 != b:
        m += 1
    return m


def third_of(name):
    pcs, _ = chord_info(name)
    return (pcs[1] - pcs[0]) % 12


def nearest_tone(name, target, lo, hi):
    pcs, _ = chord_info(name)
    cands = [m for m in range(lo, hi + 1) if m % 12 in pcs]
    return min(cands, key=lambda m: abs(m - target))


# ================================================================== timp, notație
class TempoMap:
    """Hartă de tempo: segs = [(măsura de început, pătrimi pe minut), ...]."""

    def __init__(self, bpb, segs):
        self.bpb = bpb
        self.segs = segs

    def t(self, bar, beat=0.0):
        B = bar * self.bpb + beat
        t = 0.0
        for k, (b0, bpm) in enumerate(self.segs):
            s0 = b0 * self.bpb
            s1 = self.segs[k + 1][0] * self.bpb if k + 1 < len(self.segs) else np.inf
            if B <= s0:
                break
            t += (min(B, s1) - s0) * 60.0 / bpm
        return t

    def beat_s(self, bar):
        bpm = [b for b0, b in self.segs if b0 <= bar][-1]
        return 60.0 / bpm


def parse_bar(s, bpb):
    out = []
    for tok in s.split():
        nm, d = tok.split(":")
        out.append((None if nm == "R" else midi(nm), float(d)))
    tot = sum(d for _, d in out)
    assert abs(tot - bpb) < 1e-9, f"măsura „{s}” are {tot} timpi, nu {bpb}"
    return out


def mel(bars, bar0, tm, transpose=0, vel=1.0):
    """Evenimentele unei melodii: (t0, durată_s, nota MIDI sau None, intensitate)."""
    ev = []
    for k, s in enumerate(bars):
        pos = 0.0
        for m, d in parse_bar(s, tm.bpb):
            t0, t1 = tm.t(bar0 + k, pos), tm.t(bar0 + k, pos + d)
            ev.append((t0, t1 - t0, None if m is None else m + transpose, vel))
            pos += d
    return ev


def chords(chs, bar0, tm):
    ev = []
    for k, s in enumerate(chs):
        toks = s.split()
        if all(":" not in x for x in toks):
            items = [(x, tm.bpb / len(toks)) for x in toks]
        else:
            items = [(x.split(":")[0], float(x.split(":")[1])) for x in toks]
        assert abs(sum(d for _, d in items) - tm.bpb) < 1e-9, f"acordurile „{s}” nu acoperă măsura"
        pos = 0.0
        for nm, d in items:
            t0, t1 = tm.t(bar0 + k, pos), tm.t(bar0 + k, pos + d)
            ev.append(dict(t=t0, d=t1 - t0, name=nm, bar=bar0 + k, beat=pos, beats=d))
            pos += d
    return ev


def chord_at(chev, t):
    cur = chev[0]["name"]
    for c in chev:
        if c["t"] <= t + 1e-6:
            cur = c["name"]
    return cur


# ================================================================== instrumente
class Stems:
    def __init__(self, total):
        self.total = total
        self.b = {}

    def buf(self, k):
        if k not in self.b:
            self.b[k] = stereo(self.total)
        return self.b[k]

    def add(self, k, sig, t0, gain=1.0, pan=0.0):
        add(self.buf(k), sig, t0, gain=gain, pan=pan)


def line_arrays(evs, n, attack=0.04, release=0.09, port=0.025, frac=0.92, toff=0.0, det=1.0, hold_last=0.0):
    """Frecvența și amplitudinea unei linii melodice continue (legato când notele se ating)."""
    f = np.zeros(n)
    a = np.zeros(n)
    since = np.full(n, 10.0)
    notes = [e for e in evs if e[2] is not None]
    for i, (t0, d, m, v) in enumerate(notes):
        t0 += toff
        fn = mhz(m) * det
        nxt = notes[i + 1] if i + 1 < len(notes) else None
        conn_next = nxt is not None and abs(nxt[0] + toff - (t0 + d)) < 0.02
        prev = notes[i - 1] if i else None
        conn_prev = prev is not None and abs(prev[0] + prev[1] - (t0 - toff)) < 0.02
        L = d if conn_next else d * frac
        if nxt is None:
            L += hold_last
        i0, i1 = max(0, ns(t0)), min(n, ns(t0 + L))
        if i1 <= i0:
            continue
        seg = np.full(i1 - i0, fn)
        if conn_prev:
            g = min(len(seg), ns(port))
            seg[:g] = np.geomspace(mhz(prev[2]) * det, fn, g)
        f[i0:i1] = seg
        since[i0:i1] = t_axis(i1 - i0)
        env = np.full(i1 - i0, v)
        k = min(len(env), ns(attack))
        env[:k] *= np.linspace(0.7 if conn_prev else 0.0, 1.0, k)
        a[i0:i1] = env
        if not conn_next:
            r = ns(release + (0.5 if nxt is None else 0.0))
            j1 = min(n, i1 + r)
            a[i1:j1] = v * np.linspace(1, 0, j1 - i1)
            f[i1:j1] = fn
            since[i1:j1] = t_axis(j1 - i1) + (i1 - i0) / SR
    nz = np.nonzero(f)[0]
    if len(nz):
        idx = np.maximum.accumulate(np.where(f > 0, np.arange(n), 0))
        f = f[idx]
        f[: nz[0]] = f[nz[0]]
    else:
        f[:] = 440.0
    w = max(3, ns(0.006))
    a = np.convolve(a, np.ones(w) / w, mode="same")
    return f, a, since


def vib_curve(f, since, rng, depth, rate, delay=0.18):
    n = len(f)
    t = t_axis(n)
    dep = depth * np.clip((since - delay) / 0.3, 0, 1)
    r = rate * (1 + 0.04 * np.sin(2 * np.pi * 0.23 * t + rng.uniform(0, 6)))
    ph = 2 * np.pi * np.cumsum(r) / SR + rng.uniform(0, 6.28)
    return f * 2 ** (dep * np.sin(ph) / 12)


def bowed_line(evs, total, rng, voices=3, vib=0.18, bright=0.6, pan=0.0, spread=0.3, hold_last=0.0):
    """Secție de coarde cu arcușul (viori): voci ușor dezacordate și decalate, panoramate în evantai."""
    n = ns(total)
    out = stereo(total)
    for v in range(voices):
        det = 2 ** (rng.uniform(-7, 7) / 1200)
        toff = 0.0 if v == 0 else rng.uniform(-0.012, 0.012)
        f, a, since = line_arrays(evs, n, attack=0.05, release=0.12, toff=toff, det=det, hold_last=hold_last)
        f = vib_curve(f, since, rng, vib * rng.uniform(0.8, 1.2), rng.uniform(5.3, 6.3))
        x = lp(saw(f, phase0=rng.uniform()), 2600 + 4200 * bright, order=2)
        bow = bp(rng.standard_normal(n), 2500, 7500) * 0.025
        p = pan + spread * ((v / max(1, voices - 1)) - 0.5)
        add(out, (x + bow) * a / voices, 0.0, pan=p)
    return out


def wind_line(evs, total, rng, kind="flute", pan=0.0, hold_last=0.0, vel=1.0):
    """Flaut sau clarinet: sinteză aditivă pe o linie continuă, cu suflu și vibrato."""
    n = ns(total)
    if kind == "flute":
        harm, vib, rate, breath, lpf, att = [1.0, 0.32, 0.12, 0.06, 0.03], 0.11, 5.2, 0.05, 9000, 0.045
    else:  # clarinet: armonice impare dominante
        harm, vib, rate, breath, lpf, att = [1.0, 0.04, 0.48, 0.05, 0.26, 0.04, 0.12, 0.02, 0.05], 0.05, 5.0, 0.02, 5000, 0.035
    f, a, since = line_arrays(evs, n, attack=att, release=0.07, hold_last=hold_last)
    f = vib_curve(f, since, rng, vib, rate, delay=0.25)
    x = additive(f, harm, phase0=rng.uniform())
    nz = bp(rng.standard_normal(n), 1800, 8000) * breath
    chiff = np.zeros(n)
    x = lp(x + nz, lpf, order=2) * a
    return stereo_pan(x * vel + chiff, pan)


def stereo_pan(x, pan):
    a = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    return np.vstack([x * np.cos(a), x * np.sin(a)])


def string_note(f, dur, rng, attack=0.08, release=0.25, bright=0.5, voices=3, trem=0.0, vib=0.1):
    """Notă de coarde (secție): dinți de fierăstrău dezacordați, vibrato, opțional tremolo."""
    L = dur + release
    n = ns(L)
    t = t_axis(n)
    out = np.zeros(n)
    ramp = np.clip((t - 0.15) / 0.4, 0, 1)
    for v in range(voices):
        det = rng.uniform(-9, 9) / 1200
        fv = f * 2 ** (det + vib / 12 * ramp * np.sin(2 * np.pi * rng.uniform(5.0, 6.2) * t + rng.uniform(0, 6.28)))
        x = saw(fv, phase0=rng.uniform())
        if trem > 0:
            tr = rng.uniform(12.5, 14.5)
            x *= 1 - trem * (0.5 - 0.5 * np.cos(2 * np.pi * tr * t + rng.uniform(0, 6.28)))
        out += x
    out /= voices
    fc = min(2000 + 4500 * bright, 18 * f + 1500)
    return lp(out, fc, order=2) * env_adsr(n, attack, 0.12, 0.88, release)


def body_eq(x, high=True):
    """Rezonanțele „cutiei” instrumentelor cu coarde (aproximare)."""
    y = peaking(x, 290, 4.0, 1.6)
    y = peaking(y, 1100, 2.0, 1.2)
    y = peaking(y, 2800, 3.5, 1.3)
    return hp(y, 150 if high else 35, order=2)


def brass(f, dur, rng, bright=1.0, scoop=0.3):
    """Alamă: doi dinți de fierăstrău dezacordați, „scoop” la atac, strălucire care se deschide."""
    n = ns(dur + 0.14)
    t = t_axis(n)
    sc = 2 ** ((-scoop * np.exp(-t / 0.03)) / 12)
    vb = 2 ** ((0.06 * np.clip((t - 0.35) / 0.3, 0, 1) * np.sin(2 * np.pi * 5.0 * t + rng.uniform(0, 6))) / 12)
    fr = f * sc * vb
    x = 0.5 * saw(fr * 2 ** (0.05 / 12), phase0=rng.uniform()) + 0.5 * saw(fr * 2 ** (-0.05 / 12), phase0=rng.uniform())
    eb = (1 - np.exp(-t / 0.04)) * (0.6 + 0.4 * np.exp(-t / 0.3))
    y = lp(x, 500 + f, order=2) * (1 - eb) + lp(x, 600 + f + 3800 * bright, order=2) * eb
    return y * env_adsr(n, 0.03, 0.15, 0.8, 0.12)


def pizz(f, rng, dur=0.9):
    x = ks_pluck(f, dur, t60=0.55 if f < 150 else 0.4, bright=0.28, pos=0.22, rng=rng)
    x = lp(x, 2500)
    x[-ns(0.05):] *= np.linspace(1, 0, ns(0.05))
    return x


def harp(m, rng, dur=2.4, bright=0.36):
    f = mhz(m)
    x = ks_pluck(f, dur, t60=3.0 if f < 200 else (2.0 if f < 600 else 1.2), bright=bright, pos=0.27, rng=rng)
    x[-ns(0.08):] *= np.linspace(1, 0, ns(0.08))
    return x


def timpani(f, rng, vel=1.0, dur=3.0, ring=1.0):
    ratios = [0.62, 1.0, 1.50, 1.98, 2.44, 2.90, 3.36]
    amps = [0.35, 1.0, 0.5, 0.35, 0.18, 0.1, 0.05]
    t60s = [0.25 * ring, 2.4 * ring, 1.5 * ring, 1.1 * ring, 0.7 * ring, 0.5 * ring, 0.35 * ring]
    x = modal([f * r for r in ratios], amps, t60s, dur, rng=rng, attack=0.0015)
    n = len(x)
    t = t_axis(n)
    th = lp(rng.standard_normal(n), 220 + 500 * vel) * np.exp(-t / 0.016)
    x = x / (np.max(np.abs(x)) + 1e-12) + 0.35 * th / (np.max(np.abs(th)) + 1e-12)
    x = lp(x, 700 + 2600 * vel, order=2)
    x[-ns(0.1):] *= np.linspace(1, 0, ns(0.1))
    return vel * x / (np.max(np.abs(x)) + 1e-12)


TIMP = {"D": midi("D3"), "A": midi("A2"), "Bb": midi("Bb2"), "F": midi("F3")}


def timp_hit(st, note, t, rng, vel=1.0):
    st.add("timp", timpani(mhz(TIMP[note]), rng, vel), t, gain=vel)


def timp_roll(st, note, t0, t1, g0, g1, rng, rate=16.0):
    t, k = t0, 0
    f = mhz(TIMP[note])
    while t < t1:
        u = (t - t0) / max(1e-6, t1 - t0)
        g = g0 + (g1 - g0) * u
        x = timpani(f, rng, vel=0.35 + 0.5 * g, dur=0.9, ring=0.55)
        st.add("timp", x, t + rng.uniform(-0.004, 0.004), gain=0.42 * g * (0.85 if k % 2 else 1.0),
               pan=0.06 if k % 2 else -0.06)
        t += rng.uniform(0.93, 1.07) / rate
        k += 1


def cymbal(rng, dur=2.6):
    n = ns(dur)
    nz = hp(rng.standard_normal(n), 4200) * env_ar(n, 0.002, dur * 0.8)
    metal = modal([3150, 4370, 5230, 6810, 7940, 9120], [1, .8, .7, .6, .5, .4],
                  [1.2, 1.0, .9, .8, .7, .6], dur, rng=rng, beat_hz=3)
    y = 0.8 * nz / (np.max(np.abs(nz)) + 1e-12) + 0.25 * metal / (np.max(np.abs(metal)) + 1e-12)
    y[-ns(0.15):] *= np.linspace(1, 0, ns(0.15))
    return lp(y, 11000) / (np.max(np.abs(y)) + 1e-12)


def cymbal_swell(rng, dur):
    n = ns(dur)
    t = t_axis(n)
    nz = hp(rng.standard_normal(n), 3500)
    metal = modal([3150, 4370, 5230, 6810], [1, .8, .7, .6], [9, 9, 9, 9], dur, rng=rng, beat_hz=4)
    y = (0.8 * nz / np.max(np.abs(nz)) + 0.3 * metal / (np.max(np.abs(metal)) + 1e-12)) * (t / dur) ** 2.2
    y[-ns(0.03):] *= np.linspace(1, 0, ns(0.03))
    return lp(y, 10000)


def snare(rng, vel=1.0, dur=0.28):
    n = ns(dur)
    body = modal([185, 330, 460], [1.0, 0.5, 0.25], [0.09, 0.06, 0.04], dur, rng=rng, attack=0.0005)
    nz = bp(rng.standard_normal(n), 1800, 8000) * env_ar(n, 0.002, 0.18)
    y = 0.6 * body + 0.9 * nz
    return lp(vel * y / (np.max(np.abs(y)) + 1e-12), 9000)


def bass_drum(rng):
    x = kick(dur=0.9, f_hi=90, f_lo=48, pitch_tau=0.05, t60=0.75, click=0.03, rng=rng)
    n = len(x)
    x = x + 0.3 * lp(rng.standard_normal(n), 160) * env_ar(n, 0.003, 0.3)
    x[-ns(0.05):] *= np.linspace(1, 0, ns(0.05))
    return x / (np.max(np.abs(x)) + 1e-12)


def glock(m, rng, dur=1.6):
    f = mhz(m)
    x = modal([f, 2.76 * f, 5.40 * f, 8.93 * f], [1, 0.3, 0.1, 0.04], [1.4, 0.5, 0.18, 0.08], dur, rng=rng,
              attack=0.0005)
    x[-ns(0.05):] *= np.linspace(1, 0, ns(0.05))
    return lp(x, 9000) / (np.max(np.abs(x)) + 1e-12)


def celesta(m, rng, dur=2.4):
    f = mhz(m)
    ring = 2.4 * (440.0 / f) ** 0.3
    x = modal([f, f * 2.005, f * 3.0, f * 5.4], [1.0, 0.13, 0.05, 0.025], [ring, ring * 0.4, ring * 0.2, 0.25],
              dur, rng=rng, attack=0.0025)
    x[-ns(0.1):] *= np.linspace(1, 0, ns(0.1))
    return x / (np.max(np.abs(x)) + 1e-12)


# ---------------------------------------------------------------- ajutoare de orchestrație
def pad_chords(st, key, chev, lo, hi, rng, gain=1.0, maxn=4, attack=0.1, release=0.3, bright=0.45, trem=0.0,
               pan=0.0, spread=0.5, gain_fn=None, voices=3, vib=0.1):
    for c in chev:
        notes = voicing(c["name"], lo, hi, maxn)
        g = gain * (gain_fn(c) if gain_fn else 1.0)
        for j, m in enumerate(notes):
            p = pan + spread * ((j / max(1, len(notes) - 1)) - 0.5)
            st.add(key, string_note(mhz(m), c["d"], rng, attack, release, bright, voices, trem, vib), c["t"],
                   gain=g / len(notes) ** 0.5, pan=p)


def low_strings(st, chev, rng, lo=38, gain=1.0, attack=0.12, octave=True, key="low"):
    for c in chev:
        r = root_in(c["name"], lo)
        st.add(key, string_note(mhz(r), c["d"], rng, attack, 0.3, 0.35, 3, 0.0, 0.06), c["t"], gain=gain, pan=0.4)
        if octave:
            st.add(key, string_note(mhz(r + 12), c["d"], rng, attack, 0.3, 0.4, 3, 0.0, 0.1), c["t"],
                   gain=0.6 * gain, pan=0.3)


def brass_line(st, key, evs, rng, bright=1.0, gain=1.0, pan=0.0, legato=0.9, scoop=0.3):
    for t0, d, m, v in evs:
        if m is not None:
            st.add(key, brass(mhz(m), d * legato, rng, bright, scoop), t0 + rng.uniform(-0.003, 0.003),
                   gain=gain * v * rng.uniform(0.92, 1.0), pan=pan)


def brass_chord(st, key, notes, t0, dur, rng, bright=0.6, gain=1.0, pan=0.0, spread=0.3):
    for j, m in enumerate(notes):
        p = pan + spread * ((j / max(1, len(notes) - 1)) - 0.5)
        st.add(key, brass(mhz(m), dur, rng, bright, scoop=0.15), t0 + rng.uniform(-0.004, 0.004),
               gain=gain / len(notes) ** 0.5, pan=p)


def harp_gliss(st, lo, hi, scale_pcs, t0, dur, rng, gain=1.0, key="harp"):
    notes = [m for m in range(lo, hi + 1) if m % 12 in scale_pcs]
    for k, m in enumerate(notes):
        st.add(key, harp(m, rng, 1.6, 0.42), t0 + dur * k / len(notes), gain=gain * (0.6 + 0.4 * k / len(notes)),
               pan=-0.6 + 0.5 * k / len(notes))


def harp_roll(st, notes, t0, rng, gain=1.0, step=0.055, dur=3.0):
    for k, m in enumerate(notes):
        st.add("harp", harp(m, rng, dur), t0 + k * step, gain=gain, pan=-0.6 + 0.07 * k)


D_MAJOR = [2, 4, 6, 7, 9, 11, 1]

# ================================================================== partitura – mișcarea I
MOTTO = ["A4:1 D5:1.5 E5:.5 F#5:1", "B5:1 A5:3"]                      # treptele 5–1–2–3 | 6–5 în Re
INTRO_ANS = ["D5:1 G5:1.5 A5:.5 B5:1", "C#6:1 A5:1 G5:1 E5:1"]
CH_INTRO = ["D", "G:1 D:3", "G", "A7"]
THEME_A = [
    "A4:.5 D5:.5 F#5:.5 E5:.5 D5:1 A5:1",
    "G5:.5 F#5:.5 E5:.5 F#5:.5 D5:2",
    "B4:.5 D5:.5 G5:.5 F#5:.5 E5:1 B5:1",
    "A5:.75 G5:.25 F#5:.5 G5:.5 A5:2",
    "A4:.5 D5:.5 F#5:.5 E5:.5 D5:1 B5:1",
    "A5:.5 G5:.5 F#5:.5 G5:.5 A5:1 D6:1",
    "B5:.5 A5:.5 G5:.5 F#5:.5 E5:1 C#6:1",
    "D6:1 A5:.5 F#5:.5 D5:1 R:1",
]
CH_A = ["D", "A7:2 D:2", "G", "A", "D:2 Bm:2", "D", "G:2 A7:2", "D"]
EPISODE_B = [
    "F#4:.5 B4:.5 C#5:.5 D5:.5 C#5:1 B4:1",
    "A4:.5 B4:.5 C#5:.5 A4:.5 F#4:2",
    "G4:.5 B4:.5 D5:.5 E5:.5 F#5:1 E5:1",
    "D5:.5 C#5:.5 B4:.5 A#4:.5 B4:2",
    "F#5:.5 B5:.5 C#6:.5 D6:.5 C#6:1 B5:1",
    "E5:.5 F#5:.5 G5:.5 E5:.5 C#5:2",
    "D5:.5 E5:.5 F#5:.5 G5:.5 A5:1 G5:.5 F#5:.5",
    "E5:1 C#5:1 A4:1 R:1",
]
CH_B = ["Bm", "F#m", "G:2 D:2", "F#7:2 Bm:2", "Bm", "A7", "D", "A7"]
CODA_I = ["A4:1 D5:1.5 E5:.5 F#5:1", "B5:1 A5:3", "D6:.5 B5:.5 G5:1 A5:.5 C#6:.5 E6:1", "D6:.5 R:1.5 D6:2"]
CH_CODA_I = ["D", "G:1 D:3", "G:2 A7:2", "D"]
SECS_I = [("Introducere: motivul orașului la corni", 0, 4), ("Tema A (viori)", 4, 8),
          ("Tema A, cu flaut și alămuri", 12, 8), ("Episod în si minor (clarinet, apoi flaut)", 20, 8),
          ("Revenirea temei A, tutti", 28, 8), ("Coda: motivul orașului la trompete", 36, 4)]

# ================================================================== partitura – mișcarea a II-a
THEME_II = [
    "F4:1.5 G4:.5 Bb4:1",
    "D5:2 C5:1",
    "Bb4:1 A4:.5 G4:.5 Eb4:1",
    "C5:2 A4:1",
    "F4:1.5 G4:.5 Bb4:1",
    "F5:2 D5:1",
    "Eb5:1 D5:.5 C5:.5 A4:1",
    "Bb4:3",
]
CH_II = ["Bb", "Gm", "Eb", "F", "Bb", "Dm", "Cm:2 F7:1", "Bb"]
MID_II = ["D5:1 G5:1.5 F5:.5", "Eb5:1 Bb5:1.5 G5:.5", "F5:1 C6:1.5 A5:.5", "Bb5:2 A5:1"]
CH_MID_II = ["Gm", "Eb", "F7", "Bb:2 F7:1"]
CODA_II = ["F4:1 Bb4:1.5 C5:.5", "D5:1 G5:1 F5:1", "Eb5:1 G5:1 A5:1", "Bb5:3"]   # motivul în Si bemol, 3/4
CH_CODA_II = ["Bb", "Gm7", "Eb:2 F7:1", "Bb"]
SECS_II = [("Introducere: harpa", 0, 2), ("Tema lirică (clarinet)", 2, 8), ("Mijloc (flaut, corni)", 10, 4),
           ("Tema, la viori", 14, 8), ("Coda: motivul orașului, încet", 22, 4)]

# ================================================================== partitura – mișcarea a III-a
MOTTO_LOW = ["A3:1 D4:1.5 E4:.5 F#4:1", "B4:1 A4:3"]
CH_MAEST = ["D", "D", "G:1 D:3", "A7"]
THEME_C = [
    "D5:1.5 A4:.5 D5:1 F#5:1",
    "E5:.75 F#5:.25 G5:1 E5:1 C#5:1",
    "D5:1.5 F#5:.5 A5:1 D6:1",
    "B5:1.5 A5:.5 A5:2",
    "G5:1.5 B5:.5 A5:1 F#5:1",
    "E5:1 A5:1 G5:1 E5:1",
    "F#5:.5 G5:.5 A5:1 G5:.5 E5:.5 C#5:1",
    "D5:2 R:2",
]
CH_C = ["D", "A7", "D", "G:2 D:2", "Em:2 D:2", "A7", "D:2 A7:2", "D"]
BRIDGE_VLN = ["F#5:1 B5:1.5 C#6:1.5", "R:4", "B4:1 E5:1.5 F#5:1.5", "E5:1 A5:1 C#6:1 E6:1"]
BRIDGE_HRN = ["R:4", "D4:1 G4:1.5 A4:1.5", "R:4", "R:4"]
CH_BRIDGE = ["Bm:2.5 F#m:1.5", "G:2.5 D:1.5", "Em:2.5 Bm:1.5", "A7"]
FINAL_III = ["A4:1 D5:1.5 E5:.5 F#5:1", "B5:1 A5:3", "G5:.5 B5:.5 D6:1 C#6:.5 E6:.5 A6:1", "D6:4"]
CH_FINAL_III = ["D", "G:1 D:3", "G:2 A7:2", "D"]
SECS_III = [("Maestoso: motivul orașului la alămuri, glissando de harpă", 0, 4),
            ("Allegro: tema festivă (trompete și viori)", 4, 8), ("Tema festivă, tutti", 12, 8),
            ("Punte: motivul trece din voce în voce", 20, 4), ("Tema A din mișcarea I, la alămuri", 24, 4),
            ("Final", 28, 4)]

MOVEMENTS = [
    dict(nr="I", titlu="Piața se trezește", indicatie="Allegro", tonalitate="Re major", masura="4/4",
         tempo="144 de pătrimi pe minut", masuri=40),
    dict(nr="II", titlu="Pagini în lumina lămpii", indicatie="Andante", tonalitate="Si bemol major",
         masura="3/4", tempo="72 de pătrimi pe minut", masuri=26),
    dict(nr="III", titlu="Cortina se ridică", indicatie="Maestoso – Allegro", tonalitate="Re major",
         masura="4/4", tempo="76, apoi 132 de pătrimi pe minut", masuri=32),
]
LAYOUT = [  # (hartă de tempo, număr de măsuri, coada după ultima măsură în s, secțiuni)
    (TempoMap(4, [(0, 144)]), 40, 2.8, SECS_I),
    (TempoMap(3, [(0, 72)]), 26, 3.8, SECS_II),
    (TempoMap(4, [(0, 76), (4, 132)]), 32, 4.6, SECS_III),
]


# ================================================================== randare – mișcarea I
def render_I(seed=1774):
    rng = rng_of(seed)
    tm, nb, ring, _ = LAYOUT[0]
    beat = tm.beat_s(0)
    end = tm.t(nb)
    total = end + ring
    st = Stems(total)
    chev = chords(CH_INTRO + CH_A + CH_A + CH_B + CH_A + CH_CODA_I, 0, tm)
    sec = lambda b0, b1: [c for c in chev if b0 <= c["bar"] < b1]  # noqa: E731

    vln = mel(THEME_A, 4, tm) + mel(THEME_A, 12, tm) + mel(THEME_A, 28, tm) + mel(CODA_I[2:], 38, tm)
    fl = mel(INTRO_ANS, 2, tm) + mel(THEME_A, 12, tm, vel=0.8) + mel(EPISODE_B[4:], 24, tm) + \
        mel(THEME_A, 28, tm) + mel(CODA_I[2:], 38, tm)
    cl = mel(INTRO_ANS, 2, tm, transpose=-12) + mel(EPISODE_B[:4], 20, tm)

    # ---- introducere (1–4): tremolo de coarde, motivul la corni, răspunsul suflătorilor
    pad_chords(st, "pad", sec(0, 4), 57, 74, rng, gain=1.0, trem=0.65, attack=0.25,
               gain_fn=lambda c: 0.45 + 0.18 * c["bar"])
    low_strings(st, sec(0, 4), rng, gain=0.9, attack=0.3)
    brass_line(st, "horns", mel(MOTTO, 0, tm, transpose=-12), rng, bright=0.35, gain=1.0, pan=-0.3, legato=0.95)
    brass_line(st, "horns", mel(MOTTO, 0, tm, transpose=-24), rng, bright=0.3, gain=0.45, pan=-0.2, legato=0.95)
    timp_hit(st, "D", tm.t(0, 0), rng, 0.9)
    timp_hit(st, "A", tm.t(0, 2), rng, 0.55)
    timp_hit(st, "D", tm.t(1, 1), rng, 0.75)
    timp_roll(st, "A", tm.t(3, 1), tm.t(4, 0), 0.15, 0.75, rng)
    for k, nm in enumerate(["G2", "D3", "G3", "B3", "D4", "G4", "B4"]):
        st.add("harp", harp(midi(nm), rng), tm.t(2, 0) + 0.05 * k, gain=0.9, pan=-0.6 + 0.06 * k)

    # ---- tema A (5–12): viorile, acorduri scurte pe contratimp, pizzicato pe timpi
    for c in sec(4, 12):
        for b in np.arange(c["beat"], c["beat"] + c["beats"]):
            t = tm.t(c["bar"], b)
            if b % 2 == 1:
                for j, m in enumerate(voicing(c["name"], 55, 69, 3)):
                    st.add("pad", string_note(mhz(m), 0.16, rng, 0.012, 0.09, 0.45, 2), t, gain=0.55,
                           pan=-0.1 + 0.15 * j)
            else:
                r = root_in(c["name"], 38)
                m = r if b % 4 == 0 else r + 7
                st.add("pizz", pizz(mhz(m), rng), t, gain=1.0, pan=0.35)
                st.add("pizz", pizz(mhz(m + 12), rng), t + 0.008, gain=0.6, pan=0.2)
        for m in voicing(c["name"], 53, 64, 2):
            st.add("horns", brass(mhz(m), c["d"] * 0.95, rng, 0.15, 0.0), c["t"], gain=0.28, pan=-0.3)
        if c["beat"] == 0 and c["name"][0] in "DA":
            timp_hit(st, c["name"][0], c["t"], rng, 0.45)

    # ---- tema A cu flaut (13–20) și revenirea tutti (29–36)
    def tutti_A(b0, full):
        for c in sec(b0, b0 + 8):
            pad_chords(st, "pad", [c], 55, 72, rng, gain=0.8 if full else 0.65, attack=0.06, release=0.2)
            for b in np.arange(c["beat"], c["beat"] + c["beats"]):
                t = tm.t(c["bar"], b)
                r = root_in(c["name"], 38)
                if b % 2 == 0:
                    m = r if b % 4 == 0 else r + 7
                    st.add("low", string_note(mhz(m), 0.8 * beat, rng, 0.02, 0.12, 0.4, 3), t, gain=1.0, pan=0.4)
                    st.add("low", string_note(mhz(m + 12), 0.8 * beat, rng, 0.02, 0.12, 0.45, 3), t, gain=0.5,
                           pan=0.3)
                    if c["name"][0] in "DA":
                        timp_hit(st, "D" if (c["name"][0] == "D") == (b % 4 == 0) else "A", t, rng,
                                 0.7 if full else 0.5)
                else:
                    brass_chord(st, "horns", voicing(c["name"], 55, 67, 3), t, 0.4 * beat, rng, 0.45,
                                gain=0.8 if full else 0.6, pan=-0.3, spread=0.2)
        for t0, d, m, v in mel(THEME_A, b0, tm):
            if m is not None and d >= 0.99 * beat:
                st.add("glock", glock(m + 12, rng), t0, gain=0.7 if full else 0.5, pan=0.4)

    tutti_A(12, False)
    st.add("cym", cymbal(rng), tm.t(12), gain=0.45, pan=0.25)
    tutti_A(28, True)
    brass_line(st, "tpt", mel(THEME_A[:4], 28, tm), rng, bright=0.9, gain=0.85, pan=0.2, legato=0.85)
    st.add("cym", cymbal(rng), tm.t(28), gain=0.9, pan=0.25)
    st.add("cym", cymbal(rng), tm.t(32), gain=0.5, pan=0.25)

    # ---- episod în si minor (21–28): pizzicato în arpegii, coarde moi
    for c in sec(20, 28):
        tones = voicing(c["name"], 50, 69, 4)
        order = [0, 1, 2, 3, 2, 1, 0, 1]
        for k in range(int(c["beats"] * 2)):
            b = c["beat"] + k * 0.5
            st.add("pizz", pizz(mhz(tones[order[int(b * 2) % 8]]), rng, 0.7), tm.t(c["bar"], b),
                   gain=0.8 if k % 2 == 0 else 0.5, pan=0.1)
    low_strings(st, sec(20, 27), rng, gain=0.55, attack=0.25, octave=False)
    pad_chords(st, "pad", sec(20, 27), 55, 66, rng, gain=0.4, maxn=2, attack=0.3, release=0.3, bright=0.3)
    pad_chords(st, "pad", sec(27, 28), 57, 74, rng, gain=0.8, trem=0.7, attack=0.8)
    low_strings(st, sec(27, 28), rng, gain=0.8, attack=0.4)
    timp_roll(st, "A", tm.t(27, 2), tm.t(28, 0), 0.2, 0.8, rng)

    # ---- coda (37–40)
    brass_line(st, "tpt", mel(CODA_I[:2], 36, tm), rng, bright=1.0, gain=1.0, pan=0.2, legato=0.92)
    brass_line(st, "horns", mel(CODA_I[:2], 36, tm, transpose=-12), rng, bright=0.5, gain=0.8, pan=-0.3,
               legato=0.92)
    pad_chords(st, "pad", sec(36, 39), 57, 76, rng, gain=1.0, trem=0.6, attack=0.05, maxn=5)
    low_strings(st, sec(36, 39), rng, gain=1.0, attack=0.05)
    timp_hit(st, "D", tm.t(36), rng, 0.95)
    timp_hit(st, "D", tm.t(37, 1), rng, 0.8)
    timp_roll(st, "A", tm.t(38, 2), tm.t(39, 0), 0.3, 0.95, rng)
    st.add("cym", cymbal(rng), tm.t(36), gain=0.7, pan=0.25)
    # măsura 40: „ta – taaa”
    for b, L, g in ((0, 0.35, 0.85), (2, 1.7, 1.0)):
        t = tm.t(39, b)
        brass_chord(st, "tpt", [midi("D5"), midi("F#5"), midi("A5")], t, L, rng, 0.9, gain=1.1 * g, pan=0.2)
        brass_chord(st, "horns", [midi("A3"), midi("D4"), midi("F#4"), midi("A4")], t, L, rng, 0.5, gain=g, pan=-0.3)
        for j, m in enumerate(voicing("D", 50, 78, 6)):
            st.add("pad", string_note(mhz(m), L, rng, 0.015, 0.35, 0.6), t, gain=0.5 * g, pan=-0.3 + 0.12 * j)
        st.add("low", string_note(mhz(midi("D2")), L, rng, 0.015, 0.35, 0.4), t, gain=g, pan=0.4)
        st.add("low", string_note(mhz(midi("D3")), L, rng, 0.015, 0.35, 0.45), t, gain=0.6 * g, pan=0.3)
        timp_hit(st, "D", t, rng, g)
        st.add("cym", cymbal(rng), t, gain=0.8 * g, pan=0.25)
    harp_roll(st, [midi(x) for x in ("D2", "A2", "D3", "F#3", "A3", "D4", "F#4")], tm.t(39, 2), rng, gain=0.8)
    for k, nm in enumerate(["D6", "F#6", "A6", "D7"]):
        st.add("glock", glock(midi(nm), rng), tm.t(39, 2) + 0.07 * k, gain=0.6, pan=0.4)

    # ---- liniile melodice
    st.add("vln", bowed_line(vln, total, rng, voices=3, vib=0.17, bright=0.65, pan=-0.35, hold_last=0.5), 0.0)
    st.add("winds", wind_line(fl, total, rng, "flute", pan=-0.08, hold_last=0.5), 0.0)
    st.add("winds", wind_line(cl, total, rng, "clarinet", pan=0.12, vel=0.9), 0.0)

    targets = {"vln": (-17.5, 0.2), "pad": (-22.5, 0.28), "low": (-22.0, 0.15), "pizz": (-24.0, 0.2),
               "winds": (-20.5, 0.25), "horns": (-23.0, 0.3), "tpt": (-21.0, 0.22), "timp": (-23.5, 0.3),
               "cym": (-30.0, 0.25), "harp": (-25.0, 0.3), "glock": (-28.0, 0.3)}
    secs = [dict(name=nm, bar0=b0, t=round(tm.t(b0), 3)) for nm, b0, nb in SECS_I]
    return st, targets, secs, end, total


# ================================================================== randare – mișcarea a II-a
def render_II(seed=1869):
    rng = rng_of(seed)
    tm, nb, ring, _ = LAYOUT[1]
    end = tm.t(nb)
    total = end + ring
    st = Stems(total)
    chev = chords(["Bb", "Gm"] + CH_II + CH_MID_II + CH_II + CH_CODA_II, 0, tm)
    sec = lambda b0, b1: [c for c in chev if b0 <= c["bar"] < b1]  # noqa: E731

    cl = mel(THEME_II, 2, tm) + mel(CODA_II[:2], 22, tm, vel=0.9)
    fl = mel(MID_II, 10, tm) + mel(CODA_II[2:], 24, tm, vel=0.85)
    vln = mel(THEME_II, 14, tm, transpose=12)

    # harpa: arpegii legănate pe optimi (bas, cvintă, octavă, terță, octavă, cvintă)
    for bar in range(0, 22):
        for k in range(6):
            t = tm.t(bar, k * 0.5)
            name = chord_at(chev, t)
            r = root_in(name, 34)
            pat = [r, r + 7, r + 12, r + 12 + third_of(name), r + 12, r + 7]
            g = [1.0, 0.55, 0.7, 0.6, 0.7, 0.55][k]
            lvl = 0.55 if 14 <= bar < 22 else (0.85 if bar < 2 else 0.75)
            st.add("harp", harp(pat[k], rng, 2.2), t, gain=lvl * g, pan=-0.55 + 0.05 * k)
    for bar, nm in ((22, "Bb"), (23, "Gm7"), (24, "Eb")):
        r = root_in(nm, 34)
        notes = [r, r + 7, r + 12] + [m for m in voicing(nm, r + 13, r + 26, 3)]
        harp_roll(st, notes, tm.t(bar), rng, gain=0.7, step=0.07)
    harp_roll(st, [midi(x) for x in ("Bb1", "F2", "Bb2", "D3", "F3", "Bb3", "D4", "F4")], tm.t(25), rng,
              gain=0.85, step=0.08, dur=3.6)

    # coarde: acorduri lungi, moi
    lvl = lambda c: {0: 0.5, 1: 0.5}.get(c["bar"], 0.6 if c["bar"] < 10 else (0.8 if c["bar"] < 14 else  # noqa: E731
                                                                              (0.95 if c["bar"] < 22 else 0.7)))
    pad_chords(st, "pad", chev, 53, 67, rng, gain=1.0, maxn=3, attack=0.5, release=0.6, bright=0.28,
               gain_fn=lvl, vib=0.08)
    low_strings(st, chev, rng, lo=36, gain=0.7, attack=0.35, octave=False)
    # corni moi în mijloc
    for c in sec(10, 14):
        for m in voicing(c["name"], 53, 62, 2):
            st.add("horns", brass(mhz(m), c["d"] * 0.97, rng, 0.12, 0.0), c["t"], gain=0.5, pan=-0.3)
    # clarinetul: contracânt (note lungi ale acordului) sub tema viorilor
    cc = []
    prev = 62
    for c in sec(14, 22):
        m = nearest_tone(c["name"], prev, 58, 67)
        cc.append((c["t"], c["d"], m, 0.75))
        prev = m
    cl += cc
    # celesta: sclipiri pe acordul final
    for k, nm in enumerate(["Bb5", "D6", "F6", "Bb6"]):
        st.add("cel", celesta(midi(nm), rng, 3.0), tm.t(25) + 0.35 + 0.22 * k, gain=0.8, pan=0.4)
    for t0, d, m, v in mel(CODA_II[:2], 22, tm):
        st.add("cel", celesta(m + 12, rng, 1.8), t0, gain=0.35, pan=0.45)
    timp_roll(st, "Bb", tm.t(25), tm.t(25, 2.5), 0.25, 0.05, rng, rate=13)

    st.add("vln", bowed_line(vln, total, rng, voices=4, vib=0.22, bright=0.5, pan=-0.3, spread=0.4), 0.0)
    st.add("winds", wind_line(sorted(cl), total, rng, "clarinet", pan=0.12), 0.0)
    st.add("winds", wind_line(fl, total, rng, "flute", pan=-0.08, hold_last=1.6), 0.0)

    targets = {"vln": (-18.0, 0.28), "winds": (-18.5, 0.28), "pad": (-24.5, 0.32), "low": (-25.5, 0.2),
               "harp": (-21.5, 0.3), "horns": (-26.0, 0.32), "cel": (-27.0, 0.35), "timp": (-33.0, 0.35)}
    secs = [dict(name=nm, bar0=b0, t=round(tm.t(b0), 3)) for nm, b0, nb in SECS_II]
    return st, targets, secs, end, total


# ================================================================== randare – mișcarea a III-a
def render_III(seed=1788):
    rng = rng_of(seed)
    tm, nb, ring, _ = LAYOUT[2]
    end = tm.t(nb)
    total = end + ring
    st = Stems(total)
    chev = chords(CH_MAEST + CH_C + CH_C + CH_BRIDGE + CH_A[:4] + CH_FINAL_III, 0, tm)
    sec = lambda b0, b1: [c for c in chev if b0 <= c["bar"] < b1]  # noqa: E731

    vln = mel(THEME_C, 4, tm) + mel(THEME_C, 12, tm) + mel(BRIDGE_VLN, 20, tm) + mel(THEME_A[:4], 24, tm) + \
        mel(FINAL_III, 28, tm)
    fl = mel(THEME_C, 12, tm, vel=0.85) + mel(BRIDGE_VLN[3:], 23, tm) + mel(THEME_A[:4], 24, tm) + \
        mel(FINAL_III, 28, tm)

    # ---- Maestoso (1–4): motivul orașului la alămuri, în octave (trompete, corni, tromboni)
    timp_roll(st, "D", tm.t(0), tm.t(1) - 0.05, 0.12, 0.85, rng)
    st.add("low", string_note(mhz(midi("D2")), tm.t(1), rng, 2.2, 0.3, 0.35), 0.0, gain=1.0, pan=0.4)
    st.add("low", string_note(mhz(midi("D3")), tm.t(1), rng, 2.2, 0.3, 0.4), 0.0, gain=0.6, pan=0.3)
    st.add("cym", cymbal_swell(rng, tm.t(1) - tm.t(0, 1.5)), tm.t(0, 1.5), gain=0.5, pan=0.25)
    brass_line(st, "horns", mel(MOTTO_LOW, 1, tm), rng, bright=0.55, gain=1.0, pan=-0.3, legato=0.95)
    brass_line(st, "trb", mel(MOTTO_LOW, 1, tm, transpose=-12), rng, bright=0.45, gain=1.0, pan=0.3, legato=0.95)
    brass_line(st, "tpt", mel(MOTTO, 1, tm), rng, bright=0.8, gain=0.8, pan=0.2, legato=0.95)
    for c in sec(1, 3):
        st.add("tuba", brass(mhz(root_in(c["name"], 38)), c["d"] * 0.96, rng, 0.15, 0.1), c["t"], gain=1.0, pan=0.35)
    pad_chords(st, "pad", sec(1, 3), 50, 74, rng, gain=0.6, maxn=5, attack=0.08, release=0.4)
    low_strings(st, sec(1, 3), rng, gain=1.0, attack=0.05)
    timp_hit(st, "D", tm.t(1), rng, 1.0)
    st.add("bd", bass_drum(rng), tm.t(1), gain=0.8)
    st.add("cym", cymbal(rng, 3.2), tm.t(1), gain=1.0, pan=0.25)
    timp_hit(st, "D", tm.t(2, 1), rng, 0.75)
    # măsura 4: cortina se ridică – glissando de harpă, tremolo, rulouri
    harp_gliss(st, midi("A2"), midi("A6"), D_MAJOR, tm.t(3), tm.t(3, 2.6) - tm.t(3), rng, gain=1.0)
    pad_chords(st, "pad", sec(3, 4), 57, 76, rng, gain=1.0, maxn=5, trem=0.7, attack=1.6, release=0.15)
    low_strings(st, sec(3, 4), rng, gain=0.9, attack=1.0)
    timp_roll(st, "A", tm.t(3), tm.t(4) - 0.03, 0.15, 0.9, rng)
    k = 0
    for t in np.arange(tm.t(3, 2), tm.t(4) - 0.03, 0.045):
        u = (t - tm.t(3, 2)) / (tm.t(4) - tm.t(3, 2))
        st.add("sn", snare(rng, 1.0, 0.18), t, gain=(0.12 + 0.6 * u) * (0.85 if k % 2 else 1.0), pan=-0.15)
        k += 1

    # ---- Allegro (5–32)
    def march(c, lvl=1.0, piatti=True, horns=True, pad=True):
        """Acompaniament de marș festiv pe un acord: bas pe timpi, „pah” la corni pe contratimp, tobe."""
        if pad:
            pad_chords(st, "pad", [c], 55, 72, rng, gain=0.75 * lvl, attack=0.05, release=0.2)
        for b in np.arange(c["beat"], c["beat"] + c["beats"]):
            t = tm.t(c["bar"], b)
            r = root_in(c["name"], 38)
            if b % 2 == 0:
                m = r if b % 4 == 0 else r + 7
                st.add("tuba", brass(mhz(m), 0.55 * tm.beat_s(c["bar"]), rng, 0.15, 0.1), t, gain=lvl, pan=0.35)
                st.add("low", string_note(mhz(m + 12), 0.7 * tm.beat_s(c["bar"]), rng, 0.02, 0.1, 0.45, 3), t,
                       gain=0.7 * lvl, pan=0.35)
                st.add("bd", bass_drum(rng), t, gain=lvl * (1.0 if b % 4 == 0 else 0.8))
                if piatti:
                    st.add("cym", cymbal(rng, 0.7), t, gain=0.3 * lvl, pan=0.3)
                if c["name"][0] in "DA":
                    timp_hit(st, "D" if (c["name"][0] == "D") == (b % 4 == 0) else "A", t, rng, 0.65 * lvl)
            elif horns:
                brass_chord(st, "horns", voicing(c["name"], 55, 67, 3), t, 0.4 * tm.beat_s(c["bar"]), rng, 0.5,
                            gain=0.75 * lvl, pan=-0.3, spread=0.2)
            for sb, g in ((0, 0.75), (0.5, 0.45), (0.75, 0.35)):
                st.add("sn", snare(rng), t + sb * tm.beat_s(c["bar"]), gain=lvl * g * rng.uniform(0.9, 1.0), pan=-0.15)

    for c in sec(4, 12):
        march(c, 0.85, piatti=False)
    brass_line(st, "tpt", mel(THEME_C, 4, tm), rng, bright=1.0, gain=1.0, pan=0.2, legato=0.88)
    st.add("cym", cymbal(rng), tm.t(4), gain=1.0, pan=0.25)
    st.add("cym", cymbal(rng), tm.t(8), gain=0.6, pan=0.25)

    for c in sec(12, 20):
        march(c, 1.0)
    brass_line(st, "tpt", mel(THEME_C[4:], 16, tm), rng, bright=1.0, gain=0.9, pan=0.2, legato=0.88)
    cc, prev = [], 64
    for c in sec(12, 20):
        m = nearest_tone(c["name"], prev, 57, 69)
        cc.append((c["t"], c["d"], m, 0.8))
        prev = m
    brass_line(st, "horns", cc, rng, bright=0.45, gain=0.75, pan=-0.35, legato=0.97)
    for t0, d, m, v in mel(THEME_C, 12, tm):
        if m is not None and d >= 0.99 * tm.beat_s(12):
            st.add("glock", glock(m + 12, rng), t0, gain=0.7, pan=0.4)
    st.add("cym", cymbal(rng), tm.t(12), gain=0.9, pan=0.25)
    st.add("cym", cymbal(rng), tm.t(16), gain=0.7, pan=0.25)

    # punte (21–24)
    pad_chords(st, "pad", sec(20, 24), 55, 72, rng, gain=0.8, attack=0.08, release=0.25)
    low_strings(st, sec(20, 24), rng, gain=0.9, attack=0.05)
    brass_line(st, "horns", mel(BRIDGE_HRN, 20, tm), rng, bright=0.7, gain=1.1, pan=-0.3, legato=0.95)
    brass_line(st, "trb", mel(BRIDGE_HRN, 20, tm, transpose=-12), rng, bright=0.5, gain=0.7, pan=0.3, legato=0.95)
    for b in (20, 21, 22):
        timp_hit(st, "D" if b != 20 else "A", tm.t(b), rng, 0.6)
        st.add("bd", bass_drum(rng), tm.t(b), gain=0.6)
    brass_line(st, "tpt", mel(BRIDGE_VLN[3:], 23, tm), rng, bright=1.0, gain=0.9, pan=0.2, legato=0.9)
    timp_roll(st, "A", tm.t(23), tm.t(24) - 0.03, 0.25, 0.95, rng)
    k = 0
    for t in np.arange(tm.t(23, 2), tm.t(24) - 0.03, 0.045):
        u = (t - tm.t(23, 2)) / (tm.t(24) - tm.t(23, 2))
        st.add("sn", snare(rng, 1.0, 0.18), t, gain=(0.15 + 0.6 * u) * (0.85 if k % 2 else 1.0), pan=-0.15)
        k += 1

    # tema A din mișcarea I (25–28), la trompete
    for c in sec(24, 28):
        march(c, 1.0)
    brass_line(st, "tpt", mel(THEME_A[:4], 24, tm), rng, bright=1.0, gain=1.0, pan=0.2, legato=0.88)
    for t0, d, m, v in mel(THEME_A[:4], 24, tm):
        if m is not None and d >= 0.99 * tm.beat_s(24):
            st.add("glock", glock(m + 12, rng), t0, gain=0.7, pan=0.4)
    st.add("cym", cymbal(rng), tm.t(24), gain=1.0, pan=0.25)

    # final (29–32) + lovitura de încheiere
    for c in sec(28, 30):
        march(c, 1.05, horns=False)
    brass_line(st, "tpt", mel(FINAL_III[:2], 28, tm), rng, bright=1.0, gain=1.1, pan=0.2, legato=0.94)
    brass_line(st, "horns", mel(FINAL_III[:2], 28, tm, transpose=-12), rng, bright=0.6, gain=1.0, pan=-0.3,
               legato=0.94)
    brass_line(st, "trb", mel(FINAL_III[:2], 28, tm, transpose=-24), rng, bright=0.5, gain=0.8, pan=0.3,
               legato=0.94)
    st.add("cym", cymbal(rng), tm.t(28), gain=1.0, pan=0.25)
    for c in sec(30, 31):
        brass_chord(st, "horns", voicing(c["name"], 55, 69, 4), c["t"], c["d"] * 0.9, rng, 0.6, gain=0.9, pan=-0.3)
        brass_chord(st, "tpt", voicing(c["name"], 62, 74, 3), c["t"], c["d"] * 0.9, rng, 0.9, gain=0.7, pan=0.2)
        st.add("tuba", brass(mhz(root_in(c["name"], 38)), c["d"] * 0.9, rng, 0.15, 0.1), c["t"], gain=1.0,
               pan=0.35)
    pad_chords(st, "pad", sec(30, 31), 55, 74, rng, gain=0.9, trem=0.5, attack=0.05)
    low_strings(st, sec(30, 31), rng, gain=1.0, attack=0.05)
    timp_roll(st, "A", tm.t(30, 2), tm.t(31) - 0.03, 0.3, 1.0, rng)
    k = 0
    for t in np.arange(tm.t(30, 2), tm.t(31) - 0.03, 0.045):
        st.add("sn", snare(rng, 1.0, 0.18), t, gain=(0.2 + 0.5 * (t - tm.t(30, 2)) / (tm.t(31) - tm.t(30, 2))) *
               (0.85 if k % 2 else 1.0), pan=-0.15)
        k += 1
    # măsura 32: acordul lung de Re major, cu ruloul timpanilor, apoi lovitura finală
    L = tm.t(32) - tm.t(31) - 0.06
    brass_chord(st, "tpt", [midi(x) for x in ("D5", "F#5", "A5")], tm.t(31), L, rng, 1.0, gain=1.15, pan=0.2)
    brass_chord(st, "horns", [midi(x) for x in ("A3", "D4", "F#4", "A4")], tm.t(31), L, rng, 0.6, gain=1.0, pan=-0.3)
    brass_chord(st, "trb", [midi(x) for x in ("D3", "A3", "D4")], tm.t(31), L, rng, 0.5, gain=0.9, pan=0.3)
    st.add("tuba", brass(mhz(midi("D2")), L, rng, 0.15, 0.1), tm.t(31), gain=1.0, pan=0.35)
    for j, m in enumerate(voicing("D", 50, 78, 6)):
        st.add("pad", string_note(mhz(m), L, rng, 0.02, 0.25, 0.6, trem=0.4), tm.t(31), gain=0.45, pan=-0.3 + 0.12 * j)
    st.add("low", string_note(mhz(midi("D2")), L, rng, 0.02, 0.25, 0.4), tm.t(31), gain=1.0, pan=0.4)
    timp_hit(st, "D", tm.t(31), rng, 1.0)
    timp_roll(st, "D", tm.t(31, 0.3), tm.t(32) - 0.05, 0.35, 0.9, rng)
    st.add("cym", cymbal(rng), tm.t(31), gain=1.0, pan=0.25)
    tf = tm.t(32)
    brass_chord(st, "tpt", [midi(x) for x in ("D5", "F#5", "A5")], tf, 0.5, rng, 1.0, gain=1.2, pan=0.2)
    brass_chord(st, "horns", [midi(x) for x in ("A3", "D4", "F#4", "A4")], tf, 0.5, rng, 0.6, gain=1.0, pan=-0.3)
    brass_chord(st, "trb", [midi(x) for x in ("D3", "A3", "D4")], tf, 0.5, rng, 0.5, gain=0.9, pan=0.3)
    st.add("tuba", brass(mhz(midi("D2")), 0.5, rng, 0.15, 0.1), tf, gain=1.0, pan=0.35)
    for j, m in enumerate(voicing("D", 50, 81, 7)):
        st.add("pad", string_note(mhz(m), 0.45, rng, 0.01, 0.3, 0.6), tf, gain=0.5, pan=-0.3 + 0.1 * j)
    st.add("low", string_note(mhz(midi("D2")), 0.45, rng, 0.01, 0.3, 0.4), tf, gain=1.0, pan=0.4)
    timp_hit(st, "D", tf, rng, 1.0)
    st.add("bd", bass_drum(rng), tf, gain=1.0)
    st.add("cym", cymbal(rng, 3.6), tf, gain=1.0, pan=0.25)
    harp_roll(st, [midi(x) for x in ("D2", "A2", "D3", "F#3", "A3", "D4", "F#4", "A4")], tf, rng, gain=0.9,
              step=0.03, dur=3.4)
    for k2, nm in enumerate(["D6", "F#6", "A6", "D7"]):
        st.add("glock", glock(midi(nm), rng, 2.4), tf + 0.06 * k2, gain=0.7, pan=0.4)
    vln.append((tf, 0.45, midi("D6"), 1.0))
    fl.append((tf, 0.45, midi("D6"), 1.0))

    st.add("vln", bowed_line(vln, total, rng, voices=4, vib=0.16, bright=0.7, pan=-0.35, spread=0.35), 0.0)
    st.add("winds", wind_line(fl, total, rng, "flute", pan=-0.08), 0.0)

    targets = {"vln": (-19.0, 0.22), "winds": (-22.0, 0.25), "tpt": (-18.5, 0.22), "horns": (-21.0, 0.3),
               "trb": (-23.0, 0.25), "tuba": (-22.5, 0.12), "pad": (-22.0, 0.28), "low": (-22.0, 0.15),
               "timp": (-21.5, 0.3), "sn": (-25.5, 0.2), "bd": (-25.0, 0.2), "cym": (-27.5, 0.25),
               "harp": (-24.0, 0.3), "glock": (-27.0, 0.3)}
    secs = [dict(name=nm, bar0=b0, t=round(tm.t(b0), 3)) for nm, b0, nb in SECS_III]
    return st, targets, secs, end, total


# ================================================================== mix
STRING_STEMS = {"vln": True, "pad": True, "low": False}


def mix_movement(st, targets, ir, end, target_lufs):
    mix = stereo(st.total)
    for k, buf in st.b.items():
        tgt, wet = targets[k]
        x = buf
        if k in STRING_STEMS:
            x = body_eq(x, STRING_STEMS[k])
        x = hp(x, 30)
        x = match_lufs(x, tgt)
        report(x, "   " + k)
        mix += reverb(x, ir, wet=wet, dry=1.0)
    mix = match_lufs(mix, target_lufs)
    # stingere: după ultimul sunet, coada sălii se stinge până la capătul bufferului
    t = t_axis(mix.shape[1])
    f0 = st.total - 1.4
    g = np.ones_like(t)
    m = t >= f0
    g[m] = np.cos(0.5 * np.pi * np.clip((t[m] - f0) / 1.4, 0, 1)) ** 2
    return mix * g


def layout():
    """Începutul, sfârșitul muzicii și sfârșitul sunetului pentru fiecare mișcare (s, absolut)."""
    t = LEAD_IN
    out = []
    for (tm, nb, ring, secs), mv in zip(LAYOUT, MOVEMENTS):
        end = tm.t(nb)
        out.append(dict(mv=mv, tm=tm, t0=t, end=end, total=end + ring, secs=secs))
        t += end + ring + GAP
    return out, t - GAP + 0.4


def marks_info(dur=None):
    lay, total = layout()
    mvs = []
    for L in lay:
        mvs.append({**L["mv"], "inceput_s": round(L["t0"], 2), "sfarsit_muzica_s": round(L["t0"] + L["end"], 2),
                    "sfarsit_sunet_s": round(L["t0"] + L["total"], 2),
                    "sectiuni": [dict(nume=nm, masura=b0 + 1, t_s=round(L["t0"] + L["tm"].t(b0), 2))
                                 for nm, b0, nb in L["secs"]]})
    # melodiile principale (pentru verificarea notă cu notă în MP3)
    items = [(0, "Tema A", "viori I", THEME_A, 4, 0), (0, "Episod", "clarinet", EPISODE_B[:4], 20, 0),
             (0, "Episod", "flaut", EPISODE_B[4:], 24, 0), (0, "Coda: motivul orașului", "trompete", CODA_I[:2], 36, 0),
             (1, "Tema lirică", "clarinet", THEME_II, 2, 0), (1, "Mijloc", "flaut", MID_II, 10, 0),
             (1, "Tema, la viori", "viori I", THEME_II, 14, 12),
             (1, "Coda: motivul orașului", "clarinet", CODA_II[:2], 22, 0),
             (2, "Maestoso: motivul orașului", "trompete, corni și tromboni, în octave", MOTTO, 1, 0),
             (2, "Tema festivă", "trompete și viori", THEME_C, 4, 0),
             (2, "Tema A din mișcarea I", "trompete, viori, flaut", THEME_A[:4], 24, 0),
             (2, "Final: motivul orașului", "trompete, viori, flaut", FINAL_III[:2], 28, 0)]
    notes = []
    for k, sec, inst, bars, b0, tr in items:
        L = lay[k]
        for t0, d, m, v in mel(bars, b0, L["tm"], tr):
            if m is not None:
                notes.append(dict(miscare=L["mv"]["nr"], sectiune=sec, instrument=inst, t=round(L["t0"] + t0, 3),
                                  d=round(d, 3), midi=int(m)))
    return {"titlu_creativ": "Piață, pagină, cortină", "durata_s": round(dur if dur else total, 2),
            "marcaje_s": [m["inceput_s"] for m in mvs], "pauza_intre_miscari_s": GAP, "miscari": mvs,
            "motivul_orasului": {"I": MOTTO, "II": CODA_II[:2], "III": MOTTO_LOW},
            "melodii_principale": notes}


def render():
    ir = make_ir(t60=2.2, predelay=0.022, seed=1949, hf_ratio=0.42, lf_ratio=1.2)
    lay, TOTAL = layout()
    out = stereo(TOTAL)
    for L, fn, tgt in zip(lay, (render_I, render_II, render_III), (-15.0, -19.0, -13.5)):
        st, targets, secs, end, total = fn()
        assert abs(end - L["end"]) < 1e-9 and abs(total - L["total"]) < 1e-9
        print(f"mișcarea {L['mv']['nr']}: {end:.2f} s muzică + {total - end:.2f} s coadă, de la {L['t0']:.2f} s")
        add(out, mix_movement(st, targets, ir, end, tgt), L["t0"])
    return out


# ================================================================== notația pentru fișa .md
DUR_NAME = {0.25: "ș", 0.5: "o", 0.75: "o.", 1.0: "p", 1.5: "p.", 2.0: "d", 3.0: "d.", 4.0: "n"}


def fmt_t(t):
    s = f"{t % 60:04.1f}".replace(".", ",")
    return f"{int(t // 60)}:{s}"


def fmt_chords(ch):
    out = []
    for tok in ch.split():
        if ":" in tok:
            nm, b = tok.split(":")
            b = float(b)
            out.append(f"{nm} ({b:g} {'timp' if b == 1 else 'timpi'})".replace(".", ","))
        else:
            out.append(tok)
    return " – ".join(out)


def notation():
    lay, _ = layout()
    items = [  # (mișcare, titlu, instrument, măsuri, măsura de început, acorduri)
        (0, "Motivul orașului (introducere, corni – sună cu o octavă mai jos decât e scris aici)", MOTTO, 0,
         CH_INTRO[:2]),
        (0, "Tema A (viori I)", THEME_A, 4, CH_A),
        (0, "Episodul în si minor (clarinet, apoi flaut)", EPISODE_B, 20, CH_B),
        (1, "Tema lirică (clarinet)", THEME_II, 2, CH_II),
        (1, "Mijlocul (flaut)", MID_II, 10, CH_MID_II),
        (1, "Coda: motivul orașului (clarinet, apoi flaut)", CODA_II, 22, CH_CODA_II),
        (2, "Maestoso: motivul orașului (trompete; corni și tromboni în octave, dedesubt)", MOTTO, 1, CH_MAEST[1:3]),
        (2, "Tema festivă (trompete și viori)", THEME_C, 4, CH_C),
    ]
    out = []
    for k, title, bars, b0, chs in items:
        L = lay[k]
        tm = L["tm"]
        out.append(f"### {L['mv']['nr']}. {title}\n")
        out.append("| Măs. | Timp | Acorduri | Note (durată) |")
        out.append("|---|---|---|---|")
        for j, (b, ch) in enumerate(zip(bars, chs)):
            notes = parse_bar(b, tm.bpb)
            nt = " · ".join(("pauză" if m is None else tok.split(":")[0]) + f" {DUR_NAME[d]}"
                            for (m, d), tok in zip(notes, b.split()))
            out.append(f"| {b0 + j + 1} | {fmt_t(L['t0'] + tm.t(b0 + j))} | {fmt_chords(ch)} | {nt} |")
        out.append("")
    return "\n".join(out)


def write_marks(dur=None):
    info = marks_info(dur)
    with open(os.path.join(HERE, "A21_marcaje.json"), "w", encoding="utf-8") as fh:
        json.dump(info, fh, ensure_ascii=False, indent=1)
    return info


if __name__ == "__main__":
    if "--notatie" in sys.argv:
        print(notation())
        sys.exit(0)
    if "--marcaje" in sys.argv:
        info = write_marks()
        print(json.dumps({k: v for k, v in info.items() if k != "melodii_principale"}, ensure_ascii=False, indent=1))
        sys.exit(0)
    mix = render()
    out = finalize(mix, OUT, "A21 Piață, pagină, cortină – uvertură AI pentru un oraș, în 3 mișcări",
                   "Temă originală în stil de uvertură de concert; orchestră sintetizată în cod, fără mostre – "
                   "ACTIV AI, calupul Cultură vie", target_lufs=-14.0, fin=0.02, fout=0.5)
    report(out, "A21 final")
    info = write_marks(out.shape[1] / SR)
    print(json.dumps({k: v for k, v in info.items() if k != "melodii_principale"}, ensure_ascii=False, indent=1))
