"""Shared paths and helpers for the bench book-pipeline. Stdlib only."""
import datetime as dt
import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = ROOT / "library"
CONVERTER = Path(os.environ.get("BOOK_TO_SKILL_ROOT", "")) if os.environ.get("BOOK_TO_SKILL_ROOT") else None
if CONVERTER is None:
    for cand in (Path.home() / ".claude/skills/book-to-skill", Path.home() / ".agents/skills/book-to-skill"):
        if (cand / "scripts/extract.py").is_file():
            CONVERTER = cand.resolve()
            break
CONVERTER_PY = Path(os.environ.get("BOOK_TO_SKILL_PYTHON", Path.home() / ".local/share/book-to-skill-venv/bin/python3"))
SKILLS_HOME = Path.home() / ".agents/skills"          # one physical copy per generated skill
CLAUDE_SKILLS = Path.home() / ".claude/skills"         # Claude Code discovers it through a symlink


def lane_dir(lane: str) -> Path:
    d = LIBRARY / lane
    for sub in ("inbox", "artifacts", "logs", "skill", "shards", "heatmaps"):
        (d / sub).mkdir(parents=True, exist_ok=True)
    (LIBRARY / "human").mkdir(parents=True, exist_ok=True)
    return d


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "untitled"


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", "replace")).hexdigest()


def est_tokens(s: str) -> int:
    return (len(s) + 3) // 4


def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def write_json(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)
    return path


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
