#!/usr/bin/env python3
"""Bench book-pipeline (5820 / machinist). Same call shape as the Mac's library/run_pipeline.py.

  python3 library/run_pipeline.py --src <file|dir|glob> [--src ...] --label <slug> [--skip-dna] [--to-skill] [--shard]
  python3 library/run_pipeline.py install --label <slug>      # after the agent finishes the skill
  python3 library/run_pipeline.py status                      # what is in the library

Ladder on the bench:  source -> extract (converter) -> prechew artifact -> human view
                                                      \\-> book-to-skill handoff -> agent SKILL.md -> install
                                                      \\-> shard -> heat map (spectral-terrain fingerprint lineage) -> eve GAT (--eve)
DNA / apply / hinge stay on the Mac; --skip-dna is accepted so Mac commands paste unchanged.
Lane: --lane, else BOOK_PIPELINE_LIBRARY_LANE, else "new".
"""
import argparse
import glob
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import extract, human, prechew, shard, to_skill  # noqa: E402
from pipeline.common import LIBRARY, lane_dir, now, read_json, sha256_text, slugify, write_json  # noqa: E402


def expand(srcs):
    out = []
    for s in srcs:
        s = os.path.expanduser(s)
        hits = glob.glob(s) if any(c in s for c in "*?[") else [s]
        if not hits or not all(Path(h).exists() for h in hits):
            raise SystemExit(f"source not found: {s}")
        out += [str(Path(h).resolve()) for h in hits]
    return out


def run(a):
    label = slugify(a.label)
    lane = lane_dir(a.lane)
    srcs = expand(a.src)
    log = lane / "logs" / f"run-{label}"
    print(f"[1/4] extract  {len(srcs)} path(s) -> {log / 'extract'}")
    meta = extract.run(srcs, log / "extract", a.mode)
    full = (log / "extract" / "full_text.txt").read_text(encoding="utf-8")
    write_json(lane / "inbox" / f"{label}.sources.json", {
        "label": label, "created": now(), "paths": srcs,
        "files": [{"path": s.get("source_file"), "sha256": s.get("sha256")} for s in meta.get("sources") or [meta]]})

    art = prechew.build(label, a.lane, meta, full, log / "extract" / "full_text.txt", srcs)
    art_path = write_json(lane / "artifacts" / f"{label}.auto.artifact.json", art)
    t = art["totals"]
    print(f"[2/4] prechew  {t['files_total']} files, {t['chapters_total']} chapters, ~{t['tokens']} tok "
          f"-> {art_path.name} ({art_path.stat().st_size // 1024} KB vs {len(full.encode()) // 1024} KB text)")

    heat = None
    if a.shard:
        sd = shard.build(art, full, a.max_shard_tokens)
        write_json(lane / "shards" / f"{label}.shards.json", sd)
        heat = shard.heatmap(sd)
        write_json(lane / "heatmaps" / f"{label}.heatmap.json", heat)
        hot = sorted(heat["points"], key=lambda p: -p["heat"])[:3]
        print(f"[3/4] shard    {len(sd['shards'])} shards (cap {a.max_shard_tokens} tok) -> heat map; hottest: "
              + "; ".join(f"{p['title'][:40]} ({p['heat']})" for p in hot))
        if a.eve:
            import subprocess
            from pipeline.eve_pass import EVE_PYTHON
            hp = lane / "heatmaps" / f"{label}.heatmap.json"
            r = subprocess.run([str(EVE_PYTHON), str(Path(__file__).resolve().parent.parent / "pipeline/eve_pass.py"), str(hp)],
                               capture_output=True, text=True)
            if r.returncode:
                raise SystemExit("eve pass failed:\n" + r.stderr[-2000:])
            print("      " + r.stdout.strip().splitlines()[-1])
            heat = read_json(hp)
    else:
        print("[3/4] shard    skipped (--shard to enable)")

    if a.to_skill:
        h = to_skill.handoff(lane, label, label, log / "extract", art_path, meta)
        print(f"[4/4] to-skill handoff -> {h}  ({read_json(h)['mode']}); agent finishes converter Steps 3-9")
    else:
        print("[4/4] to-skill skipped (--to-skill to enable)")
    print(f"      human view -> {human.write(art, heat)}")


def status(a):
    for lane in sorted(p for p in LIBRARY.iterdir() if p.is_dir() and p.name != "human"):
        print(f"lane {lane.name}")
        for art in sorted((lane / "artifacts").glob("*.auto.artifact.json")):
            j = read_json(art)
            label = j["label"]
            sk = lane / "skill" / label
            flags = ["shards" if (lane / "shards" / f"{label}.shards.json").exists() else "",
                     "handoff" if (lane / "logs" / f"book-to-skill-{label}" / "handoff.json").exists() else "",
                     "SKILL.md" if (sk / "SKILL.md").exists() else "",
                     "installed" if (Path.home() / ".agents/skills" / label).is_symlink() else ""]
            print(f"  {label:32s} {j['totals']['chapters_total']:4d} ch ~{j['totals']['tokens']:7d} tok  "
                  + " ".join(f for f in flags if f))


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("install", "status"):
        p = argparse.ArgumentParser()
        p.add_argument("cmd"); p.add_argument("--label"); p.add_argument("--lane", default=os.environ.get("BOOK_PIPELINE_LIBRARY_LANE", "new"))
        a = p.parse_args()
        if a.cmd == "status":
            return status(a)
        for line in to_skill.install(lane_dir(a.lane), slugify(a.label)):
            print("linked", line)
        return
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--src", action="append", required=True)
    p.add_argument("--label", required=True)
    p.add_argument("--lane", default=os.environ.get("BOOK_PIPELINE_LIBRARY_LANE", "new"))
    p.add_argument("--mode", choices=["text", "technical"], default="text")
    p.add_argument("--skip-dna", action="store_true", help="accepted for Mac parity; DNA is not on the bench")
    p.add_argument("--to-skill", action="store_true")
    p.add_argument("--shard", action="store_true")
    p.add_argument("--max-shard-tokens", type=int, default=2000)
    p.add_argument("--eve", action="store_true", help="after --shard: TriadGATGraphRAG pass (needs ~/.local/share/eve + eve-venv)")
    run(p.parse_args())


if __name__ == "__main__":
    main()
