"""Stage 2 — prechew. Extracted text -> one uniform `<label>.auto.artifact.json` per run.

The artifact is metadata, not text: per chapter it keeps the heading outline with line offsets, hashes, links,
dates, top terms and a one-line lead. An agent reads the artifact to decide WHERE to look, then pulls only that
line range from logs/<run>/extract/full_text.txt. Field names `source.sha256`, `totals.tokens` and
`totals.chapters_total` match what spectral-terrain's structural fingerprint reads (scripts/geo_rag_ingest.py).
"""
import collections
import os
import re
from pathlib import Path

from .common import est_tokens, now, sha256_text
from .extract import split_sources

SCHEMA = "book_pipeline.prechew.v1"
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"\]\(([^)\s]+)\)")
DATE = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")
WORD = re.compile(r"[A-Za-z][A-Za-z0-9_\-]{2,}")
STOP = set("""the and for that this with from are was were not but you your our its it's into onto than then them they
there their what when where which who will would can could should has have had been being does did done just only
also more most less very any all each per via out off one two use used using get got make made like same new now
here about over under after before because while still yet too why how ago let lets don't isn't it’s""".split())


def _outline(lines):
    out, fence = [], False
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        m = None if fence else HEADING.match(ln)
        if m:
            out.append({"level": len(m.group(1)), "title": m.group(2).strip(), "line": i})
    return out


def _lead(lines):
    for ln in lines:
        s = ln.strip().lstrip("-*> ").strip()
        if s and not s.startswith(("#", "```", "|", "---", "<")) and len(s) > 20:
            return s[:240]
    return ""


def _terms(text, k=12):
    c = collections.Counter(w.lower() for w in WORD.findall(text))
    return [w for w, _ in c.most_common(80) if w not in STOP and not w.isdigit()][:k]


def _chapter(title, src, sha, lines, start, end, offset):
    body = "\n".join(lines[start - 1:end])
    dates = sorted(set(DATE.findall(body)))
    return {
        "title": title,
        "source": src,
        "source_sha256": sha,
        "line_start": start,
        "line_end": end,
        "full_text_line_offset": offset,   # read full_text.txt lines offset+line_start .. offset+line_end
        "tokens": est_tokens(body),
        "words": len(body.split()),
        "sha256": sha256_text(body),
        "lead": _lead(lines[start - 1:end]),
        "headings": [h for h in _outline(lines[start - 1:end])],
        "wikilinks": sorted(set(m.strip() for m in WIKILINK.findall(body))),
        "links": sorted(set(MDLINK.findall(body)))[:50],
        "dates": {"first": dates[0], "last": dates[-1], "count": len(dates)} if dates else None,
        "code_blocks": body.count("```") // 2,
        "table_rows": sum(1 for ln in lines[start - 1:end] if ln.lstrip().startswith("|")),
        "terms": _terms(body),
    }


def build(label: str, lane: str, meta: dict, full_text: str, text_path: Path, roots) -> dict:
    by_path = {s.get("source_file"): s for s in meta.get("sources", [])} or {meta.get("source_file"): meta}
    common_root = os.path.commonpath([str(Path(r).resolve()) for r in roots]) if roots else ""
    if Path(common_root).is_file():
        common_root = str(Path(common_root).parent)
    blocks = list(split_sources(full_text))
    chapters = []
    for path, text, offset in blocks:
        path = path or meta.get("source_file")
        src_meta = by_path.get(path, {})
        rel = os.path.relpath(path, common_root) if path and common_root else (path or label)
        lines = text.split("\n")
        if len(blocks) > 1:
            # many sources: one chapter per source, its headings are the sections
            chapters.append(_chapter(rel, rel, src_meta.get("sha256"), lines, 1, len(lines), offset))
            continue
        # one source: split at the shallowest heading level that occurs more than once
        outline = _outline(lines)
        levels = collections.Counter(h["level"] for h in outline)
        cut = min((lv for lv, n in levels.items() if n > 1), default=None)
        marks = [h for h in outline if h["level"] == cut] if cut else []
        if not marks:
            chapters.append(_chapter(rel, rel, src_meta.get("sha256"), lines, 1, len(lines), offset))
            continue
        if marks[0]["line"] > 1:
            marks.insert(0, {"title": "(front matter)", "line": 1})
        for i, h in enumerate(marks):
            end = marks[i + 1]["line"] - 1 if i + 1 < len(marks) else len(lines)
            chapters.append(_chapter(h["title"], rel, src_meta.get("sha256"), lines, h["line"], end, offset))

    combined = "".join(s["sha256"] or "" for s in meta.get("sources", [])) or sha256_text(full_text)
    sources = meta.get("sources") or [meta]
    return {
        "schema": SCHEMA,
        "label": label,
        "lane": lane,
        "created": now(),
        "source": {
            "kind": "multi" if len(sources) > 1 else sources[0].get("format"),
            "root": common_root,
            "sha256": sha256_text(combined),
            "files": [{"path": os.path.relpath(s.get("source_file", ""), common_root) if common_root else s.get("source_file"),
                       "sha256": s.get("sha256"), "format": s.get("format"), "method": s.get("extraction_method"),
                       "tokens": s.get("estimated_tokens")} for s in sources],
        },
        "text": {"path": str(text_path), "sha256": sha256_text(full_text)},
        "totals": {
            "tokens": sum(c["tokens"] for c in chapters),
            "words": sum(c["words"] for c in chapters),
            "chapters_total": len(chapters),
            "sections_total": sum(len(c["headings"]) for c in chapters),
            "wikilinks_total": sum(len(c["wikilinks"]) for c in chapters),
            "files_total": len(sources),
        },
        "terms": _terms(full_text, 25),
        "chapters": chapters,
    }
