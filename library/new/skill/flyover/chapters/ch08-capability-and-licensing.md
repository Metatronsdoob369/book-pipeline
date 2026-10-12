# Chapter 8: What is possible, and licensing as the wall

**Sources:** `Capability Assessment — 2026-09-15.md` L9–42 · `_flyover-Hub.md` L44–45 (2026-09-07 scope pivot), L47–51 (2026-09-15 route + licensing flag), L53–55 (2026-09-08 v1 picture), L71–74 (2026-09-07 v1 scope). Policy readings are the notes' own, "not legal advice", verified 2026-09-15; re-check before relying on them.

## Core Idea
Deterministic aerial footage of a real location splits into a solved half (6-DoF camera + geometry-locked motion — "the moat") and a hard half (photoreal appearance), which is possible only via **structure-locked diffusion on geometry you have the right to ship**. Licensing, not technology, is the wall.

## Frameworks Introduced
- **Four-claim decomposition with verdicts** (Assessment L11–36): split the ask into independent claims, give each a verdict:
  1. Deterministic 6-DoF camera + geometry-locked motion — **SOLVED, already owned**. "Geometry in, geometry out: zero variation by construction." This is what prompt-driven video tools cannot do.
  2. "Any location on earth" at photoreal — **NOT POSSIBLE today**: Google Photorealistic 3D Tiles cover ~2,500 cities / 49+ countries; outside coverage the only photoreal geometry is a site visit (drone → RealityScan/3DGS).
  3. "Little variation in accuracy" — **POSSIBLE, only under one architecture**: render geometry deterministically along the exact trajectory; confine diffusion to a structure-locked enhancement pass.
  4. Licensing — **the real wall**.
- **Provenance tags** (L11): **[verified <date>]** = checked this session (web fetch or file opened); **[relayed]** = carried from notes, not re-tested. Use on every claim.
- **"Bridge to check, not a claim"** (L28): when two components look format-compatible (Blender depth pass ↔ GEN3C v2v input), verify the format matches before building on it.
- **One-line verdict** (L41–42): "The deterministic-camera half is done and is the moat. The photoreal-appearance half is possible today only via structure-locked diffusion … and only on geometry you have the right to ship — which today means captured or licensed geometry, not Google's."

## Structure-locked options named (as of 2026-09-15, L24–27)
- **NVIDIA GEN3C**: "3D cache" rendered along the trajectory conditions the video model; v2v takes per-frame depth + pose + intrinsics. Open code (Apache 2.0); weights under NVIDIA Open Model License (commercial → inquiry). Tested on H100/A100, ~43 GB with offloading.
- **World Labs Marble**: worlds from text/images/video; exports splats, meshes, video with camera control. **Caveat: it generates** — property identity (roof corners) not guaranteed.
- **World Labs Atlas**: poses/depth as native inputs; early access only (no API date or pricing as of 2026-09-15).
- Prompt-driven i2v/t2v remains non-deterministic on camera — "Not the path." (L27)

## Licensing readings
- **Earth Studio** (L31): content may not be used "for promotional films, advertisements or commercials" (real-estate video is Google's own example). → Earth Studio scoped to internal trajectory/sun-math reference only (Hub L45).
- **Google Photorealistic 3D Tiles** (L32–34): promo videos ≤30 s, no Street View, not resold separately; offline uses, non-visualization uses (image analysis, machine interpretation, geodata extraction) and pre-fetching/storing prohibited. Reading: the promo carve-out is for promoting *your app*, not a pre-rendered flyover sold as the deliverable; feeding tile renders into diffusion is arguably machine interpretation. Path to confirm: Google Maps Platform enterprise licensing. Commander decides.
- **Measurements from Google 3D imagery** (L35): "programmatically reading and recording measurements … is considered derivative and is prohibited" — relevant to v2 roof quantities.
- **Licence-clean geometry** (L36): drone capture (RealityScan), licensed mesh vendors (rights to confirm), and — per later work — public measured data (USGS lidar, DEM, NAIP, HABS drawings; ch02/ch11).

## v1 vs v2 (Hub L44–45, L53–55, L71–74)
- **v1**: any real-world location → directable (sun/time/weather) cinematic aerial flyover, sold as an agency capability to promo/sales/marketing clients; not an editing tool.
- **v2**: roofing/shingle visualization (ch07), built on v1's core once v1 ships.
- **"The clubhouse mesh is the film"**; 3D Tiles were the coordinate plate/environment, not the deliverable. "A tiles-only orbit is worthless" — the Commander already has ~10k Earth Studio/maps flyovers (Hub L55).
- Route chosen 2026-09-15 (Hub L49): trajectory math + generated/photographed appearance → Marble world → local render; ships no Google pixels or mesh. Remaining Google thread: anchor coordinates — replaceable with USGS/county data for US sites.

## Anti-patterns
- Writing "commercially licensed for exactly this use" without reading the policy page.
- Treating a generator's "camera control" as property-identity control.
- Editing a canonical decision doc to match your reading — flag it; the Commander decides (L34).

## Key Takeaways
1. Own the camera and the geometry; rent only the look.
2. Ship only geometry you have the right to ship.
3. Tag every claim verified-with-date or relayed.
4. A tiles-only or Earth-Studio-pixel deliverable is not the product.

## Connects To
- **ch02** (Route A is the structure-locked architecture realised locally), **ch06**, **ch07**.
