"""Stage 1 — extract. Every source format goes through the book-to-skill converter's deterministic extractor,
so prechew sees one shape: full_text.txt with SOURCE: boundaries + metadata.json with a sha256 per source."""
import os
import re
import subprocess
from pathlib import Path

from .common import CONVERTER, CONVERTER_PY, read_json

BOUNDARY = re.compile(r"^={20,}\nSOURCE: (?P<name>.+?) \(Path: (?P<path>.+?)\)\n={20,}\n", re.M)


def run(sources, workdir: Path, mode: str = "text") -> dict:
    if CONVERTER is None:
        raise SystemExit("book-to-skill converter not found (~/.claude/skills or ~/.agents/skills, or BOOK_TO_SKILL_ROOT)")
    py = str(CONVERTER_PY) if Path(CONVERTER_PY).exists() else "python3"
    workdir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, BOOK_SKILL_WORKDIR=str(workdir))
    cmd = [py, str(CONVERTER / "scripts/extract.py"), *map(str, sources), "--mode", mode, "--install-missing", "no"]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    (workdir / "extract.log").write_text(r.stdout + r.stderr, encoding="utf-8")
    if r.returncode != 0 or not (workdir / "metadata.json").is_file():
        raise SystemExit(f"converter extract failed (exit {r.returncode}); see {workdir / 'extract.log'}")
    return read_json(workdir / "metadata.json")


def split_sources(full_text: str):
    """Yield (path, text, line_offset) per SOURCE block; line N of the block is line_offset + N of full_text.
    A single-source run has no boundary: the whole text is one block."""
    hits = list(BOUNDARY.finditer(full_text))
    if not hits:
        yield None, full_text, 0
        return
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(full_text)
        yield m.group("path"), full_text[m.end():end], full_text.count("\n", 0, m.end())
