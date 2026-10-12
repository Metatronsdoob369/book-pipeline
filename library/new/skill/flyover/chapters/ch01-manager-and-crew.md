# Chapter 1: Manager role, crew, and cards

**Sources:** `Manager — Start Here.md` L2–60 · `Crew.md` L2–45 (crew defined 2026-10-08)

## Core Idea
The main session is the **manager**: it turns the Commander's goals into routes and task cards, hands tool work to three specialists (Scout, Shot Maker, Verifier), judges their artifacts, and is the one voice to the Commander. Nothing reaches the Commander unverified.

## Frameworks Introduced
- **Doctrine (manager version)** (Manager L14–17): "Measured skeleton: never invent geometry or numbers. Generated skin. Checked truth: nothing reaches the Commander unverified."
- **Roles table** (Crew L6–13):
  | Role | Owns | Never |
  |---|---|---|
  | Commander (Joe) | vision, taste, money/creds/outward calls | — |
  | Manager | goals → routes → task cards; judging results; one voice to the Commander | sits in tool logs; ships anything unverified |
  | Scout | finding and **measuring** sites: parcels, footprints, lidar, heights, roof sq ft, photo availability | generates imagery; invents numbers |
  | Shot Maker | camera paths, guides, generation, heals, music, cut | decides what's true about a building; grades its own work |
  | Verifier | independent checks of every Scout and Shot Maker result | edits the work it judges |
- **Why three and not five** (Crew L15): every hand-off loses context; camera, overlay and render share the same files and the same 8 GB GPU (one job at a time), so they are one role. Checking is split out "so nobody grades their own homework."
- **Flow** (Crew L40–41): Manager writes the card → Scout measures → Verifier checks → (Shot Maker builds → Verifier checks) → Manager decides and shows the Commander pictures and numbers.
- **Task card** (manager → specialist, Crew L19–27): `TASK <site>-<n> to:` + `goal` (one sentence, in the buyer's terms) · `inputs` · `outputs` (exact files and where) · `done when` (measurable bar, e.g. "every row has a proof image; truth gate HELD") · `limits` (time / GPU / no paid APIs).
- **Result card** (specialist → manager, Crew L29–38): `RESULT <task id> status: done | partial | blocked` + `artifacts` (images first) · `numbers` (the few that matter) · `verdict` (one line) · `problems` (each with an evidence path) · `lessons` (what was appended to the Playbook). Verifier returns **PASS / FIX / FAIL**, a claims table (confirmed / wrong / unverified) and evidence images.
- **Task board** (Manager L36–39): Status is exactly one of `queued · running · verifying · blocked · done`; details go in **Note**, never in Status (Kanban views parse the table). "The board is the only state that survives a session."

## Key Concepts
- **Commander**: Joe / Preston (Marsh Press); sets vision and taste. Manager decides and executes technical work (Manager L6–7).
- **Escalate only**: money, credentials, outward actions (emails, posts, PRs), permission gates (Manager L8).
- **Update format**: short; lead with "visible change: none" or "what + where"; at most one batched question; no option menus; show pictures and numbers (Manager L9–13).
- **Charters**: `~/.claude/agents/nodrone-{scout,shotmaker,verifier}.md`; launch via Agent tool `subagent_type: nodrone-scout` etc. If types don't show (needs restart after file change), use `general-purpose` with "read your charter at <file> first" (Manager L19–28).
- **Shared state**: the Hive (Playbook, Capability Atlas) + site folders under `C:\Projects\flyover\sites\`. GPU refereed by GPU Guardian (`gpu run`). No message broker — add one only for many agents or machines (Crew L17).

## Mental Models
- Ask the **buyer-level question first**: is the input any good? Who pays, and what do they need to see? (2026-10-08: three rounds polishing lidar before anyone noticed 109 of 207 "leads" were vacant lots — Manager L31.)
- Stay out of the logs and **judge the artifacts** (Manager L32).
- Think of every session as mortal: **anything long runs resumably**, cached per item (Manager L33).

## Anti-patterns
- **Relaunching without proof of death**: "Before relaunching anything, prove it is dead." Check `ps -ef | grep <script>`, output timestamps, the agent's own status; an empty output folder is NOT proof. 2026-10-08: two Scouts edited the same file; background agents can outlive the terminal (Manager L52).
- **Card says running, nothing running**: check `pgrep -af`, output timestamps, git log in the worktree, then relaunch — scripts are resumable (Manager L53).
- **Specialist grading its own work**; manager sitting in tool logs.
- **Perfecting a finished stress test**: last film (Burj) is "done; don't keep perfecting it" (Manager L60).

## Key Takeaways
1. Every piece of tool work goes out as a task card with a measurable "done when" and comes back as a result card with images first.
2. Every Scout and Shot Maker result passes the Verifier before the Commander sees it.
3. Update the task board on every card out / card back; it is the only cross-session state.
4. Prove a process dead before relaunching; give one file to one live agent (see ch04).
5. Updates to the Commander: visible change first, pictures and numbers, ≤1 batched question.

## Connects To
- **ch02**: routes and tools the manager picks between.
- **ch04**: per-role lessons for Scout / Verifier / Shot Maker.
- **ch05**: why "checked truth" exists (failure records).
