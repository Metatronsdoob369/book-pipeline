# Chapter 7: The ONSC worked example and the roof/shingle product (v2)

**Sources:** `Flyover Pipeline.md` L11–37 · `ONSC Clubhouse.md` L10–53 · `Product - Shingle Visualization.md` L9–21 · `Renderer Hand-off.md` L8–18 · `Open - Renderer route.md` L8–13 · `Flyover SaaS Backend.md` L8–19 · `INVENTORY_AND_STATUS_QUO.md` L69–80 (all ~2026-09-02/03)

**Scope note:** on 2026-09-07 this roofing framing became **v2** (parked, not abandoned); v1 is a location-agnostic cinematic flyover (Hub L44–45, L71–73). On 2026-10-05 the clubhouse was parked as the goal project and later kept as a benchmark/regression site (Hub L22; Inventory L40). The seven-stage Earth Studio pipeline below is the original design; later work moved to the measured-skeleton routes (ch02/ch03).

## Core Idea
Google Earth as **coordinate system**, Earth Studio as **physically honest camera**, the property's **own photos** for appearance; "The Earth Studio pixels are throwaway; the geometry, the camera path and the sun are what we keep." (Pipeline L13) The invariant is **geometry**, not the roof's current surface.

## Frameworks Introduced
- **Seven stages** (Pipeline L15–22): 1 Extract (hover-read anchors → `anchors.json`, permanent) · 2 Plan (`move.json` → `gt_build.py` → brief + KML + keyframes CSV) · 3 Build & render (Earth Studio, no API, human/browser-driven) · 4 Verify (`es_verify.py` → camera ENU, anchor pixels, pass/fail) · 5 Matrices (camera-to-world + intrinsics) · 6 Render · 7 QA (generated video's roof corners vs `anchor_pixels.csv`).
- **Acceptance test** (Renderer Hand-off L18; Product L21): the four roof corners in the generated video must sit on (or move parallel to) their pixel tracks in `anchor_pixels.csv` in every frame.
- **Division of labour** (Renderer Hand-off L10): geometry from Earth (anchors), motion from the camera, light direction from Time of Day, appearance from the property's own photos, AI as the compositor.
- **Two ways to do the shingle swap** (Product L15–17): *Generative* (prompt/reference the shingle onto the roof) — fast, approximate, may drift; fine for a mood piece. *Geometric* (roof planes as surfaces, each shingle spec a material with real dimensions, camera from `camera_matrices.json`) — deterministic, repeatable per SKU. **"This is the product path."** A new shingle is a new material, not a new pipeline.
- **Three renderer routes** as posed 2026-09-03 (Renderer route L8–13): Higgsfield v2v (fastest, geometry approximate) · image-to-3D + Blender camera (exact camera, surface depends on model) · full 3DGS/photogrammetry (highest fidelity, many photos). Superseded 2026-09-05 (ch09) and again by Route A (ch02).
- **SaaS entity model** (SaaS L10–16): **Site** (`anchors.json`, permanent) and **Flight** (`move.json`, disposable); renders/exports/QA hang off a Flight. Model the Earth Studio stage as a human-in-the-loop task with hand-off in (KML, keyframes CSV, track-point table) and out (tracking JSON, frame folder); everything else is pure Python.

## Key Concepts
- **Anchors**: hover-read fiducials (cupola origin, roof corners, lot corners, pavilion) in DMS/decimal/elevation/ENU; ONSC verified against Google's ruler to 6 cm, anchors ±0.5 m (ONSC L14–30). A reference pin is "reference only, not a fiducial".
- **Roof hero move**: reveal → orbit → rise to top-down hold; the roof is the hero of every move (Pipeline L37).
- **True course size**: a shingle spec (dimensions, exposure, profile, colour blend, hip/ridge cap) rendered on real geometry casts correct shadow lines (Product L13).
- **Recon by-products**: footprint and plane areas, ridge/hip lengths, approximate bundle count. Pitch cannot be read from nadir imagery — take it from an oblique photo or plans and **mark it as an estimate** (Product L19).
- **quotable=false** (Inventory/Status L69–80): hand-massed roof geometry and generic material specs are flagged non-quotable (the "Plumb boundary": Flyover renders visuals; quantities are not quoted from non-Plumb massing).

## Photo capture keyed to anchors (ONSC L50–51)
Each roof corner from the corner and the diagonal; cupola from four sides + a low oblique; wide frames from the parking-lot corners; a scale reference (pavilion with the west end). Measure the real roof height once (QA had assumed +9 m).

## Anti-patterns
- **Inventing roof condition**: "roof condition must come from real photos, never invented." (Hub L108)
- Making the Earth Studio render the customer asset — attribution licence; "the customer asset is always generated" (Hub L114).
- Generative swap as the product (drifts between frames).

## Key Takeaways
1. Geometry is the invariant; the roof surface is the swappable material.
2. Site (anchors) is permanent; Flight (move) is disposable.
3. Roof corners on their anchor pixel tracks in every frame = acceptance.
4. Quantities from imagery are estimates and labelled so.

## Connects To
- **ch06** (camera math), **ch08** (why v2 was parked, licensing on measurements), **ch09** (renderer decision).
