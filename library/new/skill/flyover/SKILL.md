---
name: flyover
description: "Operating manual for NoDrone / flyover crew agents (manager, Scout, Shot Maker, Verifier), distilled from the Hive flyover notes. Load when doing any NoDrone work: planning or judging a flyover shot, measuring sites/roofs/heights, building geometry-locked AI aerials (Route A, Wan Fun-Control, truth gate), verifying crew results, driving Unreal/Blender for the pipeline, decoding Earth Studio cameras, or checking licensing and past failure modes before repeating them."
---

<!-- argument-hint: [topic, rule name, role, or chapter number] -->

# Flyover / NoDrone — crew operating manual
**Source**: 25 Hive notes in `~/Hive/10-Projects/flyover` (2026-09-01 → 2026-10-10) | **Chapters**: 11 | **Generated**: 2026-10-12

## How to Use This Skill
- **Without arguments**: the doctrine and rules below are the working core.
- **With a topic** (e.g. `truth gate`, `dark roofs`, `Earth Studio export`): find it in the Topic Index and read that chapter.
- **With a role**: manager → ch01; Scout/Verifier → ch04; Shot Maker → ch03 + ch04.
- These are **working notes**. Dated status (task board, "where we are", versions, paths) goes stale; this skill keeps doctrine, decisions with reasons, techniques and gotchas. The live task board is in `Manager — Start Here.md` in the Hive. Read it there, never from here.

---

