"""Stage 4 — shard + heat map. Chapters over the token cap are shattered at their headings (then paragraphs) into
shards; every shard is a pointer (line range + hash), never a copy of the text.

Each shard carries a deterministic 5-D structural fingerprint in the spectral-terrain 0-dim lineage
(scripts/geo_rag_ingest.py: log1p(tokens), sha256[:8] % 1000 / 1000, log1p(depth)), extended for prose:
  [log1p(tokens), hash_norm, log1p(headings), log1p(links), log1p(code_blocks + table_rows)]
The heat map normalizes across the corpus (min-max, as geo_rag_ingest does) and scores each shard:
  shatter = euclidean distance from the corpus centroid   (spectral calibrate.ts)
  heat    = manhattan resonance sum|v|                     (spectral calibrate.ts)
plus its k nearest neighbours, so the corpus is navigable geometry. No network, no model, no numpy.
"""
import math
import re

from .common import est_tokens, now, sha256_text
from .prechew import HEADING, MDLINK, WIKILINK

SCHEMA = "book_pipeline.shards.v1"
HEAT_SCHEMA = "book_pipeline.heatmap.v1"
DIMS = ["log_tokens", "hash_norm", "log_headings", "log_links", "log_technical"]


def _cuts(lines, max_tokens):
    """Line indexes (0-based, exclusive ends) that split `lines` into pieces of <= max_tokens where possible."""
    pieces, start = [], 0
    heads = [i for i, ln in enumerate(lines) if HEADING.match(ln)] + [len(lines)]
    for h in heads:
        if h <= start:
            continue
        seg = lines[start:h]
        if est_tokens("\n".join(seg)) <= max_tokens:
            pieces.append((start, h))
        else:  # still too big between headings: break at blank lines
            s, acc = start, 0
            for i in range(start, h):
                acc += len(lines[i]) // 4 + 1
                if acc >= max_tokens and not lines[i].strip():
                    pieces.append((s, i + 1)); s, acc = i + 1, 0
            if s < h:
                pieces.append((s, h))
        start = h
    # merge slivers forward so headings-only pieces don't become shards
    merged = []
    for a, b in pieces:
        if merged and est_tokens("\n".join(lines[merged[-1][0]:b])) <= max_tokens and b - a < 4:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def fingerprint(body: str, sha: str) -> list:
    lines = body.split("\n")
    heads = sum(1 for ln in lines if HEADING.match(ln))
    links = len(WIKILINK.findall(body)) + len(MDLINK.findall(body))
    tech = body.count("```") // 2 + sum(1 for ln in lines if ln.lstrip().startswith("|"))
    return [round(math.log1p(est_tokens(body)), 5), (int(sha[:8], 16) % 1000) / 1000.0,
            round(math.log1p(heads), 5), round(math.log1p(links), 5), round(math.log1p(tech), 5)]


def build(artifact: dict, full_text: str, max_tokens: int = 2000) -> dict:
    ft = full_text.split("\n")
    shards = []
    for ci, ch in enumerate(artifact["chapters"]):
        base = ch["full_text_line_offset"]
        lines = ft[base + ch["line_start"] - 1: base + ch["line_end"]]
        cuts = [(0, len(lines))] if ch["tokens"] <= max_tokens else _cuts(lines, max_tokens)
        for si, (a, b) in enumerate(cuts):
            body = "\n".join(lines[a:b])
            if not body.strip():
                continue
            title = next((HEADING.match(ln).group(2) for ln in lines[a:b] if HEADING.match(ln)), ch["title"])
            sha = sha256_text(body)
            shards.append({
                "id": f"c{ci:03d}s{si:03d}",
                "chapter": ch["title"],
                "title": title,
                "source": ch["source"],
                "full_text_lines": [base + ch["line_start"] + a, base + ch["line_start"] + b - 1],
                "tokens": est_tokens(body),
                "sha256": sha,
                "fingerprint_raw": fingerprint(body, sha),
            })
    return {"schema": SCHEMA, "label": artifact["label"], "created": now(), "max_tokens": max_tokens,
            "dims": DIMS, "text": artifact["text"], "shards": shards}


def heatmap(shard_doc: dict, k: int = 4) -> dict:
    pts = [s["fingerprint_raw"] for s in shard_doc["shards"]]
    n, d = len(pts), len(DIMS)
    if n == 0:
        return {"schema": HEAT_SCHEMA, "label": shard_doc["label"], "points": []}
    lo = [min(p[j] for p in pts) for j in range(d)]
    hi = [max(p[j] for p in pts) for j in range(d)]
    norm = [[(p[j] - lo[j]) / (hi[j] - lo[j]) if hi[j] - lo[j] > 1e-8 else 0.0 for j in range(d)] for p in pts]
    # hash_norm is identity, not structure: it keeps duplicates apart but is left out of distance and heat
    use = [j for j in range(d) if DIMS[j] != "hash_norm"]
    cen = [sum(v[j] for v in norm) / n for j in range(d)]
    dist = lambda a, b: math.sqrt(sum((a[j] - b[j]) ** 2 for j in use))
    out = []
    for i, (s, v) in enumerate(zip(shard_doc["shards"], norm)):
        nn = sorted((dist(v, w), j) for j, w in enumerate(norm) if j != i)[:k]
        out.append({
            "id": s["id"], "title": s["title"], "chapter": s["chapter"], "source": s["source"],
            "full_text_lines": s["full_text_lines"], "tokens": s["tokens"],
            "fingerprint_norm": [round(x, 5) for x in v],
            "heat": round(sum(abs(v[j]) for j in use), 5),
            "shatter": round(dist(v, cen), 5),
            "neighbours": [shard_doc["shards"][j]["id"] for _, j in nn],
        })
    sh = sorted(p["shatter"] for p in out)
    return {"schema": HEAT_SCHEMA, "label": shard_doc["label"], "created": now(), "dims": DIMS,
            "metric": {"heat": "manhattan sum|v| over structural dims", "shatter": "euclidean distance from centroid"},
            "centroid": [round(x, 5) for x in cen], "shatter_median": sh[len(sh) // 2], "points": out}
