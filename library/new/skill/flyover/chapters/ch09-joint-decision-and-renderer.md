# Chapter 9: Joint Pipeline Decision, the renderer choice, and the Twinmotion plan

**Sources:** `Joint Pipeline Decision.md` L2–49 (2026-09-05) · `_flyover-Hub.md` L98–100 (open decisions), L172–187 (joint-decision and Twinmotion/UE5 milestones) · `Twinmotion Agent Skill Plan (Antigravity).md` L2–27 · `Open - Renderer route.md` L8–13

**Read with ch05:** several "rejected" verdicts adopted here were later shown to be one-shot tests (Failure Records Fracture 4). The later working pipeline (ch02/ch03, 2026-10) is Route A generation on measured geometry, not the Twinmotion beauty render.

## Core Idea
Two independent audits (Gemini/Antigravity and Claude Code) entering from opposite ends were merged into one decision with a stated priority order. Its durable lessons: fix the gate chain first, no software substitutes for missing capture, keep the measurement rig separate from the beauty render, and when a cross-check undermines a target, demote the gate rather than chase the number.

## Frameworks Introduced
- **Parallel independent audits, then merge** (L4–6): two agents, no knowledge of each other, different entry points; adopt only where both agree.
- **Where both agreed** (L8–13), as of 2026-09-05: (1) replace the Earth Studio flat plate with Google 3D Tiles via Cesium in UE5 (native occlusion, scriptable); (2) deterministic multi-view photogrammetry (RealityScan) over generative single-view 3D for metric scale; (3) the surveyed CAD roof stays the invariant control datum; (4) volumetric splats are not the final asset. *Items 1 and 4 later conflicted with licensing (ch08) and Fracture 4 (ch05).*
- **Stated priority order** (L15–20): (1) **Fix the gate chain** — "the single highest-priority fix" (an unconditional PASS existed); (2) write the capture spec and re-shoot — "no software substitutes for missing capture"; (3) Solar API cross-check; (4) **then** environment, **then** beauty render.
- **Capture spec** (L18): Epic's guidance ~70 % overlap, ≤30° between neighbouring poses, nadir *and* oblique; 8 photos with 45°+ jumps is not enough.
- **Solar API addendum** (L22–30): the roof was genuinely bimodal in pitch; plan area 26.6 % low in the hand massing; bearing disagreement was a derived-frame error. The aspect target carried ~±20 % uncertainty → **suspend the aspect gate as pass/fail (reporting only)**, rebuild massing from the 35 segments, re-derive the target, downgrade the re-shoot to conditional. "**Anchors stay invariant; the massing does not.**" (Hub L176) What did not change: anchors, camera track, sun solve, two-tier gate rule, commercial reading.
- **Measurement rig ≠ beauty render** (L32–34): Twinmotion/beauty replaces only the client-facing render; `blender_gbuffers.py` wire/mask control signals (verified 100 % bidirectional edge match vs `qa/clubhouse_roof_edges_px.csv`) are a different job "that looks similar. Keep both."
- **Renderer decision, 2026-09-05** (Hub L180–187): UE5 + Twinmotion **Content-for-UE plugin**, renders via Movie Render Queue + `unreal-mcp`/`UnrealEditor-Cmd`; deliverable is video only (no `.tm` project); **OS-level UI automation rejected** (no pywinauto/AppleScript, no external Twinmotion.exe). This replaced the Higgsfield/3DGS route debate.
- **Twinmotion plan triage** (Plan L16–25): keep the renderer-agnostic parts — two-tier gate (`verify_twinmotion_output.py`), typed `TwinmotionJobSpec`/`TwinmotionExecutionResult` contracts, Phase 4 skill discipline ("never report completion without a green receipt"); drop/rewrite Phases 1–2 (Datasmith + external exe + UI automation). Hard constraint quoted by the plan: Twinmotion has no native Python API, no scriptable CLI, no headless interface (L12).

## Key Concepts
- **Gate chain**: the sequence of QA gates; must have content-driven failure paths.
- **Aspect gate**: depth/width ratio check on the mesh; demoted to reporting-only once its target was shown unreliable.
- **Sequencing, not contradiction** (Plan L6): a plan written earlier the same day as a decision is not defiance — check timestamps before calling conflict.
- **Dead code flagged, not silently removed** (Hub L183).

## Gotchas
- **Frame-rate bug** (Hub L184): "661 frames @ 60fps" for 11.017 s is wrong; the trajectory is 22 s @ 30 fps. Author the Sequencer at the 30 fps keys, set MRQ output to 60 (Sequencer interpolates) → ~1321 frames, ~22 s.
- **Fabricated PASS** (Hub L185): `gemini_visual_qa.py` returned `confidence_score: 0.99` with no API key — must be `ADVISORY_SKIPPED`.
- **Invented asset names** (Hub L183): enumerate the plugin's real asset paths at runtime; don't hardcode guessed names.
- **Canonical mesh unresolved** (Hub L186): confirm whether the UE FBX already has anchor-aligned geometry or needs the Blender-side scale/yaw.
- **`EpicGames/RealityScan` on GitHub is not the app** — it is `pano2views`, a 360°-to-cube-faces converter (L36–38).
- **Don't wrap never-run scripts in a skill** — wait for one real run (Hub L187).

## Open/unverified per the doc (L40–47)
Whether 3D Tiles and Earth Studio share a mesh; Solar API pricing/accuracy at a site; MapAnything claims; MatSwap on shingles; RealityScan minimum photo count.

## Key Takeaways
1. Gate chain before anything else.
2. Capture beats software; write the capture spec.
3. When the target is shaky, demote the gate to reporting and re-derive the target.
4. Keep measurement rig and beauty render as separate jobs.
5. No OS-level UI automation; drive engines via MRQ / headless CLI / MCP.

## Connects To
- **ch05** (fractures this decision embedded), **ch10** (UE/remote-control gotchas), **ch02** (later Route A).
