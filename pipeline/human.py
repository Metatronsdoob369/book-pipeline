"""Human view — library/human/<label>.html: collapsible outline of the artifact, plus the heat map as an SVG
scatter when shards exist (x = size, y = structure, colour = heat, ring = shatter). Self-contained, no scripts."""
import html
import math

from .common import LIBRARY

E = html.escape


def _scatter(heat: dict) -> str:
    pts = heat.get("points") or []
    if not pts:
        return ""
    W, H, P = 900, 520, 40
    dims = heat["dims"]
    xi, yi = dims.index("log_tokens"), [dims.index("log_headings"), dims.index("log_links"), dims.index("log_technical")]
    hmax = max(p["heat"] for p in pts) or 1
    smed = heat.get("shatter_median") or 0
    dots = []
    for p in pts:
        v = p["fingerprint_norm"]
        x = P + v[xi] * (W - 2 * P)
        y = H - P - (sum(v[j] for j in yi) / 3) * (H - 2 * P)
        t = p["heat"] / hmax
        col = f"hsl({int(220 - 210 * t)},85%,{int(45 + 10 * t)}%)"
        r = 4 + 3 * math.sqrt(p["tokens"] / 500)
        ring = ' stroke="#fff" stroke-width="1.5"' if p["shatter"] > 2 * smed else ""
        tip = f'{p["title"]} — {p["source"]} L{p["full_text_lines"][0]}-{p["full_text_lines"][1]} · heat {p["heat"]} · shatter {p["shatter"]}'
        if "gat_heat" in p:
            tip += f' · GAT heat {p["gat_heat"]} · GAT shatter {p["gat_shatter"]}' + (" · RAG hit" if p["rag_retrieved"] else "")
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{min(r, 16):.1f}" fill="{col}" fill-opacity=".8"{ring}><title>{E(tip)}</title></circle>')
    ev = heat.get("eve")
    eve_line = (f'<p class="m">eve TriadGAT: {ev["nodes"]} nodes · {ev["edges"]} edges · GSI {ev["gsi_score"]} · '
                f'{ev["retrieval_hits"]} RAG hits (untrained GAT — relational context; fingerprint heat is primary)</p>') if ev else ""
    return (f'<h2>Heat map — {len(pts)} shards</h2>{eve_line}<p class="m">x = size · y = structure (headings, links, tables/code) · '
            f'colour = heat (blue cold → red hot) · white ring = shatter &gt; 2× median (outliers). Hover a dot.</p>'
            f'<svg viewBox="0 0 {W} {H}" role="img"><rect width="{W}" height="{H}" fill="var(--panel)"/>{"".join(dots)}'
            f'<text x="{P}" y="{H - 12}" class="ax">small</text><text x="{W - P}" y="{H - 12}" class="ax" text-anchor="end">large</text>'
            f'<text x="10" y="{P}" class="ax">structured</text></svg>')


def write(artifact: dict, heat: dict | None = None) -> str:
    t = artifact["totals"]
    rows = []
    for ch in artifact["chapters"]:
        heads = "".join(f'<li style="margin-left:{(h["level"] - 1) * 14}px">{E(h["title"])} <span class="m">L{h["line"]}</span></li>'
                        for h in ch["headings"][:80])
        links = ", ".join(E(w) for w in ch["wikilinks"][:20])
        dates = f'{ch["dates"]["first"]} → {ch["dates"]["last"]}' if ch["dates"] else ""
        rows.append(
            f'<details><summary><b>{E(ch["title"])}</b> <span class="m">{ch["tokens"]} tok · {len(ch["headings"])} headings'
            f'{" · " + dates if dates else ""}</span></summary><div class="b"><p>{E(ch["lead"])}</p>'
            f'<p class="m">terms: {E(", ".join(ch["terms"]))}</p>{"<p class=m>links: " + links + "</p>" if links else ""}'
            f'<ul>{heads}</ul></div></details>')
    page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(artifact["label"])} — prechew</title><style>
:root{{--bg:#0f1115;--panel:#171a21;--fg:#e6e6e6;--mute:#8b93a1;--line:#2a2f3a}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0;padding:16px;max-width:980px;margin:auto}}
details{{border:1px solid var(--line);border-radius:8px;margin:6px 0;background:var(--panel)}}summary{{cursor:pointer;padding:8px 12px}}
.b{{padding:0 14px 10px}}.m{{color:var(--mute);font-size:13px}}ul{{list-style:none;padding:0}}svg{{width:100%;height:auto;border-radius:8px}}
.ax{{fill:var(--mute);font-size:12px}}</style></head><body>
<h1>{E(artifact["label"])}</h1><p class="m">{t["files_total"]} files · {t["chapters_total"]} chapters · {t["sections_total"]} sections ·
~{t["tokens"]} tokens · {t["wikilinks_total"]} wikilinks · lane {E(artifact["lane"])} · {E(artifact["created"])}</p>
<p class="m">top terms: {E(", ".join(artifact["terms"]))}</p>
{_scatter(heat) if heat else ""}<h2>Outline</h2>{"".join(rows)}</body></html>"""
    out = LIBRARY / "human" / f'{artifact["label"]}.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return str(out)
