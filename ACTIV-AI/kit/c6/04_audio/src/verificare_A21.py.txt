"""Verificare tehnică pentru A21 „Piață, pagină, cortină” (uvertură în 3 mișcări).

Măsoară MP3-ul final (nu mixul din memorie): ffprobe (format, durată, debit), ffmpeg ebur128
(loudness integrat, LRA, true peak, vârf de eșantion), eșantioane la limită (clipping), salturi bruște
între eșantioane (tăieturi), liniștea dintre mișcări, stingerea fiecărei mișcări înainte de pauză,
loudness pe mișcări, tonalitatea estimată pe mișcări (cromagramă + profilurile Krumhansl–Kessler),
periodicitatea dominantă a atacurilor (tempo estimat), spectrogramă (axă logaritmică) și formă de undă
cu loudness pe termen scurt. Fișele .md: ortografie (hunspell ro_RO) și ș/ț cu sedilă.

Rulare: python3 verificare_A21.py -> ../_verificare/raport_A21.json + PNG-uri
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, "/home/claude/expo/04_audio/_src")
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from scipy import signal  # noqa: E402

from audiolib import SR, _KW, lufs  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
VER = os.path.join(ROOT, "_verificare")
os.makedirs(VER, exist_ok=True)
MP3 = os.path.join(ROOT, "A21_uvertura_pentru_un_oras.mp3")
NAMES = ["Do", "Do#", "Re", "Mi bemol", "Mi", "Fa", "Fa#", "Sol", "La bemol", "La", "Si bemol", "Si"]
KS_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
KS_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def ffprobe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", path],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    st, fm = j["streams"][0], j["format"]
    return {"codec": st["codec_name"], "sample_rate_hz": int(st["sample_rate"]), "canale": st["channels"],
            "bitrate_kbps": round(int(st.get("bit_rate", fm["bit_rate"])) / 1000),
            "durata_s": round(float(fm["duration"]), 2), "titlu_id3": fm.get("tags", {}).get("title", "")}


def ebur128(path):
    err = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-filter_complex", "ebur128=peak=true+sample",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    summ = err[err.rfind("Summary:"):]
    g = lambda pat: float(re.search(pat, summ).group(1))  # noqa: E731
    return {"loudness_integrat_lufs": g(r"I:\s+(-?[\d.]+) LUFS"), "lra_lu": g(r"LRA:\s+(-?[\d.]+) LU"),
            "true_peak_dbtp": g(r"True peak:\s+Peak:\s+(-?[\d.]+) dBFS"),
            "sample_peak_dbfs": g(r"Sample peak:\s+Peak:\s+(-?[\d.]+) dBFS")}


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).T.astype(np.float64)


def db(x):
    return float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12))


def short_term(x, win=3.0, hop=0.1):
    y = x
    for b, a in _KW:
        y = signal.lfilter(b, a, y, axis=-1)
    p = (y ** 2).sum(axis=0)
    w, h = int(win * SR), int(hop * SR)
    cs = np.concatenate([[0], np.cumsum(p)])
    st = np.arange(0, len(p) - w, h)
    return (st + w / 2) / SR, -0.691 + 10 * np.log10((cs[st + w] - cs[st]) / w + 1e-20)


def key_estimate(mono):
    """Cromagramă pe tot fragmentul (110–2000 Hz) corelată cu profilurile Krumhansl–Kessler."""
    f, t, Z = signal.stft(mono, SR, nperseg=8192, noverlap=8192 - 2048)
    mag = np.abs(Z)
    keep = (f >= 110) & (f <= 2000)
    pcs = np.round(12 * np.log2(f[keep] / 440.0) + 69).astype(int) % 12
    chroma = np.zeros(12)
    np.add.at(chroma, pcs, np.sqrt(mag[keep]).sum(axis=1))
    res = []
    for k in range(12):
        res.append((float(np.corrcoef(chroma, np.roll(KS_MAJ, k))[0, 1]), f"{NAMES[k]} major"))
        res.append((float(np.corrcoef(chroma, np.roll(KS_MIN, k))[0, 1]), f"{NAMES[k].lower()} minor"))
    res.sort(reverse=True)
    return [{"tonalitate": nm, "corelatie": round(c, 3)} for c, nm in res[:3]]


def tempo_estimate(mono, lo=60, hi=200):
    """Periodicitatea dominantă a atacurilor (flux spectral + autocorelație), în pătrimi pe minut."""
    hop = 512
    f, t, Z = signal.stft(mono, SR, nperseg=2048, noverlap=2048 - hop)
    L = np.log1p(100 * np.abs(Z))
    flux = np.maximum(0, np.diff(L, axis=1)).sum(axis=0)
    flux -= np.convolve(flux, np.ones(40) / 40, mode="same")
    flux = np.maximum(flux, 0)
    ac = np.correlate(flux, flux, mode="full")[len(flux) - 1:]
    fps = SR / hop
    lags = np.arange(len(ac))
    bpm = 60 * fps / np.maximum(lags, 1)
    m = (bpm >= lo) & (bpm <= hi)
    cand = []
    for i in np.argsort(ac[m])[::-1]:
        b = float(bpm[m][i])
        if all(abs(b - c) / c > 0.04 for c in cand):
            cand.append(b)
        if len(cand) == 3:
            break
    return [round(c, 1) for c in cand]


def tempo_ok(est, declared):
    """Estimarea corespunde tempo-ului declarat sau unui multiplu simplu (pătrimi, optimi, măsuri)?"""
    for e in est[:2]:
        for r in (0.5, 1.0, 2.0, 1 / 3, 3.0, 2 / 3, 1.5):
            if abs(e - declared * r) / (declared * r) < 0.04:
                return True, round(r, 3)
    return False, None


def melody_check(x, notes):
    """Pentru fiecare notă a melodiilor principale: înălțimea dominantă în registrul melodiei
    (fundamentală + armonicele 2 și 3), comparată cu nota scrisă."""
    mono = x.mean(axis=0)
    groups = {}
    for nt in notes:
        groups.setdefault((nt["miscare"], nt["sectiune"], nt["instrument"]), []).append(nt)
    out = []
    for (mv, sec, inst), nts in groups.items():
        lo, hi = min(n["midi"] for n in nts) - 2, max(n["midi"] for n in nts) + 2
        ok, bad = 0, []
        for nt in nts:
            a = int((nt["t"] + 0.035) * SR)
            b = int((nt["t"] + min(max(nt["d"] - 0.03, 0.08), 0.45)) * SR)
            seg = mono[a:b] * np.hanning(b - a)
            N = 1 << 16
            sp = np.abs(np.fft.rfft(seg, N))
            fr = np.fft.rfftfreq(N, 1 / SR)

            def band(f):
                m = (fr > f * 2 ** (-0.3 / 12)) & (fr < f * 2 ** (0.3 / 12))
                return sp[m].max() if np.any(m) else 0.0

            hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)  # noqa: E731
            score = {m: band(hz(m)) + 0.8 * band(2 * hz(m)) + 0.6 * band(3 * hz(m)) for m in range(lo, hi + 1)}
            best = max(score, key=score.get)
            if best == nt["midi"]:
                ok += 1
            else:
                bad.append({"t": nt["t"], "scris_midi": nt["midi"], "detectat_midi": best,
                            "aceeasi_nota_alta_octava": (best - nt["midi"]) % 12 == 0})
        okpc = ok + sum(b["aceeasi_nota_alta_octava"] for b in bad)
        out.append({"miscare": mv, "sectiune": sec, "instrument": inst, "note": len(nts), "recunoscute_exact": ok,
                    "recunoscute_indiferent_de_octava": okpc, "procent_exact": round(100 * ok / len(nts), 1),
                    "nepotriviri": bad})
    return out


def click_index(x):
    """Salturi izolate între eșantioane: saltul raportat la RMS-ul diferențelor din jur (20 ms).
    Un clic (tăietură) dă un raport mare (> 10); atacurile de tobă, talgere și timpani rămân sub."""
    from scipy.ndimage import uniform_filter1d
    d = np.abs(np.diff(x, axis=1)).max(axis=0)
    rms = np.sqrt(np.maximum(uniform_filter1d(d ** 2, size=int(0.02 * SR)), 0))
    r = np.where(d > 0.02, d / (rms + 1e-6), 0)
    i = int(np.argmax(r))
    return round(float(r[i]), 1), round(i / SR, 2), int(np.sum(r > 10))


def plots(x, info):
    mono = x.mean(axis=0)
    t_end = len(mono) / SR
    f, t, Z = signal.spectrogram(mono, SR, window="hann", nperseg=4096, noverlap=4096 - 1024, mode="magnitude")
    Zdb = 20 * np.log10(Z + 1e-9)
    Zdb -= Zdb.max()
    fig, ax = plt.subplots(figsize=(18, 7.5), dpi=110)
    keep = (f >= 30) & (f <= 18000)
    pc = ax.pcolormesh(t, f[keep], Zdb[keep], shading="auto", cmap="magma", vmin=-90, vmax=0)
    ax.set_yscale("log")
    ax.set_ylim(30, 18000)
    ax.set_yticks([50, 100, 200, 400, 800, 1600, 3200, 6400, 12800])
    ax.set_yticklabels(["50", "100", "200", "400", "800", "1,6k", "3,2k", "6,4k", "12,8k"])
    gap = info["pauza_intre_miscari_s"]
    for k, mv in enumerate(info["miscari"]):
        t0 = mv["inceput_s"]
        ax.axvline(t0, color="#E2A62B", lw=2.2)
        if k + 1 < len(info["miscari"]):
            ax.axvspan(mv["sfarsit_sunet_s"], mv["sfarsit_sunet_s"] + gap, color="#12A594", alpha=0.25)
        ax.text(t0 + 0.8, 13500, f"{mv['nr']}. {mv['titlu']}", color="#0F1720", fontsize=10, weight="bold",
                bbox=dict(facecolor="#E2A62B", alpha=0.95, edgecolor="none", pad=2))
        for k, s in enumerate(mv["sectiuni"][1:]):
            ax.axvline(s["t_s"], color="#F3EFE6", lw=0.7, alpha=0.6, ls="--")
            ax.text(s["t_s"] + 0.4, [45, 36, 58][k % 3], f"m. {s['masura']}", color="#F3EFE6", fontsize=7.5)
    ax.set_xlim(0, t_end)
    ax.set_xlabel("timp (s)")
    ax.set_ylabel("frecvență (Hz, scară logaritmică)")
    ax.set_title(f"A21 „Piață, pagină, cortină” – spectrograma MP3 ({t_end:.1f} s); linii ocru: începutul "
                 f"mișcărilor; benzi verzi: liniștea dintre mișcări; linii punctate: secțiuni (măsura)")
    fig.colorbar(pc, ax=ax, label="dB (relativ la maxim)")
    fig.tight_layout()
    p1 = os.path.join(VER, "A21_uvertura_pentru_un_oras_spectrograma.png")
    fig.savefig(p1)
    plt.close(fig)

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(18, 7.5), dpi=110, sharex=True)
    tt = np.arange(len(mono)) / SR
    a1.plot(tt[::100], x[0, ::100], lw=0.4, color="#0E7C86", label="stânga")
    a1.plot(tt[::100], -x[1, ::100], lw=0.4, color="#6E56CF", alpha=0.7, label="dreapta (inversat)")
    for v in (10 ** (-1 / 20), -10 ** (-1 / 20)):
        a1.axhline(v, color="#B9583A", ls="--", lw=0.8)
    a1.set_ylim(-1.05, 1.05)
    a1.set_ylabel("amplitudine")
    a1.legend(loc="lower right", fontsize=8)
    gap = info["pauza_intre_miscari_s"]
    ts, st = short_term(x)
    a2.plot(ts, st, color="#E2A62B", lw=1.4, label="loudness pe termen scurt (3 s)")
    a2.axhline(-14, color="#12A594", ls="--", lw=1, label="țintă −14 LUFS (integrat)")
    a2.set_ylim(-40, -6)
    a2.set_ylabel("LUFS")
    a2.set_xlabel("timp (s)")
    a2.legend(loc="lower right", fontsize=8)
    for k, mv in enumerate(info["miscari"]):
        for ax in (a1, a2):
            ax.axvline(mv["inceput_s"], color="#E2A62B", lw=1.6)
            if k + 1 < len(info["miscari"]):
                ax.axvspan(mv["sfarsit_sunet_s"], mv["sfarsit_sunet_s"] + gap, color="#12A594", alpha=0.25)
        a1.text(mv["inceput_s"] + 0.6, 0.9, f"{mv['nr']}. {mv['titlu']}", fontsize=9, color="#1B2733")
    a1.set_title("A21 – formă de undă (liniile roșii: −1 dBFS) și loudness pe termen scurt; "
                 "benzi verzi: liniștea dintre mișcări")
    fig.tight_layout()
    p2 = os.path.join(VER, "A21_uvertura_pentru_un_oras_forma_unda.png")
    fig.savefig(p2)
    plt.close(fig)
    return p1, p2


def hunspell(path):
    txt = re.sub(r"`[^`]*`", "", open(path, encoding="utf-8").read())
    r = subprocess.run(["hunspell", "-d", "ro_RO", "-i", "utf-8", "-l"], input=txt, capture_output=True, text=True)
    return sorted(set(r.stdout.split())), len(re.findall("[şţŞŢ]", txt))


if __name__ == "__main__":
    info = json.load(open(os.path.join(HERE, "A21_marcaje.json"), encoding="utf-8"))
    probe = ffprobe(MP3)
    loud = ebur128(MP3)
    x = decode(MP3)
    mono = x.mean(axis=0)
    n = x.shape[1]
    env = np.abs(x).max(axis=0)
    nz = np.nonzero(env > 10 ** (-60 / 20))[0]
    jumps = np.abs(np.diff(x, axis=1)).max(axis=0)
    rep = {"fisier": "04_audio/A21_uvertura_pentru_un_oras.mp3", "ffprobe": probe, "ebur128": loud,
           "esantioane_la_limita_0dBFS": int(np.sum(np.abs(x) >= 0.999)),
           "salt_maxim_intre_esantioane": round(float(jumps.max()), 4),
           "inceput_sunet_s": round(nz[0] / SR, 3), "sfarsit_sunet_s": round(nz[-1] / SR, 3)}
    ci, ci_t, ci_n = click_index(x)
    rep["indice_clic_maxim"] = {"raport": ci, "t_s": ci_t, "salturi_izolate_peste_10": ci_n}
    rep["melodii_principale"] = melody_check(x, info["melodii_principale"])
    tot_n = sum(m["note"] for m in rep["melodii_principale"])
    tot_ok = sum(m["recunoscute_exact"] for m in rep["melodii_principale"])
    tot_pc = sum(m["recunoscute_indiferent_de_octava"] for m in rep["melodii_principale"])
    rep["melodii_principale_total"] = {
        "note": tot_n, "recunoscute_exact": tot_ok, "procent_exact": round(100 * tot_ok / tot_n, 1),
        "recunoscute_indiferent_de_octava": tot_pc, "procent_indiferent_de_octava": round(100 * tot_pc / tot_n, 1),
        "explicatie": "unele teme sunt dublate la octava de jos (corni, tromboni); acolo analiza poate alege octava "
                      "de jos – nota este aceeași"}
    mvs = []
    declared = {"I": [(0.0, None, 144)], "II": [(0.0, None, 72)], "III": [(None, None, 132)]}
    for k, mv in enumerate(info["miscari"]):
        a, b = int(mv["inceput_s"] * SR), int(mv["sfarsit_sunet_s"] * SR)
        seg = x[:, a:b]
        item = {"miscare": mv["nr"], "titlu": mv["titlu"], "inceput_s": mv["inceput_s"],
                "durata_s": round(mv["sfarsit_sunet_s"] - mv["inceput_s"], 2),
                "loudness_lufs": round(lufs(seg), 1),
                "loudness_termen_scurt_max_lufs": round(float(short_term(seg)[1].max()), 1),
                "tonalitate_declarata": mv["tonalitate"], "tonalitate_estimata": key_estimate(seg.mean(axis=0))}
        item["corelatie_stereo_L_R"] = round(float(np.corrcoef(seg[0], seg[1])[0, 1]), 2)
        item["echilibru_L_minus_R_db"] = round(db(seg[0]) - db(seg[1]), 1)
        item["tonalitate_confirmata"] = item["tonalitate_estimata"][0]["tonalitate"].lower() == mv["tonalitate"].lower()
        # tempo: pentru mișcarea a III-a se măsoară doar partea Allegro (de la măsura 5)
        a2 = int(mv["sectiuni"][1]["t_s"] * SR) if mv["nr"] == "III" else a
        bpm_decl = 132 if mv["nr"] == "III" else (144 if mv["nr"] == "I" else 72)
        est = tempo_estimate(x[:, a2:int(mv["sfarsit_muzica_s"] * SR)].mean(axis=0))
        ok, ratio = tempo_ok(est, bpm_decl)
        item["tempo_declarat_bpm"] = bpm_decl
        item["tempo_estimat_bpm_candidati"] = est
        item["tempo_confirmat"] = ok
        item["raport_estimat_declarat"] = ratio
        # stingerea: ultimele 0,3 s ale mișcării, înaintea pauzei
        item["nivel_ultimele_0_3_s_dbfs"] = round(db(x[:, b - int(0.3 * SR):b]), 1)
        item["nivel_primele_0_05_s_dbfs"] = round(db(x[:, a:a + int(0.05 * SR)]), 1)
        if k + 1 < len(info["miscari"]):
            c = int(info["miscari"][k + 1]["inceput_s"] * SR)
            gap = x[:, b + int(0.05 * SR):c - int(0.05 * SR)]
            item["pauza_dupa_s"] = round((c - b) / SR, 2)
            item["nivel_pauza_dbfs"] = round(db(gap), 1)
            item["varf_pauza_dbfs"] = round(float(20 * np.log10(np.abs(gap).max() + 1e-12)), 1)
        mvs.append(item)
    rep["miscari"] = mvs
    p1, p2 = plots(x, info)
    rep["grafice"] = ["04_audio/_verificare/" + os.path.basename(p) for p in (p1, p2)]
    rep["conditii"] = {
        "durata_180_240_s": 180 <= probe["durata_s"] <= 240,
        "loudness_minus_14_plus_minus_0_5": abs(loud["loudness_integrat_lufs"] + 14) <= 0.5,
        "true_peak_sub_-1_dBTP": loud["true_peak_dbtp"] <= -1.0,
        "mp3_192_kbps": probe["codec"] == "mp3" and probe["bitrate_kbps"] == 192,
        "esantionare_44100_hz": probe["sample_rate_hz"] == 44100,
        "fara_clipping": rep["esantioane_la_limita_0dBFS"] == 0,
        "fara_clicuri_izolate": rep["indice_clic_maxim"]["salturi_izolate_peste_10"] == 0,
        "melodii_principale_recunoscute_exact_peste_90_la_suta": rep["melodii_principale_total"]["procent_exact"] >= 90,
        "melodii_principale_recunoscute_indiferent_de_octava_peste_95_la_suta":
            rep["melodii_principale_total"]["procent_indiferent_de_octava"] >= 95,
        "trei_miscari": len(mvs) == 3,
        "pauze_intre_miscari_sub_-60_dBFS": all(m.get("nivel_pauza_dbfs", -999) < -60 for m in mvs),
        "miscarile_se_sting_inainte_de_pauza_sub_-45_dBFS": all(m["nivel_ultimele_0_3_s_dbfs"] < -45 for m in mvs),
        "tonalitati_confirmate": all(m["tonalitate_confirmata"] for m in mvs),
        "tempo_confirmat": all(m["tempo_confirmat"] for m in mvs),
        "stereo_compatibil_mono_corelatie_pozitiva": all(m["corelatie_stereo_L_R"] > 0.2 for m in mvs),
        "echilibru_stanga_dreapta_sub_2_dB": all(abs(m["echilibru_L_minus_R_db"]) < 2 for m in mvs),
    }
    rep["ortografie_hunspell_ro_RO"] = {}
    for fn in ("A21_uvertura_pentru_un_oras.md", "_fapte_noi_A21.md"):
        p = os.path.join(ROOT, fn)
        if os.path.exists(p):
            w, sed = hunspell(p)
            rep["ortografie_hunspell_ro_RO"][fn] = {"cuvinte_nerecunoscute": w, "s_t_cu_sedila": sed}
    out = os.path.join(VER, "raport_A21.json")
    conv = lambda o: o.item() if hasattr(o, "item") else str(o)  # noqa: E731
    json.dump(rep, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2, default=conv)
    print(json.dumps(rep, ensure_ascii=False, indent=2, default=conv))
