# Chapter 6: Earth Studio as camera — findings, export format, ground-truth skill, move decisions

**Sources:** `Earth Studio Findings.md` L8–24 · `Earth Studio Export Format.md` L8–17 · `Earth Ground Truth Skill.md` L9–18 · `Decision - Field of View 40.md` L9–15 · `Decision - Top keys offset 3 m.md` L9–11 · `Open - Pacing 22 s vs 44 s.md` L8–10 (all 2026-09-02/03, verified on the ONSC build)

**Scope note:** since 2026-09-07 Earth Studio is an **internal trajectory / sun-math reference only** — its content may not be used in promotional/commercial video (see ch08). The camera math below stays valid.

## Core Idea
Earth Studio supplies physically honest 6-DoF camera motion, lens and sun; its pixels are throwaway. The export must be decoded correctly (ECEF-local, not ENU) and the move designed so every roof anchor stays in frame and the camera never flips.

## Frameworks Introduced
- **Site vs Flight** (Ground Truth Skill L18): **Site** = `anchors.json` (permanent). **Flight** = `move.json` (disposable). New flight = new move file; new property = new anchors.
- **Engine scripts** (L13–16): `gt_build.py <site> move.json` → brief, KML overlay, keyframes CSV; `es_verify.py <export.json> <site> --keyframes … --ground …` → `camera_enu.csv`, `anchor_pixels.csv`, anchors-in-frame report; `es_matrices.py` → per-frame 4×4 camera-to-world + intrinsics.
- **Default move — 22 s roof hero** (L13): reveal from the open side r 200→110 m, orbit at r 90 m in 45° steps toward the entrance side, rise to 85 m hold offset 3 m. Knobs: `open_side_brg`, `orbit_direction`, `ground_m`, `target_agl`, `top_offset_m`, `orbit_keys`, `reveal`, `top`, `time_of_day_gmt`, `site_title`.
- **Decision: FOV 40° vertical** (FOV40 L9–15). Default 20° (≈34.8° horizontal) covers ~53 × 30 m at an 85 m hold — a 60.4 m building's corners leave frame. 30° and 35° still lose a corner. 40° (~65.8° horizontal, ~110 × 62 m at 85 m) keeps all anchors in frame on all 661 frames with ~25 m buffer and "reads more like a real drone camera." Static attribute, no keyframe changes.
- **Decision: top keys 3 m off origin** (Top keys L9–11). A camera passing exactly over its Camera Target can snap through a 180° flip. Moving KF5/KF6 3 m toward the last orbit key = 2° tilt at 85 m, invisible, keeps the last four seconds stable and pixel projection well-defined. `top_offset_m` default 3.
- **Open: pacing 22 s vs 44 s** (Pacing L8–10). 22 s peaks ~23 m/s on orbit legs (stylised); real drones film ~5–12 m/s. Doubling keyframe times halves speeds, nothing else changes. Decide after first preview; owner Joe.

## Export format, decoded (Export Format L10–17)
- `cameraFrames[i].coordinate` — exact lat, lon, altitude ASL. **Trust first.**
- `position` / `trackPoints[].position` — **"Local" = ECEF axes translated to the origin track point, NOT east/north/up.** Rotate by the ENU basis at origin (φ, λ): ê = (−sin λ, cos λ, 0), n̂ = (−sin φ cos λ, −sin φ sin λ, cos φ), û = (cos φ cos λ, cos φ sin λ, sin φ). Treating it as ENU was wrong by up to ~90 m on ONSC.
- `rotation` (deg): **R = Rx(x)·Ry(y)·Rz(z)**; forward = R·(0,0,+1), up = R·(0,−1,0); camera frame is OpenCV-style (x right, y down, z forward).
- Intrinsics: fx = fy = (H/2)/tan(fov/2), principal point at centre (1483.6 px at 40°, 1920×1080). Horizontal FOV = 2·atan(tan(fov/2)·W/H).
- `numFrames` = 660 but there are **661** cameraFrames (0–660 inclusive).
- Renderer camera-to-world: columns = [x_cam, y_cam, z_cam, C] in ENU; for COLMAP/3DGS world-to-camera, invert.

## Earth Studio UI findings (Findings L10–24)
- Typing a value does not create a keyframe — click the diamond (filled = keyed).
- Bare keystrokes are shortcuts (digits 1–4 change viewport count); type only into a focused field.
- Track point altitude doesn't follow a typed coordinate — type the elevation too.
- Camera Target at origin + 7 m, Influence 100 % → only position needs keyframing.
- Auto-Smooth on middle keys turns 45° orbit keys into an arc.
- Time of Day (GMT) gives real sun; Clouds pull live weather — hide them.
- KML overlays bake into renders — framing only.
- Render dialog may reopen on cloud .mp4 — switch to local image sequence; Map Style Clean; Advanced → 3D Tracking Data JSON, Coordinate space Local.
- **No API** — build/render is human-in-the-loop or browser automation (~25 min/site).
- Attribution mandatory on every frame — render stays an internal guide.
- Claude-in-Chrome: tools act on the front tab only; if all fail, close/reopen the side panel; screenshot `scale` may be ignored.

## Anti-patterns
- Treating "Local" coordinates as ENU. Keying the camera directly over the target. Shipping Earth Studio pixels. Trusting `numFrames`.

## Key Takeaways
1. Anchors are permanent; moves are disposable.
2. Decode Local as ECEF-shifted, rotate to ENU, R = Rx·Ry·Rz, OpenCV camera frame.
3. FOV 40 and a 3 m top offset keep every anchor in frame and the camera stable.
4. Earth Studio = math reference, never content.

## Connects To
- **ch07** (ONSC worked example and the v2 product). **ch08** (licensing exclusion).
