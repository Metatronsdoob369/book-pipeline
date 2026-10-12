# Cheatsheet — flyover

## Decision rules
- **Asked for a clip** → pick route by site data (rich A+B / medium A / thin D), gate it, Verifier before Commander. (Ch 2)
- **Clip looks wrong in one element** → heal the element (skin / SAM 3 / fill) inside the locked edit; don't regenerate. (Ch 3)
- **Generator invents structures** → give it real mass everywhere in frame. (Ch 3)
- **Thin detail drifts** (spires, jets) → move it into the hero skin or into the *control*, not the beauty. (Ch 3)
- **Two subjects appear** → reference image doesn't match frame 0; use `--no-ref` or world-rendered frame 0. (Ch 3)
- **Truth gate says DRIFTED** → check per-frame hero share first; <3 % may be pixels, <1 % is noise. (Ch 4)
- **A note says X was done/rejected** → open the file / grep the row; was it a one-shot test? (Ch 5)
- **Mesh "has holes"** → lossless dedup to rule out export splitting first, then count. (Ch 5)
- **Target looks shaky** → demote the gate to reporting, re-derive the target. (Ch 9)
- **Before relaunching** → prove it is dead (ps, timestamps, agent status). (Ch 1)
- **File you didn't write** → stop; one file, one agent. (Ch 4)
- **GPU plan** → `gpu status` first; GUARD for Blender+UE = Commander closes an app. (Ch 4)
- **Need money, creds, outward action** → escalate; everything else, decide. (Ch 1)
- **Earth Studio / Google tiles pixels in a deliverable** → no; internal math only; ship captured/licensed/public-measured geometry. (Ch 8)

## Thresholds & defaults
| Item | Value | Ch |
|---|---|---|
| Truth gate HOLD bar / p5 bar | mean IoU ~0.85 / p5 0.75 | 4 |
| Min hero frame share | ≥5 % per frame (min, not mean); ≈13k px @672×384, ≈20k @832×480 | 4 |
| Shot length | 81 frames = 3.375 s = 8 beats @142 BPM | 3 |
| Gen resolution on 8 GB | 832×480 × 81, fp8 + offload, `gpu run --vram 7000 --exclusive` | 3 |
| Bake sampling | 0.5 m hero · 0.75 m city · 1 m ground | 3 |
| Floors → height | × 3.6 m; default 6 m | 3 |
| Roof cells | >2 m above ground; erode 2 m; flag <85 % raised | 4 |
| Photo side | ≥2 usable photos; flat cams footprint ≥25 % FOV; 60 m ring (tall: r + 2×height) | 4 |
| Earth Studio | FOV 40° vertical; top offset 3 m; target origin + 7 m; 661 frames | 6 |
| Real drone speed | ~5–12 m/s (22 s move peaks ~23 m/s) | 6 |
| Capture spec | ~70 % overlap, ≤30° between poses, nadir + oblique | 9 |
| Taste | films ≥30 s, music, dynamic angles | 3 |
| Low camera floor | hero ground + 1.7 m | 4 |

## Tells & smells
- Gate checks resolution/fps/non-black only → it scores metadata, not content. (Ch 5)
- Asset trusted because of its filename or the script that made it. (Ch 5)
- Several candidate meshes, none verified → stop making new ones. (Ch 5)
- Vision QA returns high confidence with no API key → fake PASS. (Ch 9)
- Proof chip aspect ≠ bounds aspect → stretched tile-edge read. (Ch 4)
- Flat-looking slope on an outline over street → outline median, not raised cells. (Ch 4)
- Dark roof reads 10–20° → returns on HVAC; check where steep cells sit. (Ch 4)
- "13 lots" under one building → stacked tax accounts; dedupe PARCELID. (Ch 4)
- All-white Lit viewport in UE → exposure, not a missing mesh; Unlit checker ≠ missing Z. (Ch 10)
- `ping` fails but SSH works → ICMP blocked, host is up. (Ch 10)
- WMI says 4 GB VRAM → WMI bug; trust `nvidia-smi`. (Ch 10)
- Scaffold says 661 frames @60 fps → it's 22 s @30 fps; MRQ output 60, keys at 30. (Ch 9)

## Route matrix
| | Geometry lock | Look quality | Needs | Licence risk |
|---|---|---|---|---|
| A Wan Fun-Control | depth-locked mass | photoreal | measured geometry + 1 matching photo | low (Apache-2.0, own data) |
| B real-photo splat | real pixels | crisp | many posed photos | low — to verify |
| C Marble | generated | good | photos | surroundings only |
| D free-form i2v | none | fast | 1 photo | gate mandatory; spend needs go |
