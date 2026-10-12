# Patterns — flyover

## Route-by-data
**When to use**: choosing how to make a shot for a site.
**How**: rich (lidar + drawings + many photos) → A + B, C for surroundings; medium (lidar/footprint + few photos) → A; thin (1–2 photos) → D (+C), gated against footprint + height. (Ch 2)
**Trade-offs**: A needs measured geometry; D is fastest but least locked.

## Geometry-locked generation (Route A)
**When to use**: any photoreal clip of a real building.
**How**: measured/parametric geometry → coded camera path → Blender depth + object ID guides → Wan2.2 Fun-Control 5B on log-depth over a fixed range, 832×480 × 81 frames, same seed + prompt across shots, reference photo matching frame 0. (Ch 3)
**Trade-offs**: locks mass, not thin detail; thin detail comes from the hero skin.

## Truth gate
**When to use**: before any clip is called good.
**How**: render silhouette per frame → SAM 2 refine + video propagate → per-frame IoU, boundary-F, presence, depth-in-matte → best-of-N with margin; composite measured render where it drifts. Check hero frame share ≥5 % per frame first. (Ch 2, 4)
**Trade-offs**: below ~3 % share verdicts are pixel noise.

## Layered heal
**When to use**: a locked edit has a flawed element.
**How**: lock music + edit → one fixed hero skin → SAM 3 text-track removal (prompt on a clear frame) → fill. Don't regenerate whole clips. (Ch 3)

## World bake and re-render
**When to use**: after good generation, to get new camera paths cheaply.
**How**: `world_bake.py` projects frames onto geometry (depth-tested, best view wins) → `world_render.py` → low-denoise `world_polish.py`. Sample surface points per group instead of subdividing. (Ch 3)

## Height merge with provenance
**When to use**: city context geometry.
**How**: tagged height > floors × 3.6 m > 3D-GloBFP > 6 m default; label every unmeasured height; check `sources` for ML-derived heights (half weight). (Ch 3, 4)

## Lidar roof measurement
**When to use**: roof area/slope for leads.
**How**: cells >2 m above ground inside the outline; slope/height from cells eroded 2 m; flag <85 % raised; empty top-surface cells = no-return (magenta), not ground; cyan tint on counted cells. (Ch 4)

## Proof image per row
**When to use**: every Scout measurement.
**How**: boundless NAIP read, newest-year mosaic; proof aspect = bounds aspect; clean (untinted) chips for eye calls; overrides recorded in `overrides.json`. (Ch 4)

## Measured list → call list
**When to use**: before handing anything to sales.
**How**: collapse stacked accounts by PARCELID; re-pick multi-lot owners by largest overlap; tag `do_not_call`; group by owner/account; re-apply the size floor after splitting; confirm presence in newest imagery. (Ch 4)

## Photo census with honest counts
**When to use**: deciding whether a site has enough photos.
**How**: exclude proximity-only; footprint ≥25 % of FOV for flat cameras; clear sight line past neighbours; ≥2 usable photos per side; crop 360s toward the hero; allow tied photos to reach radius + 2 × height for tall subjects. (Ch 4)

## Earth Studio camera decode
**When to use**: any Earth Studio export (internal math only).
**How**: trust `coordinate`; rotate Local (ECEF-shifted) to ENU; R = Rx·Ry·Rz, OpenCV camera frame; fx = (H/2)/tan(fov/2); 661 frames not 660. FOV 40; top keys 3 m off target. (Ch 6)

## Task card → result card → verifier
**When to use**: all crew work.
**How**: card with measurable "done when" → specialist returns artifacts (images first), numbers, verdict, problems with evidence → Verifier PASS/FIX/FAIL with claims table → manager updates board. (Ch 1)

## Two-tier gate
**When to use**: any automated QA.
**How**: Tier 1 deterministic content checks with real failure paths (black-frame fraction, edge match); Tier 2 advisory vision QA that reports `ADVISORY_SKIPPED` when unavailable. (Ch 5, 9)

## Parallel independent audits
**When to use**: big pipeline decisions.
**How**: two agents audit from different ends without seeing each other; adopt where both agree; record the doc's own open/unverified list. (Ch 9)
**Trade-offs**: agreement can still embed one-shot verdicts (Fracture 4) — re-check provenance.

## Cheap CPU pre-check before GPU
**When to use**: before renders that need a GPU lease.
**How**: numpy/PIL pinhole projection of hero OBJs to pick distances/frame share (IoU 0.91–0.93 vs Blender masks); print "subject in frame" per shot from the ID pass; check `gpu status`. (Ch 3, 4)

## Headless engine drive
**When to use**: Unreal/Blender automation without a confirmed bridge.
**How**: UE remote Python (RemoteControlCommon ini section, both gates) launched via scheduled task, or `UnrealEditor-Cmd … -ExecutePythonScript` for batch only; `blender -b --factory-startup -P script.py --`. (Ch 10)
