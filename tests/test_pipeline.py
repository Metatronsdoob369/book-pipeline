"""Stdlib tests: python3 -m unittest discover -s tests (from the repo root). The converter is not needed here."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pipeline import prechew, shard  # noqa: E402
from pipeline.extract import split_sources  # noqa: E402

BAR = "=" * 80
DOC_A = "# Alpha\n\nAlpha lead sentence that is long enough.\n\n## One\ntext [[Beta]] 2026-10-01\n\n## Two\n```\n# not a heading\n```\n"
DOC_B = "# Beta\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\nSee [x](http://e.x) 2026-10-12\n"
FULL = f"{BAR}\nSOURCE: a.md (Path: /r/a.md)\n{BAR}\n{DOC_A}\n{BAR}\nSOURCE: b.md (Path: /r/sub/b.md)\n{BAR}\n{DOC_B}"
META = {"sources": [{"source_file": "/r/a.md", "sha256": "a" * 64, "format": "md"},
                    {"source_file": "/r/sub/b.md", "sha256": "b" * 64, "format": "md"}]}


class Pipeline(unittest.TestCase):
    def setUp(self):
        self.art = prechew.build("t", "new", META, FULL, Path("/x/full_text.txt"), ["/r"])

    def test_split_offsets_point_into_full_text(self):
        ft = FULL.split("\n")
        for path, text, off in split_sources(FULL):
            self.assertEqual(ft[off], text.split("\n")[0])

    def test_one_chapter_per_source_and_spectral_fields(self):
        a = self.art
        self.assertEqual([c["source"] for c in a["chapters"]], ["a.md", "sub/b.md"])
        self.assertEqual(a["totals"]["chapters_total"], 2)
        self.assertEqual(len(a["source"]["sha256"]), 64)
        self.assertIn("tokens", a["totals"])

    def test_headings_skip_code_fences_and_resolve(self):
        ft = FULL.split("\n")
        a = self.art["chapters"][0]
        self.assertEqual([h["title"] for h in a["headings"]], ["Alpha", "One", "Two"])
        for h in a["headings"]:
            self.assertIn(h["title"], ft[a["full_text_line_offset"] + a["line_start"] - 1 + h["line"] - 1])

    def test_links_dates_tables(self):
        a, b = self.art["chapters"]
        self.assertEqual(a["wikilinks"], ["Beta"])
        self.assertEqual(a["dates"]["first"], "2026-10-01")
        self.assertEqual(b["table_rows"], 3)
        self.assertEqual(b["links"], ["http://e.x"])

    def test_single_source_splits_at_repeated_heading_level(self):
        art = prechew.build("s", "new", {"source_file": "/r/a.md", "sha256": "c" * 64}, DOC_A, Path("/x"), ["/r/a.md"])
        self.assertEqual([c["title"] for c in art["chapters"]], ["(front matter)", "One", "Two"])

    def test_shards_cover_and_cap(self):
        big = "# Big\n" + "\n\n".join(f"## S{i}\n" + ("word " * 400) for i in range(10))
        art = prechew.build("b", "new", {"source_file": "/r/big.md", "sha256": "d" * 64}, big, Path("/x"), ["/r/big.md"])
        sd = shard.build(art, big, max_tokens=600)
        self.assertGreater(len(sd["shards"]), 5)
        self.assertTrue(all(s["tokens"] <= 700 for s in sd["shards"]))
        self.assertTrue(all(len(s["fingerprint_raw"]) == 5 for s in sd["shards"]))
        hm = shard.heatmap(sd)
        self.assertEqual(len(hm["points"]), len(sd["shards"]))
        self.assertTrue(all(0 <= v <= 1 for p in hm["points"] for v in p["fingerprint_norm"]))

    def test_fingerprint_is_deterministic(self):
        self.assertEqual(shard.fingerprint(DOC_A, "f" * 64), shard.fingerprint(DOC_A, "f" * 64))


if __name__ == "__main__":
    unittest.main()
