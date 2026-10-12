# Chapter 5: Failure records and verification discipline

**Sources:** `Failure Records — 2026-09-06.md` L2–29 · `AI_DRONE_CINEMATOGRAPHY_BLUEPRINT.md` L10–15 (forensic autopsy, 2026-09-03) · `_flyover-Hub.md` L102 (2026-09-06 mesh-integrity incident) · `Twinmotion Agent Skill Plan (Antigravity).md` L8–14

## Core Idea
The project's worst losses came from claims that were never opened and measured: gates that scored metadata, filenames trusted as proof, one-shot tests written up as verdicts, and Hive notes repeating them with full confidence. Doctrine: **"failure = a position that gets hired once, permanently, never twice."** (Failure Records L2)

## Frameworks Introduced — the six fractures ("Never hire again")
1. **Gate checked properties, not content** (L4–5). A Blender render in `renders/twinmotion/` passed a QA gate that checked existence, resolution, fps and non-black fraction; it was a mesh floating in a black void. *Never hire again: a gate that scores metadata as if it were content.*
2. **"Watertight" label survived sessions unverified** (L7–8). Files named `master_crisp`/`master_solid`/`clean`/`fused` were called watertight because scripts with sealing names had produced them. *Never hire again: treating a filename or a script's name as evidence its own claim is true.*
3. **The re-check over-corrected** (L10–11). bmesh counts reported ~900 islands / ~95,000 "holes"; glTF export splits vertices per face for flat shading. A lossless near-zero-epsilon dedup cut the count roughly in half before any real fill. *Never hire again: counting mesh topology defects before ruling out export-format artifacts, in that order specifically.* (Codified in the `verified-pipeline-discipline` skill.)
4. **One-shot or resource-starved tests written up as settled verdicts** (L13–18): Grok i2v (one free-web prompt, API out of credits), TRELLIS (actually load-bearing in a fused mesh), InfiniSplat (single-view frustum cutoff = input-coverage fact, not "splats don't work"). *Never hire again: compressing "one attempt, under constrained conditions" into "rejected" with no caveat.*
5. **Hive notes compound unverified claims** (L20–21). "The vault is not self-correcting by default." *Never hire again: writing a Hive note in the same voice for "I tested this" and "a prior note said this."*
6. **Eight-plus candidate mesh files, zero convergence** (L23–24). *Never hire again: a session producing a new candidate asset instead of finishing verification on an existing one.*

- **What actually helped** (L26–29): pull real rendered frames and look at them every time before saying a render worked; test a fix at multiple thresholds and report the loss at each; grep the actual notes for provenance instead of defending or capitulating.
- **Two-tier gate** (Twinmotion plan L12–14): Tier 1 deterministic (resolution / frame count / black-frame fraction / edge match vs `qa/clubhouse_roof_edges_px.csv`); Tier 2 advisory (vision-model QA on waypoint frames). A `blackFrameFraction: 0.0` assertion plus edge match would have caught Fracture 1. Operating rule kept from that plan (L24): "never report completion without a green receipt."

## Blueprint autopsy (2026-09-03, L10–15) — three named mistakes
- **Confusing the Macro Rig for the Visual Product**: Earth Studio gives camera physics; its melted satellite imagery and a hand-modelled clay box are not the product.
- **The "Plumb Compliance" Misunderstanding**: a boundary rule ("Flyover renders visuals, Plumb calculates insurance replacement quantities") was turned into a test that banned computer-vision libraries, blocking multi-view reconstruction.
- **Abandoning AI Video Prematurely**: one drifted Grok prompt → "generative video is dead."

## Key Concepts
- **Fracture**: a recorded failure mode, stated as a position never to hire again.
- **Provenance voice**: different wording for tested vs relayed claims (see ch08's `[verified]` / `[relayed]` tags).
- **Advisory skipped**: a missing-API-key vision check must report `ADVISORY_SKIPPED`, not PASS — `gemini_visual_qa.py` fabricated `confidence_score: 0.99` when the key was unset (Hub L185).

## Mental Models
- Treat every claim in the Hive as relayed until you open the file.
- A gate is only real if it has a failure path driven by content.
- Finish verifying an existing asset before making a new one.
- When challenged, grep for provenance — neither defend nor capitulate.

## Anti-patterns
- Unconditional PASS (`qa/run_quality_gates.sh` had one; most gates had zero failure paths — Joint Pipeline Decision L17).
- Reporting a render as working without looking at frames.
- Asserting a single "safe" threshold.
- Wrapping never-run scripts in a skill: "wrapping never-run scripts is documentation of a guess" (Hub L187).

## Key Takeaways
1. Open and measure before believing any label, filename or note.
2. Rule out export artifacts before counting mesh defects.
3. Write one-shot tests as one-shot tests, with conditions.
4. Gates check content and can fail; advisory checks skip, never fake PASS.
5. Converge on one source-of-truth asset.

## Connects To
- **ch01** doctrine "checked truth". **ch09** joint decision (where Fracture 4 verdicts came from).
