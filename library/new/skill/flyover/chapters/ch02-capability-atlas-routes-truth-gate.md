# Chapter 2: Capability Atlas — primitives, routes, and the truth gate

**Source:** `Capability Atlas.md` L2–56 (written 2026-10-07; status lines L49–56 are dated and not reproduced as fact)

## Core Idea
Stop using tools "by their front door": map what each one unlocks in combination, and keep several routes to the shot depending on the data a site has. Every route is sellable only if it passes the truth gate.

## Frameworks Introduced
- **The one rule** (L6): "shape comes from measurement, look comes from photos or generation, and a check proves the look never moved the shape." Doctrine source: `DOCTRINE.md` in the flyover repo — "measured skeleton, generated skin" (L4).
- **Primitives** (L8–27), as verb → tool → verdict:
  | Primitive | Tool | Verdict |
  |---|---|---|
  | MEASURE | `engine/ept_fetch.py`, `lidar_skeleton.py` (lat/lon → USGS lidar → watertight parts, DEM+NAIP terrain) | use |
  | MEASURE | `engine/house_hero.py` + facade spec JSON (lidar + measured drawing + photos → watertight hero) | use; "new house = new spec" |
  | FRAME | `engine/geodesy.py`, `engine/frames_bridge.py` (site UTM ↔ WGS84 ↔ ENU, round-trip 0.0 cm) | use |
  | POSE | COLMAP 4.2 CUDA, `align_sfm_to_lidar.py`, `photo_overlay.py` | use for tower/oil house; house blocked by symmetry (B13) |
  | CAMERA | `flyover-pipeline/3_generate_trajectory.py`, `engine/gt_build.py`, `engine/route_a_prep.py reveal_rise` | use — synthetic moves without Earth Studio |
  | RENDER | `engine/guide_passes_blender.py` → per-frame depth, object ID, normals (EXR) | use — "the control signal that locks generation to measured geometry" |
  | RENDER | `tools/render_hero_blender.py`, UE 5.8 `tools/ue_remote/*` | use; MRQ not enabled in Flyover_UE5 (as of 2026-10-07) |
  | GENERATE video, locked | Wan2.2-Fun-5B-Control in ComfyUI, `engine/route_a_wan.py` | **use — Route A** (Apache-2.0, 8 GB with fp8 + offload) |
  | GENERATE image | ComfyUI SDXL + ControlNet Union ProMax, controlnet_aux | use for seams/frames, texture plates |
  | GENERATE world | World Labs Marble (`flyover-pipeline/2_generate_splat.py`) | **use-for-surroundings** only |
  | GENERATE video, free-form | FAL endpoints, Grok Imagine | use-with-gate; spend needs Commander's go |
  | RECONSTRUCT splat | real-photo Gaussian splat (gsplat or Brush — to verify) | Route B — to verify |
  | SEGMENT/TRACK | SAM 2, EdgeTAM | **use — the truth gate**; separate venvs (both packages named `sam2`) |
  | CHECK | `engine/acceptance_check.py` (SegFormer ADE20K), `gen_qa.py`, `verify_*` → HELD/DRIFTED/HALLUCINATED | use (origin default is ONSC — make it an arg) |
  | SELECT | best-of-N (own ~20 lines; vendored repo is CC BY-NC → idea only) | use; oracle@N vs pass@1 tells "more samples" vs "better generator" |
  | SURFACE | PlaneToPBR stack (GPL-3) | use-later (skin polish) |
- **Routes to the shot, by data available** (L35–41):
  | Site data | Route | How |
  |---|---|---|
  | Rich — lidar + measured drawings + many photos | **A + B**, C for surroundings | A: measured depth along the path → Wan Fun-Control with a real photo as look. B: real-photo splat along the same path. Both gated. |
  | Medium — lidar/footprint + a few photos | **A** | lidar skeleton is enough geometry for the control video |
  | Thin — one or two photos, no lidar | **D** (+ C) | image-to-video or Marble; truth gate against whatever geometry exists (parcel footprint + height) |
- **The truth gate** (L43–47), steps:
  1. Render the building silhouette at each frame's camera (`guide_passes_blender.py` IndexOB).
  2. SAM 2 image predictor refines it on the AI frame (`predict(box, points, mask_input=±10 logits)`) → seed the video predictor (`add_new_mask`) → `propagate_in_video` with CPU offload.
  3. Per frame: IoU and boundary-F vs the silhouette, presence score, Depth Anything depth inside the matte vs rendered depth.
  4. Best-of-N with a margin; composite the measured render inside the matte where a clip drifts.

## Key Concepts
- **Route A**: measured depth video + real reference photo → Wan2.2 Fun-Control → geometry-locked photoreal clip.
- **Route B**: real-photo Gaussian splat rendered along the same path (to verify).
- **Route C**: Marble world for surroundings. **Route D**: free-form image-to-video, gated.
- **HELD / DRIFTED / HALLUCINATED**: truth-gate verdicts.
- **Best-of-N with margin**: generate N, score, pick only if the winner clears by a margin.

## Mental Models
- Pick the route from the **data the site has**, not from the tool you like.
- Use the generator for look only; geometry always arrives as a control signal.
- Use SAM seeded from your *own rendered silhouette* as a drift meter; re-prompt only where it drifts.

## Anti-patterns (blocked/demoted, L29–33)
- **SAM 3D Objects**: single objects, ≥24–32 GB VRAM — props only, rented GPU only. (SAM 3 = segmentation, not 3D.)
- **Difix3D+, Lyra**: non-commercial licenses. **HunyuanWorld-Voyager, Uni3C**: 50–60 GB VRAM. **3DGS-Enhancer**: no license.
- **Old scripts with `/Users/joewales` or ONSC hard-codes** (`render_flight_test.py`, `render_splat_*`, `generate_trellis*`, `test_infinisplat.py`): stale until parameterized.
- Using Marble for the hero: it is surroundings only (no refine/upscale).

## Key Takeaways
1. Shape from measurement, look from photos/generation, and a check proving the look never moved the shape.
2. Choose route A/B/C/D by site data richness.
3. No clip is sellable without the truth gate (silhouette → SAM 2 → per-frame IoU/boundary-F/depth).
4. Check licenses and VRAM before adopting a model; non-commercial = idea only.

## Connects To
- **ch03**: the working Route A pipeline and its rules.
- **ch04**: truth-gate pixel floor (Shot Maker lessons).
- **ch08**: why generation must be structure-locked (capability assessment).
