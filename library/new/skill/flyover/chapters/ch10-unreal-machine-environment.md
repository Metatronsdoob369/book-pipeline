# Chapter 10: Driving Unreal/Blender, the 5820, and the environment

**Sources:** `_flyover-Hub.md` L28–42 (2026-09-15/18), L53–69 (2026-09-08 incl. "Gotchas (cost this session)" L64–69), L79–84, L104 · `Server MCP Environment Audit.md` L2–41 (2026-09-05) · `Inventory — 2026-10-07.md` L2–40 · `INVENTORY_AND_STATUS_QUO.md` L2–80 (2026-09-03, Mac-side; superseded view) · `Manager — Start Here.md` L55–60

**Staleness warning:** machine specs, versions, paths, ports and repo sync states below are snapshots with dates. Re-sweep before relying on them; the inventory note itself says it "supersedes nothing" and lists key NAMES only, never values (Inventory L4).

## Core Idea
Drive engines programmatically from the agent — remote Python into a live editor, or headless CLI — never via a human click-path or OS-level UI automation. Most lost time came from config sections, launch context and transform axes, not from the engines.

## Frameworks Introduced
- **Agent drives, Commander doesn't click** (Hub L60): "Drive the editor from here. Joe is not the Unreal click-path." Also: "Joe does not hunt Z — the Mac writes the transform." (L69)
- **Headless fallback when no live bridge** (Audit L11): UE via `UnrealEditor-Cmd.exe <uproject> -ExecutePythonScript=...`; Blender via `blender -b --factory-startup -P script.py --`. Not through a bridge that hasn't been confirmed alive.
- **MCP reality check** (Audit L4–11): before relying on any MCP, check the client config and port-scan the host. A plugin of authoring guidance (e.g. `unreal-engine-skills-for-claude-code`) is not a callable bridge; name-adjacent MCPs (e.g. `weppy-roblox`) are unrelated.
- **Do not mix lanes** (Hub L28–31): a sidecar experiment (e.g. LCC4Unreal Gaussian splats in the same UE project) stays labelled as experiment, not product.

## Unreal gotchas (Hub L64–69, 2026-09-08)
- **Remote Control ini section**: `URemoteControlSettings` lives in module **RemoteControlCommon**. Files: `Config/DefaultRemoteControl.ini` **and** `Saved/Config/WindowsEditor/RemoteControl.ini`; section `[/Script/RemoteControlCommon.RemoteControlSettings]`. Keys in `DefaultEngine.ini` under `[/Script/RemoteControl.RemoteControlSettings]` are **ignored**.
- **Two gates**: `bEnableRemotePythonExecution=True` unlocks `Default__PythonScriptLibrary` (else error "Object Default__PythonScriptLibrary cannot be accessed remotely…" — "not a human Project Settings hunt"); then the function allowlist / `bAllowAnyRemoteFunctionCall`.
- **Don't launch UnrealEditor from SSH `Start-Process`** — it dies in a non-desktop session; use the scheduled task (`OpenFlyoverUE5`, console session). **`-ExecutePythonScript=` quits the interactive editor** — never use it to drive a live session.
- **Yaw vs pitch**: a building rotation put on pitch made a 23 m building read as a pancake from above.
- **Unlit ≠ missing Z**: Unlit draws a checker plate; all-white Lit was camera exposure into CesiumSunSky after hiding tiles, not a deleted mesh. Kill `r.EyeAdaptationQuality`; frame a 3/4 on the mesh.
- **Trust the viewport over a bad HighResShot** (black-void PNG) (Hub L61).
- **Live editor dirt**: do not save the map while debug materials/lighting are applied; restore materials first (Hub L39). "Do not Save Untitled over" the real map; do not re-import the FBX; "Do not drag the mesh off that pad" once georeferenced (Hub L56–57).
- **Cesium tiles 401** was an empty `access_token` on the tileset — bind the ion token in-editor; tokens never in git (Hub L59).
- **Stop fighting Cesium photoreal colour for a first clip** when it is not the milestone (Hub L36).

## Machine and environment facts (dated)
- **VRAM**: RTX 3070 is **8 GB per `nvidia-smi`**; Windows WMI reports ~4 GB (signed 32-bit overflow) — ignore WMI (Audit L16). 8 GB is RealityScan's stated minimum (10 GB recommended).
- **GPU is shared and refereed**: GPU Guardian `gpu run --vram N --exclusive --name X -- cmd`, dashboard :8790 (Manager L58; Inventory L7).
- **Login surfaces don't unlock each other**: Mac, Windows on the 5820, WSL user — three, not one password; no secrets in Hive (Hub L83).
- **SSH works though ICMP is blocked** — `ping` timing out is not "host down" (Audit L2).
- **Repo sync with Git LFS** (Audit L28–29): no remote; a plain clone of a bare mirror gives pointer files. Transfer with `rsync` including `.git/lfs/`, then `git lfs fsck` + `git lfs checkout`. Treat the WSL copy as live unless proven otherwise (Hub L82).
- **Portable app extracts** (Twinmotion, RealityScan inside the project dir) — licence/activation unverified; confirm before a real render (Audit L20–23).
- **RealityScan** (secondary-sourced, Audit L33–39): free under $1M revenue; real `-headless` CLI with sequenced params (`-load … -selectMaximalComponent … -save … -quit`); RealityScan = RealityCapture rebranded (2.0, June 2025).
- **Paths** (as of 2026-10-08, Manager L55–59): code in the `~/flyover-wt/geodesy` worktree, `engine/*.py`, venv `~/.venvs/flyover/bin/python`; data/renders under `C:\Projects\flyover\sites\…` and `…\renders\…` (WSL `/mnt/c/...`); ComfyUI :8188.
- **Local stack** (as of 2026-10-07, Inventory L10–23): UE 5.8 + `C:\Projects\Flyover_UE5` (Cesium, LCC4Unreal); Blender 5.2 headless; COLMAP 4.2.1 CUDA; ComfyUI with SDXL, ControlNet Union ProMax, RealESRGAN, RMBG; vendored SAM 2, EdgeTAM, PlaneToPBR; Depth-Anything-V2-Small, SegFormer-B4. Sibling projects: `flyover-pipeline` (stills → Marble → orbit → UE), `image-blaster` (image → World Labs world + FAL objects).
- **Python**: on the old Mac the engine ran under `/usr/bin/python3` because Homebrew 3.14 pyexpat was broken (Hub L90).

## Anti-patterns
- Assuming an MCP from a prior session is alive (the claimed Blender MCP on `localhost:9876` was not listening — Hub L104; Audit L10).
- Reading VRAM from WMI. Launching editors from non-desktop SSH. Using `-ExecutePythonScript` on a live editor. Plain `git clone` of an LFS repo.

## Key Takeaways
1. Remote Control Python: right module section, both gates, scheduled-task launch.
2. Verify any bridge by config + port scan; otherwise go headless.
3. 8 GB GPU, one job at a time, through GPU Guardian.
4. Every environment fact is a dated snapshot — re-sweep.

## Connects To
- **ch03** (8 GB budget rules), **ch09** (renderer via MRQ/headless), **ch01** (escalate creds to the Commander).
