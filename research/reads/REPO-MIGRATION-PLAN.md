# Research-Lab repository: migration plan on paper (draft 2, 2026-11-06; nothing committed or pushed before the monitor's word)

Status (2026-11-07, MON-RL-R13-MAIN and MON-RL-R13-FREEZE): the first commit happened on the owner's direct word as R13
main cc92594d6daa (research/** from bridge a67b90a5, README.md, LICENSE, .gitignore, the manifest tools and
research/MANIFEST.json; 236 files), recorded as the owner's initial commit; main stays there until bundle v7 serves R13,
the lab works on branches only, and LAB-REPO-001 (draft 5) re-keys on that base. Section 1 below is kept as drafted.

Owner proposal (2026-11-06, in the lab's chat): a lab repository to push and PR progress, with gpt-astra's feedback
as issues. Open owner decisions: what gpt-astra is and its access; verifier-numbered or plain; public or private.
The monitor's conditions: this plan before any commit; the repository added to issue tracking and lanes.json; the
visionary records it under a lock; the bridge's checkpoint keeps only the page and a digest manifest.

## 1. The first commit (one commit, by the lab, after the owner creates the empty repository and the monitor's word)

- `research/**` as it stands on the bridge at that moment, byte for byte: README (charter), hypotheses/REGISTER.md,
  experiments/RL-01..RL-22 (every PREREG version, review record, run record, data, RESULTS, REPORT), tools/*.py,
  reads/*.md, progress/*.md, build_research.py, research.html, research.json, history.json.
- `MANIFEST.json`: every file's path and sha256 at the first commit, plus the bridge commit the files came from, so
  the move loses no digest: every digest named in a register row, a report or a milestone message stays checkable.
- `README.md` at the root: what the repository is, the procedure (charter 1a), the PR flow (section 3), the issue
  triage rule, and that the bridge's page is a mirror.
- No `.github/workflows` file, ever: the zero-bill rule bans hosted workflows in every repository and the owner's
  verifier refuses them (the monitor's correction, 2026-11-06). Acceptance runs as the packet's offline commands under
  the verifier, like the other repositories: the privacy scan, the register and page build, and every experiment's
  evaluator re-run on its pinned data (standard library; seconds). The commands are listed in the repository's
  activation authority, as the R00 packet that registers the repository and the verifier extension defines them.
- No history rewriting: the bridge's git history of research/** stays on the bridge (the monitor's checkpoints); the
  repository starts at its first commit with the manifest as the bridge-to-repository link.

## 2. How research/** moves without losing history or digests

1. The monitor checkpoints the bridge first (the last bridge copy of research/**, by commit).
2. The lab makes the first commit from that exact tree and records the bridge commit in MANIFEST.json.
3. The monitor changes the checkpoint: the bridge keeps `research/research.html`, `research/research.json`,
   `research/history.json` and `research/MANIFEST.json` (copied from the repository at each lab PR merge), nothing else.
4. The lane file (`handoff/LANE-RESEARCH-LAB.md`) stays on the bridge and names the repository and its head.
5. Every digest already published in milestone messages and the register refers to file bytes, which do not change
   in the move; MANIFEST.json proves it.

## 3. The PR flow (one branch per unit of work; the owner or gpt-astra may review; the lab merges on the monitor's word)

- One PR per experiment, in the charter's order: (a) PREREG and PREREG-REVIEW (the independent review record) merged
  first, so the preregistration is public before the run; (b) the run record, data, RESULTS, REPORT, the register
  row, the scope's progress document, the rebuilt page. A design read or a fetch record is its own PR.
- PR body: the scope, the hypothesis, the verdict, the digests, and "as preregistered" or the deviation.
- Issues: gpt-astra's and the owner's feedback. Triage within the next lab turn: FIX (a new PREREG version before a
  run, or a new experiment id after one; never a re-tune under the same id), DECLINE (one-line reason), or ROUTE (to
  the visionary through the monitor when it touches the roadmap). Each issue is linked from the record it changed.
- Nothing is pushed while the owner's pause holds; heavy runs, fetches and new exports keep needing the monitor's word.

## 3a. The repository's place (the monitor, 2026-11-06, after the visionary's read)

- The repository is R13 (kind meta, no plane). R00 registers it at slot 282 with MET-VERIFY-007; bundle v7 (one
  owner install) carries R13's verifier row and a self-retiring first-packet route.
- Before the bridge takes its mirror form, the page build changes: every link the page makes into `experiments/`,
  `reads/`, `progress/` and `tools/` points at the repository (its main branch at the commit the page was built from,
  recorded in research.json), or is dropped; the bridge copy of the page then links out, never into a tree the bridge
  no longer holds. Bridge claims read the lab's digests from MANIFEST.json.
- These are lab tooling changes, made on the monitor's word with the first commit; the pause holds until then.

## 4. The owner's decisions (2026-11-06, in the lab's chat, verbatim in part)

- gpt-astra: "another llm-provider's github app which have the right of reading the repository and opening issues"
  (read access and issue creation; no write).
- "not a plain repository, we should behave like other sessions": verifier-numbered, the App installed, the entry in
  the verifier (likely folded into bundle v7 with MET-VERIFY-007, per the monitor), acceptance as offline commands
  (section 1); the monitor numbers it under the session map.
- Order (the monitor, 2026-11-06): the visionary's design read; the R00 packet that registers the repository and the
  verifier extension; the owner's install, App access and ruleset; then the lab's first commit on the monitor's word.
- "public".
- Created: `<owner>/mas-harness-research-lab` (the owner's GitHub namespace; the handle is not written here). The
  first commit follows the monitor's word, after its checkpoint, the lanes.json entry and the visionary's lock.
