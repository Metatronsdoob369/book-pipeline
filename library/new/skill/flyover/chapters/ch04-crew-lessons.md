# Chapter 4: Scout, Verifier and Shot Maker lessons

**Source:** `Playbook — Generated Aerials.md` L58–91 (Scout L58–79, Verifier L81–84, Shot Maker L86–91; all dated 2026-10-08 / 2026-10-10, from the Birmingham 35205 flat-roof scan, the cand-1 photo census, and cap-1). Counts below are from those runs, kept only where they set a rule.

## Core Idea
Measurement work fails quietly at boundaries — tile edges, dark roofs, stacked parcels, proximity-only photos, tiny heroes in frame. Each lesson is a check that makes the numbers honest.

## Frameworks Introduced
- **"One file, one agent."** (L60) Two crew sessions wrote `engine/roof_scan.py` at once; the second overwrote the first. Manager gives a file to only one live agent; a Scout that finds a file it didn't write must stop rather than overwrite.
- **"No lidar return is not ground."** (Verifier L81) Dark roofs (black EPDM, old tar) return almost no 3DEP points; filling empty cells with ground height drops the best coating leads. Count empty top-surface cells inside the outline; tint magenta.
- **"A measured list is not a call list."** (L81) 36 % of 35205 rows were decks, university, government, right-of-way or duplicates. Tag `do_not_call` and group by owner before anything goes to sales.
- **"Near the building" is not "shows the building"** — three filters (L75): (1) Commons camera within 60 m with no other tie = `proximity_only`, not counted; (2) flat cameras need the footprint across ≥25 % of their FOV; (3) sight line must clear neighbouring Overture outlines. A side counts only with ≥2 usable photos.
- **Truth-gate pixel floor** (Shot Maker L86): at 672×384 with a 2 px edge error, a perfect clip scores IoU 0.90+ at ≥5 % hero share, ~0.85 (HOLD bar) at 2.5–3 %, <0.75 (p5 bar) at ≤1 %. Provisional rule: **per-frame hero share ≥5 % (min over the clip, not the mean), or ≈13k hero px at 672×384 (≈20k at 832×480)**. Under ~3 % a DRIFTED verdict can be pixels; under ~1 % the gate is noise.

## Scout techniques
- **Box scan with 3DEP EPT** (L58): walk the EPT hierarchy once for the box, pull nodes per ~250 m tile in parallel with an on-disk node cache; cap depth (12 on AL_11County_2_B23 ≈ 9 pts/m², enough for 1 m slope cells).
- **County parcel point-in-polygon** via ArcGIS `query?geometry=lon,lat&geometryType=esriGeometryPoint…`; strip string fields (OWNERNAME is space-padded) (L59).
- **Roof area = lidar cells >2 m above ground inside the outline**, not outline area; slope/height from cells eroded 2 m; flag outlines <85 % raised; tint counted cells cyan (L62).
- **Owner lookups need a second look**: ~1 in 6 big roofs span several lots; re-pick by envelope query + largest overlap; list other lot owners (L63).
- **Collapse stacked tax accounts by PARCELID**; owner per lot = largest summed AssdValue (L66).
- **NAIP proofs: boundless read + mosaic every tile of the newest year**; check proof aspect equals bounds aspect (L61).
- **Dark roofs**: accept sparse roof as flat when lidar still says flat; else call by eye on a CLEAN NAIP chip and record in `overrides.json` (L65).
- **Parking decks**: not auto-detectable from NAIP 0.6 m + 3DEP; use Overture class/name + eye pass, 20 chips/sheet at 400 px (L67).
- **Demolitions**: two-year NAIP correlation failed (season mismatch); eye-review old|newest pairs. Roof brightness ÷ ground ring (3–15 m) across years does rank recent membrane/coating (L69).
- **Green roofs**: NDVI fails in hazy NAIP; digitise by eye on a gridded clean chip; measure rather than estimate (L70).
- **Single mailing line** in Jefferson Co parcels: don't re-query; mark `mail_note` (L71). Name rules need an "at X" exclusion (`\bUAB\b` but not `\bAT UAB\b`) (L72).
- **Photo sources for commercial buildings**: keyless sources nearly empty; Mapillary decides everything. KartaView: use v1 `POST /1.0/list/nearby-photos/`; Openverse has no geo search; crop Mapillary 360s 100° toward the hero (pano centre column = `compass_angle`) (L74).
- **Tall subjects**: let photos tied to the building reach radius + 2 × lidar height; filter titles (plate/sheet/details/lens/stairs/"view from"/animals) (L76).
- **Lidar date from the points' GpsTime**, not the project name; label fallbacks. NC_PHASE2_2003 tiles have no CRS (EPSG 2264) — read with `laz_backend=LazBackend.Lazrs`. Find tiles keyless via the TNM products API (L77).
- **Overture heights may be Microsoft ML, not tags** — check `sources`; score ML at half weight. Overture may split one building into two outlines (L78).

## Verifier checks
- Re-apply the buyer's size floor **after** splitting by owner, or tier the slices (L82).
- Before overriding a dark roof to flat, look at **where** the steep cells sit: on equipment, ignore; on roof planes, don't (L82).
- Check every row is present in the newest imagery (lidar predates NAIP) (L82).
- Recount through the account map, not raw owner keys (L83).
- "A README line saying 'X was added to tag Y' is a claim, not a fact" — always grep the output row (L83).

## Shot Maker techniques
- Separate size from time: compare distances at the same frame index (`route_a_prep.py --dist-scale k`) (L87).
- **Pick distances on CPU first**: numpy/PIL pinhole projection matches Blender ID masks at IoU 0.91–0.93 (reads ~7 % high, ignores terrain occlusion) (L88).
- Pulling a low camera back sinks it under ground; `--dist-scale` floors at hero ground + 1.7 m (L89).
- **Check `gpu status` before planning GPU work**; GUARD for Blender+UE open blocks even 2 GB leases; unblock is the Commander closing one app — don't force `gpu window` (L90).

## Anti-patterns
- Two agents on one file; trusting a stretched proof chip; outline-median slope; counting proximity-only photos; trusting a DRIFTED verdict on a sub-3 % hero; estimating when you can measure.

## Key Takeaways
1. Every measured row carries a proof image whose geometry matches its bounds.
2. Missing data (no-return, no-geotag, ML height) is labelled, never silently filled.
3. Hero frame share ≥5 % per frame before trusting the truth gate.
4. Verify outputs by grepping the rows, not by reading claims about them.

## Connects To
- **ch01** (cards, one-file rule), **ch02** (truth gate), **ch05** (claims vs evidence).
