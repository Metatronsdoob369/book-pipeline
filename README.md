# book-pipeline

**One repo: `github.com/Metatronsdoob369/book-pipeline` (public).** Every machine clones this; no local-only copies.
Built on the 5820 from the Hive hub's description, because the Mac's original (`/Users/joewales/NODE_OUT_Master/book-pipeline`)
was never on GitHub and the Mac isn't reachable from the 5820. **Mac: merge your tree in here**
(`git remote add origin … && git pull origin master --allow-unrelated-histories`) so DNA, the XML/NAUPA profiles and
their tests live in the same repo. Until then this repo is the extract → prechew → skill → shard path only.

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
TriadGAT pass runs here too with `--eve` (after `--shard`); the Qdrant push stays on the Mac.

## eve (`--eve`)

`pipeline/eve_pass.py` mirrors `geo_rag_ingest.py`: K-NN graph over the normalized fingerprints → `TriadGATGraphRAG`
→ per-shard `gat_heat` / `gat_shatter` / `rag_retrieved` and a corpus `gsi_score`, written into the heat map JSON.
eve itself is **not in this repo** — it is pinned locally at `~/.local/share/eve/eve_v1.py` (provenance in
`SOURCE.txt` there; never copy that file or its gist id here) and runs under `~/.local/share/eve-venv`
(CPU torch + torch_geometric). Outputs record only eve's sha256.

eve needs the 2026-10-12 `diffusion_lock` fix (before it, every corpus where d ≠ N crashed past t=0).
Flyover (60 shards): GSI 0.748, GAT heat tracks fingerprint heat at r = 0.96 (untrained GAT — expected).
