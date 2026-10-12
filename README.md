# book-pipeline — bench (5820 / machinist)

The 5820 copy of Joe's book-pipeline (`/Users/joewales/NODE_OUT_Master/book-pipeline` on the Mac — not on GitHub,
not reachable from here). Rebuilt from the hub's description around the same public converter. Same call shape.

```text
source (file | folder | glob; pdf epub docx html md txt rtf)
  -> extract   book-to-skill converter, deterministic          library/<lane>/logs/run-<label>/extract/{full_text.txt,metadata.json}
  -> prechew   uniform artifact: metadata, not text           library/<lane>/artifacts/<label>.auto.artifact.json
     |-> human view (outline + heat map)                      library/human/<label>.html
     |-> book-to-skill handoff  (--to-skill)                  library/<lane>/logs/book-to-skill-<label>/handoff.json
     |     agent finishes converter Steps 3-9                 library/<lane>/skill/<label>/SKILL.md ...
     |     install                                            ~/.agents/skills/<label> -> skill dir
     |                                                        ~/.claude/skills/<label> -> ~/.agents/skills/<label>
     \-> shard + heat map  (--shard)                          library/<lane>/shards/<label>.shards.json
                                                              library/<lane>/heatmaps/<label>.heatmap.json
DNA / apply / hinge: Mac only (--skip-dna accepted for parity).
```

## Run

```bash
cd ~/bench/book-pipeline
python3 library/run_pipeline.py --src ~/Hive/10-Projects/flyover --label flyover --skip-dna --to-skill --shard
python3 library/run_pipeline.py install --label flyover     # after SKILL.md exists
python3 library/run_pipeline.py status
python3 -m unittest discover -s tests
```

Re-running a label whose skill already has `SKILL.md` writes a handoff in **update-fold-in** mode (converter Mode 4):
new sources merge into the existing skill instead of replacing it. That is how a library grows.

## Where things live

| What | Where |
|---|---|
| Converter (official `virgiliojr94/book-to-skill`, pinned `a24e62f`, 2026-10-11) | `~/.agents/skills/book-to-skill`, linked from `~/.claude/skills/book-to-skill` |
| Converter Python + extractors (html, epub, pdf, docx, rtf) | `~/.local/share/book-to-skill-venv` |
| Missing extractors | poppler `pdftotext` (sudo apt; PDFs fall back to Python), Calibre (MOBI/AZW only), docling (`--mode technical`) |
| Bench code (stdlib only) | `pipeline/` — `extract`, `prechew`, `to_skill`, `shard`, `human` |

## Why the artifact, not the file

The artifact keeps, per chapter: heading outline with line numbers, hashes, wikilinks/links, date span, top terms,
one lead line, table/code counts. An agent reads that (a fraction of the text), picks the chapter, and reads only
`full_text.txt` lines `full_text_line_offset + line_start .. + line_end`. Shards point the same way — no text copies.

## Heat map lineage (spectral-terrain)

`source.sha256`, `totals.tokens`, `totals.chapters_total` are the fields spectral-terrain's
`scripts/geo_rag_ingest.py` reads for its 3-D structural fingerprint. Shards carry a 5-D prose extension of that
fingerprint; heat = manhattan Σ|v|, shatter = euclidean distance from centroid (`engine/calibrate.ts`). The eve
TriadGAT pass and Qdrant push live on the Mac; the bench map is the deterministic half.
