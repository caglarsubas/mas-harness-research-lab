# mas-harness-research-lab

The research and development line of the harness programme, recorded as evidence: a hypothesis
register, preregistered experiments with evaluator-computed verdict ledgers, one-page reports,
reading notes and the living research page.

Everything here is evidence and proposals, never authority. The product repositories and the
roadmap live elsewhere; this repository mirrors the lab's `research/**` tree from the programme
bridge, byte for byte, at the bridge commit named by `bridgeCommit` in `research/MANIFEST.json`.
Links into other bridge folders (`handoff/`, `roadmap/`) do not resolve here.

## Layout

- `research/README.md` — the lab's charter: what it owns, how an experiment runs, the
  verdict-ledger form, the rules it works under.
- `research/hypotheses/REGISTER.md` — every hypothesis `H-nn` with its status and the experiments
  that tested it.
- `research/experiments/RL-nn/` — one folder per experiment: `PREREG.md` (frozen before the run;
  earlier versions as `PREREG.v*.md`), `PREREG-REVIEW.md` (from RL-14 on), `runs/` and `data/`,
  `RESULTS.json` (the verdict ledger) and `REPORT.md` (one page).
- `research/tools/` — the evaluators and helpers, standard library only. `make_manifest.py` and
  `manifest_check.py` maintain and verify the manifest.
- `research/reads/` — reading notes and design drafts (the repository plan, packet drafts).
- `research/progress/` — progress notes.
- `research/research.html`, `research/research.json`, `research/history.json` — the living page,
  built by `research/build_research.py`.

## Checking the tree

```
python3 -I -B research/tools/manifest_check.py research/MANIFEST.json
```

Every file is listed by sha256. The check fails on a missing, unlisted or changed file, on a
symlink, on bytecode and on a `.github` directory.

## Filing issues

Open one GitHub issue per finding. Name the file by its repository path and the first eight hex
digits of its sha256 from `research/MANIFEST.json`, the hypothesis (`H-nn`) or experiment (`RL-nn`)
it concerns, what you expected and what you found. Issues are triaged by the programme's lane
monitor and routed to the lab; each receives an ACCEPT, PARTIAL or REJECT note before it is closed.

## Rules

- Standard library only, run as `python3 -I -B`; the programme pins CPython 3.12.
- No `.github` directory and no hosted workflows, ever (the programme's zero-bill rule).
- No personal data, local paths or credentials in any file.
- License: Apache-2.0 (see `LICENSE`).