## Doctrine (exact wording)
- **"Measured skeleton: never invent geometry or numbers. Generated skin. Checked truth: nothing reaches the Commander unverified."** (ch01)
- **The one rule:** "shape comes from measurement, look comes from photos or generation, and a check proves the look never moved the shape." (ch02)
- **Failure doctrine:** "failure = a position that gets hired once, permanently, never twice." (ch05)
- **Goal (Commander's taste):** "nail the world around a subject, and make the subject's building accurate." (ch03)
- **"give the generator real mass everywhere in frame, or it invents mass for you."** (ch03)
- **"Anchors stay invariant; the massing does not."** (ch09)
- **"The tool is not the limit."** Measured drawings + photos built what SfM couldn't (ch11).

## Roles and flow (ch01)
| Role | Owns | Never |
|---|---|---|
| Commander (Joe) | vision, taste, money/creds/outward calls | — |
| Manager | goals → routes → task cards; judging results; one voice to Commander | sits in tool logs; ships anything unverified |
| Scout | finding and **measuring** sites | generates imagery; invents numbers |
| Shot Maker | camera paths, guides, generation, heals, music, cut | decides what's true about a building; grades own work |
| Verifier | independent checks of every result | edits the work it judges |

Flow: Manager card → Scout measures → Verifier checks → (Shot Maker builds → Verifier checks) → Manager shows the Commander pictures and numbers.
- **Task card**: goal (buyer's terms) · inputs · outputs (exact files) · done when (measurable) · limits.
- **Result card**: status done|partial|blocked · artifacts (images first) · numbers · verdict · problems (evidence path each) · lessons appended to Playbook. Verifier: **PASS / FIX / FAIL** + claims table.
- Board status ∈ `queued · running · verifying · blocked · done`; details in Note. The board is the only state that survives a session.
- **Commander updates**: short; lead with "visible change: none" or "what + where"; ≤1 batched question; no option menus; pictures and numbers. Escalate only money, credentials, outward actions, permission gates.
- **Manager habits**: ask the buyer-level question first (is the input any good? who pays, what must they see?); hand tool work out by card; run anything long resumably; **"Before relaunching anything, prove it is dead."**

## Routes to the shot (ch02)
| Site data | Route |
|---|---|
| Rich: lidar + measured drawings + many photos | **A + B**, C for surroundings |
| Medium: lidar/footprint + a few photos | **A** |
| Thin: 1–2 photos, no lidar | **D** (+C), gated vs footprint + height |
- **A**: measured depth along the path → Wan2.2 Fun-Control 5B with a real photo as look (local, 8 GB).
- **B**: real-photo Gaussian splat along the same path (to verify). **C**: Marble for surroundings only. **D**: free-form i2v, gated; spend needs Commander's go.

## The truth gate (ch02, ch04)
1. Render the building silhouette per frame (`guide_passes_blender.py` IndexOB).
2. SAM 2 refines it on the AI frame → seeds video propagation.
3. Per frame: IoU + boundary-F vs silhouette, presence, depth-in-matte vs rendered depth → HELD / DRIFTED / HALLUCINATED.
4. Best-of-N with a margin; composite the measured render where a clip drifts.
- **Pixel floor**: require per-frame hero share **≥5 %** (min over the clip, not mean). Under ~3 % DRIFTED may be pixels; under ~1 % the gate is noise.

## Shot Maker rules (ch03; each one cost a run)
- Pipeline: Overture footprints + provenance heights → coded paths (81 frames = 3.375 s = 8 beats @142 BPM) → Blender depth + ID guides → Wan Fun-Control (log-depth, fixed range, 832×480×81, same seed + prompt) → heal in layers → truth gate → world bake/re-render.
- Reference image must match frame 0's framing (else "two Burjs").
- Depth control locks mass, not thin detail; thin detail comes from the hero skin composite.
- Put effects in the control, not the beauty.
- Check the subject is in frame (ID pass) before spending GPU.
- Lock music and edit first; fix elements, not whole clips; one fixed skin per hero first.
- 8 GB: fp8 + offload, `/free` between shots, `gpu run --vram 7000 --exclusive`; `gpu status` before planning.
- Never `pkill -f`/`pgrep -f` a pattern matching your own command line.

## Scout / Verifier rules (ch04)
- **"One file, one agent."** Found a file you didn't write → stop.
- **"No lidar return is not ground."** Dark roofs read as no-data, not ground.
- Roof area = raised lidar cells (>2 m) inside the outline, not outline area.
- **"A measured list is not a call list."** Tag `do_not_call`, dedupe by PARCELID, group by owner, re-apply size floor after splitting, confirm presence in newest imagery.
- **"Near the building" is not "shows the building"**: proximity-only photos don't count; ≥2 usable photos per side.
- Proof aspect must equal bounds aspect. Get lidar dates from point GpsTime. Label every unmeasured height.
- A README line saying a thing was done is a claim; grep the output row.

## Never hire again (ch05)
1. A gate that scores metadata as if it were content.
2. Treating a filename or a script's name as evidence its own claim is true.
3. Counting mesh topology defects before ruling out export-format artifacts.
4. Compressing "one attempt, under constrained conditions" into "rejected" with no caveat.
5. Writing a Hive note in the same voice for "I tested this" and "a prior note said this."
6. A session producing a new candidate asset instead of finishing verification on an existing one.
- Advisory checks with no key report `ADVISORY_SKIPPED`, never PASS. Look at real frames before saying a render worked.

## Licensing and scope (ch08; policy readings as of 2026-09-15, not legal advice)
- Camera + geometry half is solved ("the moat"); photoreal look only via **structure-locked diffusion on geometry you have the right to ship**.
- Earth Studio: no promotional/commercial use → internal trajectory/sun math only. Google 3D Tiles: restrictive for a sold flyover; Commander decides via enterprise licensing.
- Ship captured, licensed, or public measured geometry (USGS lidar/DEM, NAIP, HABS).
- Tag claims `[verified <date>]` vs `[relayed]`.

## Engine drive (ch10)
- Agent drives the editor; the Commander is not the click-path. No OS-level UI automation (ch09).
- UE Remote Control Python: section `[/Script/RemoteControlCommon.RemoteControlSettings]` in `DefaultRemoteControl.ini` (DefaultEngine.ini keys ignored); gates `bEnableRemotePythonExecution` + function allowlist. Launch via scheduled task, not SSH `Start-Process`; `-ExecutePythonScript=` quits a live editor.
- Verify any MCP bridge by config + port scan, else go headless (`UnrealEditor-Cmd`, `blender -b`).

---

## Resolved disagreements (2026-10-12)
Source: `Contradictions — 2026-10-12.md`. Rule: measure where possible, else the newer dated note wins. Older notes still say the old thing — trust this list over them.
- Splats = Route B, Marble = Route C. The Joint Decision's TRELLIS / splat / Grok rejections were one-shot verdicts (Failure Records Fracture 4).
- Earth Studio: reference/decoding camera only, never in sellable pixels. Google 3D Tiles: NOT cleared for sale until a licence is read and filed (Commander).
- Blender MCP (`:9876`) exists only while Blender runs with the addon — check the port before relying on it.
- 5820: Windows host 128 GB, Xeon W-2145 8C/16T; WSL sees 62 GB / 10 threads. LAN IP is DHCP — address it as `t5820-wsl`.
- Sun: chosen 20.7°/264.6° stands; the "EXIF drone timestamp" claim is unverified.
- `quotable=false` CV boundary stands; OS-level UI automation stays rejected.

## Chapter Index
| # | Title | Key frameworks |
|---|---|---|
| [ch01](chapters/ch01-manager-and-crew.md) | Manager role, crew, cards | doctrine, roles, task/result card, board, prove-it-dead |
| [ch02](chapters/ch02-capability-atlas-routes-truth-gate.md) | Capability Atlas | primitives, routes A–D, truth gate, blocked tools |
| [ch03](chapters/ch03-playbook-generated-aerials.md) | Playbook: pipeline, rules, heights, taste | Route A pipeline, layered heal, world bake, height merge |
| [ch04](chapters/ch04-crew-lessons.md) | Scout / Verifier / Shot Maker lessons | one file one agent, no-return≠ground, pixel floor |
| [ch05](chapters/ch05-failure-records.md) | Failure records | six fractures, two-tier gate, blueprint autopsy |
| [ch06](chapters/ch06-earth-studio-camera.md) | Earth Studio as camera | export decode, FOV 40, top offset 3 m, Site vs Flight |
| [ch07](chapters/ch07-onsc-and-roof-product-v2.md) | ONSC example and roof product (v2) | 7 stages, anchor-pixel acceptance, geometric swap |
| [ch08](chapters/ch08-capability-and-licensing.md) | Capability & licensing | four-claim verdicts, provenance tags, v1/v2 |
| [ch09](chapters/ch09-joint-decision-and-renderer.md) | Joint decision & renderer | priority order, capture spec, rig≠beauty, no UI automation |
| [ch10](chapters/ch10-unreal-machine-environment.md) | Unreal, machine, environment | RC ini gates, headless drive, VRAM, LFS sync |
| [ch11](chapters/ch11-history-experiments-blueprint.md) | History, experiments, blueprint | images-first sites, oblique flips, multi-tier blueprint |

## Topic Index
- **Anchors / anchor_pixels.csv** → ch06, ch07
- **Aspect gate** → ch09
- **Best-of-N** → ch02, ch03
- **Blender guide passes / EXR** → ch02, ch03, ch11
- **Call list / do_not_call / parcels** → ch04
- **Capture spec** → ch09, ch07
- **Cards / task board** → ch01
- **Dark roofs / lidar no-return** → ch04
- **Doctrine** → ch01, ch02
- **Earth Studio (UI, export, FOV, offset)** → ch06
- **Failure fractures** → ch05
- **GPU Guardian / 8 GB** → ch03, ch04, ch10
- **Heights (Overture, GloBFP, floors)** → ch03, ch04
- **Licensing (Earth Studio, 3D Tiles)** → ch08
- **Marble / GEN3C / Atlas** → ch02, ch08
- **Photo census (Mapillary, Commons)** → ch04
- **Pixel floor / hero frame share** → ch04
- **RealityScan** → ch09, ch10
- **Renderer route / Twinmotion** → ch07, ch09
- **Routes A–D** → ch02
- **SAM 2 / SAM 3** → ch02, ch03
- **Shingle swap / v2** → ch07
- **Taste** → ch03
- **Truth gate** → ch02, ch04
- **Two-tier gate** → ch05, ch09
- **Unreal Remote Control / MCP** → ch10
- **Wan2.2 Fun-Control** → ch02, ch03, ch11
- **World bake** → ch03

## Supporting Files
- [glossary.md](glossary.md): terms
- [patterns.md](patterns.md): techniques as when/how/trade-offs
- [cheatsheet.md](cheatsheet.md): decision rules, thresholds, tells, route matrix

## Scope & Limits
This skill covers the Hive flyover notes as of 2026-10-10 only. It does not cover live status, credentials or task assignments; read the Hive (`Manager — Start Here.md`, `Crew.md`, `Playbook — Generated Aerials.md`) for those, and append new lessons there, not here. Numbers marked provisional in the source (e.g. the 5 % hero-share floor) remain provisional.
