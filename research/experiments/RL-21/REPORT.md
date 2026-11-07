# RL-21 report: one writer per governed state, as the published authority records express it (H-26, contract-text half, creator-linkage operationalisation)

**Asked.** In harness-onion's published authority records at c1b838be: is every path under `architecture/` created by
exactly one packet authority (H-26a), and does every later change to such a path name its creator among the changer's
own baseline packets (H-26b)? Descriptively, how is ownership by the meta authorities laid out (H-26c)? Preregistered
as v2 (9eb03897) after v1 passed review but its chain rule proved uncomputable from the export; the overall verdict
rests on H-26b, since H-26a's count was seen in the inventory (review 2 note 1). Scope: the contract-text half under
this operationalisation, not the register's whole clause (revocation is RL-07's pinned-byte refusals; the board
traces wait on MAS-RA-009).

**Measured.** Run-001 62a328dd; RESULTS 82450439. 114 authority records: 92 packet authorities, 22 meta authorities. H-26a:
1,547 paths created, none created twice. H-26b: of 16,415 changed-file entries, 4,335 change paths created inside the
export and every one of them (4,335) names the creating packet among the changer's direct baseline packets; 12,080
entries change paths outside `architecture/` (docs, scripts, tests), which the export does not hold, and are not
gated. H-26c (descriptive): the meta authorities own 275 distinct paths, 139 of them in more than one generation;
`metaBaseline` is a commit id, so the generation chain is git history outside this export.

**Verdict: PASS** (H-26a PASS; H-26b PASS, 4,335 of 4,335 linked), for the contract-text half under the
creator-linkage operationalisation: one creator per published path, and every published change explicitly built on
the creator. It is not "exactly one writer" in the register's sense: a path may be changed by many later packets,
each naming the creator, which is the chain's discipline (a change names what it builds on), not a single writer.

**What it means.** The published records already carry a writer-of-state discipline for the contracts: creation is
unique and every change is explicitly based, with the identity rule refusing edits to pinned bytes (RL-07). What the
records do not carry is a per-state single writer across time or the authority map the register names; those are
AUTHORITY-MAP-001's design and MAS-RA-009's board. The 12,080 out-of-scope changes show the same records govern
files beyond `architecture/`; a full-repository export would extend the census.

**What it does not show.** Nothing about revocation (RL-07 covers pinned bytes); nothing about runtime writers (the
board traces); nothing about files outside `architecture/`; the chain between meta generations needs git history.

**Proposal.** None as a roadmap read. For AUTHORITY-MAP-001's design (through the monitor): the packet authorities'
`newFiles` and `baselinePackets` already form a creator-and-basis graph over 1,547 published paths with no
duplicate creator; the map can be derived from them rather than written by hand, and the single-writer-across-time
question is the one it would add.
