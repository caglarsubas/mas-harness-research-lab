# LOCK-PAGES-RL-1: the research.html redesign on the shared sheet (the owner's option A, page 2 of 3), 2026-11-16

RL-PAGES-DONE | ask: verify the claims and checkpoint; relay section 4 to Design-UX and section 5 to the visionary | needs: monitor | by: this lock's checkpoint
Research-Lab, 2026-11-16, on MON-PAGES-RL-1 (the owner, verbatim: "our html files (roadmap.html, architecture.html and research.html)
are not polished and designed well enough to be followed by user much more friendly and easily"; the owner chose "A. Full redesign
(Recommended)"). Inputs, all read from a git-archive export of the bridge at e45c3e1d: design/pages/DUX-PAGES-SPEC-1.md sections 1
(L1 to L4), 2 (S1 to S10) and 4; design/pages/PAGES-UX-2-REPORT.md notes 1, 5 and 6; visionary/PAGES-PREP-56.md section P1;
visionary/LOCK56-ROADMAP-PAGE.md; the shared sheet design/tokens/pages.css 0d9cbfe28df8cf9e; design/pages/glossary-families.md;
roadmap/page_roadmap.py (the reader function and the top bar, mirrored). Work on the export, then applied on the bridge tree with no
commit; pre-lock copies kept in the lab's scratch. No network, no heavy run, no agent.

## 1. What changed (presentation only)

- research/build_research.py 2f09c716 (was 67c32b61) keeps every source reader and the data record as they were. It inlines the sheet
  unchanged in the first style block, with the digest prefix in `<meta name="pages-css">` and in the block's first comment, and fails
  closed without the sheet or without the glossary file (P1 condition 1). The page-own rules follow in a second block and use the tokens
  only; the builder refuses a colour literal and any size under 12 px in them. Two new modes: `--page-only` renders the page from the
  existing research.json and history.json (the lock's mode: the data files stay byte-equal), `--check` renders the same way in memory
  and prints SAME or DIFFER. A normal run still rebuilds the record and the snapshots.
- The page is script-free. Views open by `:target` (the five tabs are links to `#v-start`, `#v-experiments`, `#v-hypotheses`,
  `#v-approach`, `#v-history`; Start here shows while nothing is targeted, a `:has()` rule hides it otherwise); each experiment and each
  hypothesis has a detail panel `aside.pg-panel.is-target` with the id `RL-nn` or `H-nn`, opened by its row's name link and by any
  `#RL-nn` or `#H-nn` link, a side panel on a desktop and a full-screen sheet at 860 px and below; Close returns to the view. The colour
  mode is the sheet's three radios (report note 5). The old `onclick` handlers (56) are gone.
- Start here (S2, spec section 4): the state word and one line (the lane's status word, then the newest dated milestone of the lane
  header with its fingerprints removed); Waiting on you (the hypotheses whose register status is BLOCKED on an owner answer, each with
  an Open button to its panel; "nothing" when none); the hypothesis numbers (with an experiment, ready, blocked; every count a link
  to the Hypotheses view); the last finished experiment in one sentence (the latest completed by run date, its verdict line); the cost
  to date (the register's effort column, rule J, recorded from RL-23 on; earlier rows carry none, and the line says so); the
  experiment counters; the status note cut to three lines with "Show the full note".
- Experiments: one line per row (title, code, the hypotheses tested, state, verdict, last run date); the detail holds the facts, the
  report sections, the claim verdicts and, closed by default, the checks and Evidence. Evidence carries the register entry and every
  file with its sha256 prefix: the fingerprints that stood in the old row's running text (the old page had 1,072 of them) sit there.
- Hypotheses: one line per row (statement, code, kind, stream, status, experiments); the detail holds inputs, first step, P/E score,
  the two outside ranks, the status chip, the experiments, and the register's status note closed by default. Milestones follow.
- Approach: the charter's lead open, each section, the tools, the reads and "How to read a verdict" closed by default; the glossary
  at `#gloss`, which the top bar's Glossary button opens.
- History: the snapshot table, then the resume log: the preamble and the ten newest entries closed by default, and the whole block,
  every dated entry newest first, on a new page research/resume-log.html 70a10942 (151,984 bytes; the same frame and sheet). This is
  the one demotion out of research.html: the old page carried the whole block as a 113 KB `pre`, which the 0.45 MB budget cannot hold
  beside the sheet and the detail panels. Every word of it is one click away on a page in research/**.
- Fingerprints in prose that is not the lab's to reword (the register's cells, the reports' sentences, the charter) are set as code,
  small monospace, by one rule in `inline()`: an 8-to-64-character hexadecimal token with a digit and a letter. They do not stand as
  running text; they are not moved out of the sentences that cite them.
- The top bar is the sheet's (S1): Roadmap and Architecture link to ../roadmap/roadmap.html and ../roadmap/architecture.html, Research
  is current; Updated shows the record's generatedAt; Glossary; the mode radios. The footer names the sheet's digest prefix.

## 2. The budget and the shape

- research.html 446,340 bytes (the old page 432,343; the sheet adds 21,767), 7,212 elements, all static; at most 450,000 bytes holds.
  resume-log.html 151,984 bytes beside it. The data record research.json 07caf2bd (400,850 bytes) and history.json e70697af are
  untouched by the lock's `--page-only` build.
- A later full build (the next lab milestone) rewrites the record with a new generatedAt and lists this paper under reads; the page
  grows by that much. RL-23's report at the stop date adds one panel.

## 3. Renamed labels (S3; the stored word stays in the record and in every quoted sentence)

Overview -> Start here; Hypothesis register -> Hypotheses; Resume log and history -> History; COMPLETED -> Finished; ONGOING -> Running;
PLANNED -> Planned; PASS -> Pass; FAIL -> Fail; UNRESOLVED -> Unresolved; pending -> Pending; RUN -> Tested; READY -> Ready;
BLOCKED -> Blocked, or Waiting on you when the register status names an owner answer; SUPPORTED -> Supported; CONTRADICTED ->
Contradicted; NEW_VALUE_ESTABLISHED -> New value; INCONCLUSIVE -> Inconclusive; PAUSED -> Paused; ACTIVE -> Active; "Files (sha256
prefixes)" -> Evidence; "Where the programme stands" -> Where the lab stands; "What waits, and on what" -> Waiting on you and Blocked;
"Living roadmap" -> Roadmap; "Architecture map" -> Architecture. The two hypotheses that wait on the owner today: H-21 and H-33.

## 4. Glossary: the research families (for Design-UX, from number 21; the wording is the lab's)

| # | Family | Key | Sentence |
|---|---|---|---|
| 21 | Experiment | `experiment` | one preregistered study in the lab's folder, frozen before any run, with its run records, verdict ledger and report. |
| 22 | Hypothesis | `hypothesis` | one falsifiable statement of the register, with the experiments that test it and its status. |
| 23 | Milestone gate | `milestone-gate` | a decision gate of the programme that closes on a verdict of its lead hypothesis, never on a date. |
| 24 | Claim | `claim` | one clause of a hypothesis that an experiment's ledger judges supported, contradicted or unresolved. |
| 25 | Check | `check` | one deterministic test of a verdict ledger, with its bound and the value it measured. |
| 26 | Stream | `stream` | the research roadmap stream a hypothesis belongs to, with its heavy-queue class in brackets. |

The page marks a code with `.pg-term[data-g]` where it stands beside its plain name (an experiment's and a hypothesis's row and panel
header, the stream in a panel, a milestone); claim and check ids in the ledger tables are plain code. The builder carries these six
sentences, sets one rule per family and lists them under Glossary; it reads the glossary file at build time and fails closed when a
research row there differs from them, and reports the rows still missing (six today, none after Design-UX adds them; the page's bytes
do not change when they land).

## 5. The R13 mirror (for the visionary's SCOPE-292-READ; a proposal on paper)

R13 (mas-harness-research-lab) carries research/build_research.py and has no design/ tree, so the sheet-reading builder fails closed
there. Proposal, the monitor's lean made whole: LAB-SYNC-002 (the 292 rider) carries the two files the builder reads, at the same
relative paths, byte-equal and digest-pinned in the packet's expected evidence and in research/MANIFEST.json: design/tokens/pages.css
(0d9cbfe28df8cf9e) and design/pages/glossary-families.md (its digest at the sync's bridge commit, after Design-UX's rows land). The
sync's allowed paths widen from research/** by those two paths; the lab's make_manifest.py and manifest_check.py list them beside
research/** (a lab change in the same packet, claims by script). A sheet change is then one LIGHT lock on the bridge and one rider on
R13, as P1 condition 2 says; until the sync merges, the bridge page leads and R13's page lags, as the monitor said. Two limits to
state: the top bar's Roadmap and Architecture links point at ../roadmap/, which R13 does not carry (they stay, as the sheet's S1
markup wants them; a reader of the mirror sees a missing page, not a wrong one), and research/resume-log.html is a fourth page file
in research/, so the verifier's PAGE_FILES list may need it named (Q-PAGES-RL-1 for the visionary; the lab does not read the verifier).

## 6. The claims (claims_pages_rl.py 2b886c0f in the shared folder; 25 lines of ok, PASS, on the export and on the tree)

- Builder reproducible: `--check` SAME on the export and on the tree (two renders of the same record byte-equal).
- Data files byte-equal: research.json 07caf2bd and history.json e70697af before and after.
- Coverage: every word of the old page (6,893 distinct words after the tags, code marks and bold marks are dropped) is on research.html
  or resume-log.html, or is a renamed label of section 3; 29 old words are truncation fragments (the old page cut a register line at
  220 characters and a statement at 140) whose full word is on the new page; every old experiment row id has its detail; one row and
  one panel per experiment (24) and per hypothesis (44); every hash link on the page resolves to an id (73).
- No request of its own: no script, link tag, import, url() or address on either page.
- Privacy: 0 names, 0 legacy term, 0 paths, 0 addresses on both pages and the builder (the old page 0/0/0/0; through privacy_scan only;
  no name token typed).
- The sheet inlined exactly, first style block, its digest in the meta tag and the comment; the page-own rules carry no colour literal
  and no size under 12 px; every data-g on the page has its rule; the glossary list equals the rules; the sentences obey the file's
  rules (at most 140 characters; no quote, backslash, backtick or bar).
- Fingerprints sit under Evidence in every experiment detail; none in running text outside details, tables, code and the owner's status
  note, which the spec keeps as it is.
- Size: 446,340 bytes, at most 450,000; five views and five tabs; the Start here parts present.
- design/tools/pages/pages_css_check.py against the sheet, the tokens, Design-UX's sample and both built pages: PASS.

## 7. Checks beside the claims (the built-in browser, served from a scratch copy; nothing in the repository)

Light and dark (the Dark radio turns the background to the dark surface token); 1280 by 800: Start here first, the Experiments view by
its tab, the RL-23 panel at 420 px beside the list with Evidence closed; 375 by 812: no sideways scroll (scrollWidth equals the viewport
on both pages and with a panel open), the smallest text 12 px, the smallest tap target 44 px (20 measured), the H-21 panel a fixed
full-screen sheet, the tabs one scrolling row; no console error on either page; resume-log.html lists the 43 entries.

## 8. Not claimed

No change to any record, report, register row or charter text; no wording change to the owner's status note (a content request);
nothing about architecture.html (lock 57); the mirror proposal of section 5 is a proposal, and the verifier's page list is a question.
