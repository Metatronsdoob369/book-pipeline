# Chapter 3: Playbook — the generated-aerials pipeline, rules, heights, taste

**Source:** `Playbook — Generated Aerials.md` L2–56 (learned on Bodie Island 2026-10-07 and the Burj Khalifa stress test 2026-10-07 → 10-08). Read before touching any NoDrone shot.

## Core Idea
A local, 8 GB-GPU, no-paid-API pipeline produces geometry-locked aerial films: measured/parametric world geometry → coded camera paths → Blender guide passes → Wan2.2 Fun-Control generation → layered heals → truth gate → baked world for re-use. Every rule below "cost us a run."

## Frameworks Introduced
- **The pipeline that works** (L6–12):
  1. **World geometry** — footprints from Overture (duckdb straight from S3) → heights via `engine/city_heights.py` (provenance per building). Hero: measured (lidar/drawings) or parametric from published dimensions.
  2. **Shots** — camera paths in code; 81 frames each = 3.375 s = 8 beats at 142 BPM. Blender headless guides: depth + object ID (`guide_passes_blender.py`).
  3. **Generate** — Wan2.2 Fun-Control 5B, depth control on log-depth over a fixed per-shot range, 832×480 × 81 frames, ~3 min/shot. Same seed and prompt across shots → one look.
  4. **Heal in layers** — hero gets one fixed skin (`hero_skin_pass.py`) composited over AI frames with distance haze (`composite_hero.py`); remove elements with SAM 3 text tracking (`sam3_track.py`); lock the music first (`music_and_cut.py`, ACE-Step), then fix shots inside the locked edit.
  5. **Check** — truth gate (`truth_gate.py`, SAM 2.1): IoU of the AI building vs measured silhouette → HELD / DRIFTED / HALLUCINATED.
  6. **Keep the world** — `world_bake.py` projects every generated frame onto geometry (depth-tested, best view wins); new paths render with no new generation (`world_render.py`); low-denoise polish (`world_polish.py`).
- **Height merge order** (L26–42), from the Dubai test (3 km, 11,760 buildings): tagged `height` > `num_floors` × 3.6 m > 3D-GloBFP > 6 m default.
  | Source | Burj (828 m) read | Verdict |
  |---|---|---|
  | GHSL built-height (90 m) | 29 m | useless for towers |
  | Copernicus GLO-30 DSM | 24 m | useless for towers |
  | 3D-GloBFP | 31 m | fine for low-rise only |
  | Overture/OSM tagged `height` | covers named skyline | first choice |
  | floors × 3.6 m | — | second choice |
- **Rule: "give the generator real mass everywhere in frame, or it invents mass for you."** (L40) Adding real city mass removed a hallucinated giant "swoosh" structure.
- **Taste — the Commander's calls, all still binding** (L44–50):
  - Movement is not a bonus: 30 s or more, music, dynamic angles.
  - Build it healable: lock the edit and music, then fix elements, not whole clips.
  - One fixed skin per hero first, then global fixes.
  - OSM only *proves placement*; final imagery is crafted.
  - Accent the real details, but don't invent ones that aren't there.
  - The goal: "nail the world around a subject, and make the subject's building accurate."

## Key Concepts
- **Log-depth control over fixed range**: depth control normalised per shot so the generator sees stable mass.
- **Hero skin composite**: one fixed texture pass for the hero laid over AI frames — source of thin detail.
- **World bake**: generated pixels projected back onto geometry so new cameras need no generation.
- **Height provenance**: each building's height labelled with its source; "Label every height that wasn't measured" (L42).

## Rules (each cost a run, L14–24)
- **Reference image must match frame 0's framing** — a different-angle Burj photo gave *two Burjs*. Use `--no-ref`, or the world-rendered frame 0 as reference.
- **Depth control locks mass, not thin detail** — spires, fins, fountain jets drift into "sticks and balls"; thin detail comes from the hero skin composite.
- **Put effects in the control, not the beauty** — jets added to the depth control let the AI paint real-looking water.
- **Check the subject is in frame before you spend GPU** — print "tower in frame" per shot from the ID pass.
- **832×480 × 81 frames fits 8 GB** (fp8, ComfyUI offload). Call `/free` between shots. Run under `gpu run --vram 7000 --exclusive`.
- **SAM 3: prompt on a frame where the object is clearly visible**; gated weights need a Hugging Face login.
- **Blender 5 multilayer EXR**: `media_type = "MULTI_LAYER_IMAGE"` (old `OPEN_EXR_MULTILAYER` raises). Import glTF, then rotate roots −90° about X.
- **Never `pkill -f` / `pgrep -f` a pattern that matches your own command line.**
- **Don't subdivide whole meshes to bake** — sample surface points per group (0.5 m hero, 0.75 m city, 1 m ground).
- **curl exit 92** on HF/large downloads (HTTP/2 stream reset): resume with `--http1.1 -C -`.

## Anti-patterns
- Re-generating a whole clip to fix one element (heal the element: SAM 3 track, then fill — L39).
- Trusting raster DSM/built-height grids for towers.
- Leaving empty ground in frame for the generator to invent on.

## Key Takeaways
1. Geometry first, everywhere in frame; generator only paints.
2. Same seed + prompt across shots; lock music and edit before fixing.
3. Fix in layers (hero skin → SAM 3 removal → fill), never whole-clip regenerate.
4. Bake the world once generation is good; re-render paths from the bake.
5. Respect the 8 GB budget and run under GPU Guardian.

## Connects To
- **ch02**: routes and truth gate. **ch04**: Shot Maker pixel-floor lesson. **ch10**: GPU Guardian and machine.
