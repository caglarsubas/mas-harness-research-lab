# Glossary families of the bridge pages

Every code on a bridge page belongs to a family, and every family has one sentence that says what the code is.
A page shows that sentence when a reader hovers over a code, reaches it with the keyboard or taps it, and it
lists the same sentences in its glossary. This file is the one list of families.

- Owner of the list, the keys and the layout: Design-UX.
- Owner of the wording: Roadmap-Visionary. The sentences below are copied character for character from
  section P3 of `visionary/PAGES-PREP-56.md`. A wording change is made there first and copied here by script.
- Owner of the research wording: Research-Lab. The research rows are copied whole from section 4 of
  `research/reads/LOCK-PAGES-RL-1.md`. A wording change is made there first and copied here by script.

## How a page uses the list

1. The plain name comes first. The code follows it as
   `<span class="pg-term" tabindex="0" data-g="KEY">CODE</span>`.
2. The page sets the sentence once per family in its own style block, as family name, colon, sentence:
   `.pg-term[data-g="KEY"]{--pg-tip:"FAMILY: SENTENCE"}`. The shared sheet shows it on hover, on keyboard
   focus and on tap; below 640 px it shows as a note at the bottom of the screen.
3. The page lists the families it shows in its glossary (`dl.pg-gloss`: the family as the term, the sentence as
   the description), in the order of this file.
4. A code whose family is not in this file carries no mark until the family is added here.
5. A page may use any family of any table. A family has one key and one sentence on every page.

## Roadmap families (14)

| # | Family | Key | Sentence |
|---|---|---|---|
| 1 | Item code | `item` | one planned piece of work on the roadmap; the code names its family and a number, and the rank and score belong to it. |
| 2 | Question | `question` | a decision put to the owner through the lane monitor, numbered by the slot or paper that raised it; its answer becomes a decision. |
| 3 | Decision | `decision` | the owner's answer in the owner's own words, with its date and the slot or paper it came from; the roadmap changes only through one. |
| 4 | Monitor message | `monitor-message` | a numbered instruction or ruling from the lane monitor, the one channel between the owner and every session. |
| 5 | Convention | `convention` | one of the numbered working rules of the factory, kept in the conventions file with who set it and when. |
| 6 | Layer count | `layer-count` | K, the number of chain layers (packets) one slot adds to the history chain; K 0 is machinery only. |
| 7 | Harness | `harness` | one of the sixteen capability areas of the platform, each owned by a plane and realised by deployables. |
| 8 | Repository | `repository` | one of the programme's fifteen numbered code repositories; harness-onion holds the contracts and the chain. |
| 9 | Plane | `plane` | one of the four layers of the architecture that own the harnesses; the management surface sits across them. |
| 10 | Release gate | `release-gate` | one of the three qualification checkpoints before the first release; the release path is derived from their dependency closures. |
| 11 | Priority band | `priority-band` | the item's urgency from the specification, P0 to P3, shown beside the rank; the rank itself comes from the score. |
| 12 | Status word | `status-word` | the item's stored state, shown as a plain label; Waiting on you means the item waits on the owner's answer or approval. |
| 13 | Fingerprint | `fingerprint` | the first characters of a file's or commit's hash, pinning the exact version a line refers to; it sits under Evidence. |
| 14 | Pull-request number | `pull-request` | the change that merged a packet into a repository; the verifier's check run and the merge record hang off it. |

## Architecture families (6)

| # | Family | Key | Sentence |
|---|---|---|---|
| 15 | Deployable | `deployable` | one runnable unit of the platform in the service catalog, with its owner repository, state mode and dependencies. |
| 16 | Service edge | `service-edge` | one dependency between a deployable and another deployable or an external, with its transport, timeout and retry. |
| 17 | External | `external` | a system the platform depends on but does not ship, such as the cluster API or a tenant's data source. |
| 18 | Startup wave | `startup-wave` | the order in which deployables start, each wave with its objective. |
| 19 | Evidence state | `evidence-state` | how far a record or deployable is proven, from planned, through a contract adopted, to implemented. |
| 20 | Contract record | `contract-record` | a merged harness-onion record the page reads as data, such as the service edges or the capability evidence matrix. |

## Research families (6)

| # | Family | Key | Sentence |
|---|---|---|---|
| 21 | Experiment | `experiment` | one preregistered study in the lab's folder, frozen before any run, with its run records, verdict ledger and report. |
| 22 | Hypothesis | `hypothesis` | one falsifiable statement of the register, with the experiments that test it and its status. |
| 23 | Milestone gate | `milestone-gate` | a decision gate of the programme that closes on a verdict of its lead hypothesis, never on a date. |
| 24 | Claim | `claim` | one clause of a hypothesis that an experiment's ledger judges supported, contradicted or unresolved. |
| 25 | Check | `check` | one deterministic test of a verdict ledger, with its bound and the value it measured. |
| 26 | Stream | `stream` | the research roadmap stream a hypothesis belongs to, with its heavy-queue class in brackets. |

## Rules for a new family

- One sentence, plain words, 140 characters at most, ending with a full stop. The longest today has 132.
- No fingerprint, path, name or address in a sentence.
- No double quote, backslash, backtick or vertical bar in a family name or a sentence, so that the sentence can
  be placed in a style rule and in these tables unchanged.
- The key is the family name in lower case with hyphens, without the words "code" and "number".
