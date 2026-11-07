# RL-19 preregistration: the syntheses' figures against the five held papers (H-24, the crosswalk's grounding method on a second corpus)

Status: FROZEN v1 (2026-11-06, light; the monitor's RL-M28 reply: "RL-19 is approved as light work (reading the five held papers, no network)"; the lab resumed on the owner's direct word after the 5-hour reset). This file's sha256 goes into the register.

Integrity check before the freeze, by counts only: five files held by digest in the lab scratch from the owner-approved fetches of 2026-11-05 (F2 Agentproof, F4a Harness-Bench, F4b the repeated-running paper, F5 the Nature Machine Intelligence article as open-access HTML, F6 the memory-poisoning paper); a standard-library extractor (PDF text operators after zlib; HTML tags stripped) run once before the freeze as an instrument trial returned 58,204 / 84,961 / 46,794 / 474,327 / 3,244,251 characters for the five and found the probe numbers the lab tried (counts only; no claim list existed then). The claim list (29 claims, `data/claims.json`, sha256 8ee32bfe70cd5659d21b304838f471ba2c6db1fc3f3d268fd82cef30280e76ab) was written after that trial from the three syntheses' text, before any claim was searched.

Researcher degrees of freedom, declared: the lab wrote the claim list and read every paper's first page on 2026-11-05 (titles confirmed), so some figures (the abstracts') were known to be present when the list was written; the list was still written from the syntheses, not from the papers, and includes body-text figures the lab had not seen. The three syntheses were written by outside tools for the owner, independently of this hypothesis (R7); the papers are the authors'.

## 1. Hypothesis (falsifiable)

H-24 (grounding on a second corpus): the figures the three syntheses attribute to the five held papers are found in the papers' own text at a rate of at least 90 percent. Unit: one claim (a figure as a search pattern, a meaning, the syntheses that state it); 29 claims across five papers and three syntheses. FOUND = the pattern (or its formatting variants: without the thousands comma, with a spaced or spelled percent sign) occurs in the paper's extracted text, case-insensitively; NOT_FOUND otherwise. A FOUND claim shows the figure is in the text, not that the synthesis's sentence about it is right; the report reads the context of every FOUND claim whose meaning is specific (a rate, a count with a subject) and marks it VERIFIED or MISREAD by hand, descriptively. Gate, in order: UNRESOLVED when any paper's extracted text is under 5,000 characters or fewer than 20 claims exist (instrument gap); FAIL when at most 70 percent are FOUND; PASS when at least 90 percent; UNRESOLVED between. Minimum effect: a tenth of the figures missing is the level at which the syntheses' figures could not be used as reported in a crosswalk record. Expected outcome class, stated in advance: PASS (the trial's probes, a subset of these figures, were all found).

## 2. Inputs (pinned)

| input | sha256 | origin |
|---|---|---|
| F2 `paper.pdf` (arXiv 2603.20356, 700,203 B) | 9dff38ef1396804f3c4f4d6ed471403f89b04e75336e72fe57a0be80152a23d7 | the approved GET of 2026-11-05 (FETCH-RECORD-2026-11-05, no commit: a fetched file) |
| F4a `paper.pdf` (arXiv 2605.27922, 7,218,628 B) | b2ec0c042c4738cd99ace87150af6ed175c098b39fd24f36b1b6ce141e2b5d34 | same |
| F4b `paper.pdf` (arXiv 2606.00920, 629,978 B) | 8488e9440ac33fca66aece3a956fef9ff728daa9ecf1492b02f39ce3b5fafd9b | same |
| F5 `body.bin` (the Nature Machine Intelligence article page, 475,030 B) | b3a379894adc96b9afb9d2aedddfde85b0b53787f013111911d540aae06741e9 | same |
| F6 `paper.pdf` (arXiv 2606.04329, 4,981,471 B) | 36999ed0cb2d15b93897fa1f8be9ff2291516b633889e16e377f19db4288f482 | same |
| `data/claims.json` (29 claims as reported by RS-1 61fa9041, RS-2 5b30977b, RS-3 930f89a0) | 8ee32bfe70cd5659d21b304838f471ba2c6db1fc3f3d268fd82cef30280e76ab | the lab, from the three syntheses' text |

## 3. Design and compute (the lab's instruments, frozen)

- Extractor and matcher `tools/rl19_figures.py`, sha256 4506c09180faf0d5530301ec6608c5c084c01bddb38d4b1443bbbd333589efbd: writes `data/rl19_runs.json` (per claim FOUND or NOT_FOUND, occurrences, up to 12 words of context around the first occurrence, a short quotation as the crosswalk's grounding records keep; never the papers' text).
- Evaluator `tools/rl19_eval.py`, sha256 5b9f77ca8b41258986288550ef9b3b8f1d160f6860460239276987b070f54fc7: the gate and `RESULTS.json`, naming its own digest. Both are the lab's instruments on the bridge working tree, no commit of their own, custody by these 64-character digests; a change after this freeze is a new PREREG version.
- Compute: light, this host, standard library, CPython 3.12.4, `python3 -I -B`, seconds (the 7 MB PDF's streams decode in under a minute); deterministic; no network; stream S4, queue class X; no ECU.
- Privacy: `privacy_scan.py` over every file of the folder before the report; the context snippets are the papers' words (published), no person's data of the programme.

## 4. What is PASS, FAIL, UNRESOLVED

As the gate in section 1; a FAIL or UNRESOLVED is recorded as the finding; no edit of the claim list under this id.
