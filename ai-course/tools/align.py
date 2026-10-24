"""Approximate word start times for a take, without a forced aligner.

Pauses in the take (ffmpeg silencedetect) are matched to the punctuation in its text by a
monotonic alignment; words between two anchors share the time by character count. Good to
about a quarter of a second, which is enough to land a visual beat on a spoken word.
"""
import re, subprocess

def silences(wav, noise='-38dB', d=0.12):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-i', wav, '-af', f'silencedetect=noise={noise}:d={d}', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', err)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    return list(zip(st, en))

def align(text, wav, dur):
    words = text.split()
    sil = silences(wav)
    t0 = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0           # leading silence
    t1 = sil[-1][0] if sil and sil[-1][1] > dur - 0.05 else dur   # trailing silence
    inner = [s for s in sil if s[0] > t0 + 0.05 and s[1] < t1 - 0.05]
    w = [len(x) + 1 for x in words]; tot = sum(w)
    cum = [sum(w[:i]) for i in range(len(words) + 1)]
    est = lambda i: t0 + (t1 - t0) * cum[i] / tot                 # time before word i, by characters
    bnd = [i + 1 for i, x in enumerate(words[:-1]) if re.search(r'[,.;:?!]$', x)]
    # DP: match boundaries to pauses in order; skipping either costs a fixed penalty
    SKIP_B, SKIP_S = 0.9, 0.35
    nb, ns = len(bnd), len(inner)
    INF = float('inf'); D = [[INF] * (ns + 1) for _ in range(nb + 1)]; B = [[None] * (ns + 1) for _ in range(nb + 1)]
    D[0][0] = 0
    for i in range(nb + 1):
        for j in range(ns + 1):
            if D[i][j] == INF: continue
            if i < nb and D[i][j] + SKIP_B < D[i + 1][j]: D[i + 1][j], B[i + 1][j] = D[i][j] + SKIP_B, (i, j, 0)
            if j < ns and D[i][j] + SKIP_S < D[i][j + 1]: D[i][j + 1], B[i][j + 1] = D[i][j] + SKIP_S, (i, j, 0)
            if i < nb and j < ns:
                c = D[i][j] + abs(est(bnd[i]) - (inner[j][0] + inner[j][1]) / 2)
                if c < D[i + 1][j + 1]: D[i + 1][j + 1], B[i + 1][j + 1] = c, (i, j, 1)
    i, j, pairs = nb, ns, []
    while (i, j) != (0, 0):
        pi, pj, m = B[i][j]
        if m: pairs.append((bnd[pi], inner[pj]))
        i, j = pi, pj
    pairs.reverse()
    # anchors: (word index, start time of that word, end time of the previous word)
    anchors = [(0, t0, t0)] + [(k, s[1], s[0]) for k, s in pairs] + [(len(words), t1, t1)]
    starts = []
    for (ka, ta, _), (kb, _, tb) in zip(anchors, anchors[1:]):
        span = sum(w[ka:kb]); acc = 0
        for k in range(ka, kb):
            starts.append(round(ta + (tb - ta) * acc / span, 3)); acc += w[k]
    return [[re.sub(r'[^\w\'-]', '', x).lower(), t] for x, t in zip(words, starts)]
