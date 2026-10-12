"""Stage 3 — the middle fork: book-to-skill. The deterministic half is done here (extract already ran; its output is
mirrored next to the skill, and a handoff.json says what the agent must finish). The agent then completes the
converter's SKILL.md Steps 3–9 inside library/<lane>/skill/<slug>/ — frameworks, principles, techniques and
anti-patterns taken from the text, never invented. `install` links the finished skill where agents look.
"""
import shutil
import subprocess
from pathlib import Path

from .common import CLAUDE_SKILLS, CONVERTER, SKILLS_HOME, now, write_json

SCHEMA = "book_pipeline.skill_handoff.v1"


def _converter_commit():
    if CONVERTER is None:
        return None
    r = subprocess.run(["git", "-C", str(CONVERTER), "rev-parse", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() or None


def handoff(lane_root: Path, slug: str, label: str, extract_dir: Path, artifact_path: Path, meta: dict) -> Path:
    skill_dir = lane_root / "skill" / slug
    mirror = skill_dir / "_extract"
    mirror.mkdir(parents=True, exist_ok=True)
    for f in ("full_text.txt", "metadata.json"):
        shutil.copy2(extract_dir / f, mirror / f)
    existing = (skill_dir / "SKILL.md").is_file()
    return write_json(lane_root / "logs" / f"book-to-skill-{slug}" / "handoff.json", {
        "schema": SCHEMA,
        "created": now(),
        "label": label,
        "slug": slug,
        "mode": "update-fold-in" if existing else "full-conversion",
        "converter": {"root": str(CONVERTER), "commit": _converter_commit(), "instructions": str(CONVERTER / "SKILL.md")},
        "artifact": str(artifact_path),
        "extract": {"full_text": str(mirror / "full_text.txt"), "metadata": str(mirror / "metadata.json"),
                    "tokens": meta.get("estimated_tokens"), "sources": meta.get("total_sources", 1)},
        "skill_dir": str(skill_dir),
        "install_to": str(SKILLS_HOME / slug),
        "agent_next": [
            "Read the artifact first; pull only the line ranges you need from extract.full_text.",
            "Follow converter SKILL.md Steps 3-9 (Mode 4 Update/Fold-in if mode says so) writing into skill_dir.",
            "Extract structure, not summaries. Name only frameworks the text names; cite chapter + lines.",
            f"Then: python3 library/run_pipeline.py install --label {label}",
        ],
    })


def install(lane_root: Path, slug: str) -> list:
    skill_dir = (lane_root / "skill" / slug).resolve()
    if not (skill_dir / "SKILL.md").is_file():
        raise SystemExit(f"{skill_dir}/SKILL.md missing — the agent half (converter Steps 3-9) has not run yet")
    done = []
    for link, target in ((SKILLS_HOME / slug, skill_dir), (CLAUDE_SKILLS / slug, SKILLS_HOME / slug)):
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink() or not link.exists():
            if link.is_symlink():
                link.unlink()
            link.symlink_to(target)
            done.append(f"{link} -> {target}")
        elif link.resolve() != Path(target).resolve():
            raise SystemExit(f"{link} exists and is not ours — refusing to overwrite")
    return done
