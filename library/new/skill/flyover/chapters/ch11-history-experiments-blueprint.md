# Chapter 11: Project history, early experiments, and the multi-tier blueprint

**Sources:** `_flyover-Hub.md` L2–26 (current-state header, Route A first clip, Bodie fresh site), L86–96 (2026-09-02/03 legs), L106–122 (missing inputs, hard constraints, adjacent assets), L128–170 (2026-09-04/05 milestones), L200–202 (2026-09-17 real-estate vertical) · `AI_DRONE_CINEMATOGRAPHY_BLUEPRINT.md` L2–74 (2026-09-03)

**How to read this chapter:** the hub is a dated log. Its "Where we are" blocks are status, not fact — they go stale. Only the techniques, measured lessons and decisions-with-reasons are extracted here; each is dated.

## Core Idea
The project moved from Earth Studio guide + hand massing (ONSC, Sep 2026) through generative/3D experiments to a fresh site run "strictly as designed" on public measured data (Bodie Island, Oct 2026), where the first geometry-locked photoreal clip passed the truth gate. The lessons of each leg carry forward.

## Frameworks Introduced
- **Multi-tier pipeline (Blueprint L19–59, 2026-09-03)**: macro trajectory & scale (camera + sun) → subject & context 3D veneer (client photos, 3D tiles, AI mesh) → deterministic render (headless Blender G-buffers: depth, normal/edge, alpha matte; or UE5 sequencer) → **AI temporal view synthesis** that "transforms G-buffers & client photos into photorealistic motion" while preserving the rigid camera and geometry. This is the shape the later Route A realises.
- **Images-first site choice** (Hub L22, 2026-10-05): a fresh site picked by available imagery (~400 Commons photos + HABS measured drawings), run as designed, logging every break.
- **"The tool is not the limit."** (Hub L25, lesson B13): COLMAP on internet photos could not register a near-symmetric house in 6 tries; reading the measured drawing + photos built it in one pass.
- **Stage ladder on a fresh site** (Hub L24): (1) DEM + NAIP; (2) USGS lidar; (3) measured skeleton, watertight solids placed in Unreal; (4) solid hero per building from lidar + measured drawing + photos.
- **Resolve orientation flips on oblique frames** (Hub L145, 2026-09-04/05): at nadir the 180° ambiguity is near-degenerate (IoU 0.509 vs 0.499); on an oblique frame entrance asymmetry separates it (0.494 vs 0.454). Yaw sign formula corrected to ψ = (90 − B) − θ (L144).
- **Aspect deficit proof** (L146): 1-D cross-axis scaling warps bilateral masses into ovals — true multi-view reconstruction is required, not stretching.

## Measured lessons from experiments (dated)
- **First Route A clip (2026-10-07, Hub L12–18)**: look from one Commons photo; shape from measured depth along the camera path (Blender) → Wan2.2 Fun-Control 5B on the local 3070; truth gate (SAM 2.1-large seeded from the measured silhouette) HELD, mean IoU 0.85, p5 0.77. Drift grew late in the rise (porch/steps, ground invented). Next levers named: longer path + higher res, best-of-N seeds, line/edge control alongside depth, ground from NAIP.
- **Single-view splat** (L148–152): one camera angle cannot cover a 360° path (frustum cutoff) — need opposing baseline views. Input-coverage fact, not a verdict on splats (ch05).
- **Generated mesh + measured camera** (L128–157): a TRELLIS mesh placed with verified scale/yaw and physical sun, composited over the guide plate across all 661 frames, gave solid 360° architecture — the generated mesh was usable when placed by measurement.
- **Grok i2v, one unaided run (2026-09-03, Hub L96)**: cupola 187–207 px off track, camera pushed in instead of orbiting, building redesigned, watermark reproduced. The note's own implication: unaided i2v can't hold geometry — its lane is drift-tolerant stills/photo replicas; structure must come from G-buffers or a control-capable model. (Fracture 4 caveat: one free-tier test.)
- **Blender guide-pass fixes (2026-09-03, Hub L94)**: Wireframe modifier, not `show_edges`; Standard view transform, not AgX; argparse `-h` crash, 100 m `clip_end`, default-cube purge. Camera acceptance = bidirectional edge match vs projected roof edges.
- **Material sun (Hub L95)**: a spec'd low sun killed shade planes; a higher sun was chosen — material sun is free when the composite is internal-only. Hero stills need capture time (EXIF) or a shadow-derived sun plus camera registration.
- **Engine portability (Hub L168)**: `es_matrices.py` port check 0.027° / 0.531 m and a roof check PASS on the new box before trusting it.

## Hard constraints and adjacent assets (Hub L106–122)
- Roof condition from real photos, never invented; measure roof height once.
- Earth Studio renders: internal guide only; "the customer asset is always generated." No Earth Studio API (~25 min/site by hand/browser).
- Birmingham-Leads (35205 commercial parcels) were missing `building_area` — "the measurement side of this pipeline fills it" (L119). Brand rules: `10-Projects/cosine-brand/_cosine-brand-Hub.md`.

## Real-estate vertical (2026-09-17, Hub L200–202)
Commander's own outreach, not a build task. Agreed sequencing: don't send until the output clears the bar; lead with the finished demo, not a cold call; ask for a room, not a phone pitch.

## Anti-patterns (Blueprint autopsy, L10–15)
Confusing the macro rig for the visual product; over-reading a boundary rule into banning CV libraries; abandoning AI video after one prompt. (Detail in ch05.)

## Key Takeaways
1. Pick sites images-first; measured drawings + photos can beat SfM.
2. Generation is usable when geometry and camera are measured and the result is gated.
3. Resolve orientation on oblique frames, never nadir.
4. Every hub status line is dated history — re-verify.

## Connects To
- **ch02/ch03** (Route A today), **ch05** (caveats on old verdicts), **ch07** (ONSC), **ch08** (scope pivots).
