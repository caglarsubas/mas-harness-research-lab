# RL-20 report: a static checker over the TopologySpec vectors (H-25, TopologySpec half, 3 of 5 classes)

**Asked.** Does a static checker written from MAS-RA-004's README reproduce the record's 52 topology vectors (H-25a),
and does the record refuse, with its own code and a witness, the three register classes the TopologySpec form can
express (cycle, unreachable node, budget escape), seeded once each on the 8 valid vectors, while accepting the valid
vectors (H-25b)? Preregistered as v1 (4f12f24f), reviewed once (PASS). The verdict is for H-25's TopologySpec half
and three of its five classes; the other two ("two writers", "unapproved effect path") the form cannot express.

**Measured.** Run-001 37bd0922; data c6ee93f7; RESULTS e4c282b7. H-25a: the lab's checker agrees with all 52 topology vectors
(8 accepted, 44 refused with the expected code), including the baseline-record checks of MAS-RA-002 the selection
rule needs. H-25b: 21 of 22 gated edits refused with the expected code and a witness; all 8 valid vectors accepted;
the two decentralized "unreachable" edits (not gated) were accepted, as the record has no reachability rule for
peers. One gated edit was accepted: the budget edit on the one-node SINGLE_AGENT vector, where the construction
(agentBudget = max(1, nodes - 1)) yields 1, equal to the node count, so no escape was seeded.

**Verdict: FAIL as preregistered on H-25b** (one gated edit accepted); H-25a PASS. The gate counts the accepted edit
as the record failing to refuse; the cause is the lab's edit construction on a one-node topology, which the review
foresaw. The record's rules are not contradicted: a one-node topology cannot have a budget below one node. No
re-tune under this id; a v2 with that edit excluded (21 gated) is a new id, if the lab wants the clean count.

**What it means.** The TopologySpec form, as published, already refuses the expressible classes by construction:
cycles are bounded by the depth-1 rule (a DELEGATE back-edge is MODE_STRUCTURE in every mode; MESSAGE cycles among
peers are allowed by design), unreachable nodes are refused in CENTRAL (the coordinator must delegate to every node)
and SINGLE_AGENT (no second node), and budget escapes are BUDGET. Two things the form does not do, for
GRAPH-COMPILE-001: it allows an isolated peer on a decentralized board (no reachability rule for peers), and it
carries no per-item writer and no effect marker, so "two writers" and "unapproved effect path" cannot be checked on
a TopologySpec; they need the WorkPlan and strategy records (BLOCKED) or the authority map. The lab's checker is a
second implementation of the record's rules that reproduces every vector, which is what MAS-RA-004's README promises
of any consumer (H-23's clean-room question, in part).

**What it does not show.** Nothing about the WorkPlan and strategy halves; the edits and the checker share an
author; one edit per class per vector; "witness" is the refusing rule's named object, not a trace.

**Proposal.** None as a roadmap read. Input for GRAPH-COMPILE-001's design note (through the monitor): the three
expressible classes are covered by MAS-RA-004 as it stands; the checker's new work is the WorkPlan and strategy
layers (writers, effects, budgets across plans) and, if wanted, a reachability rule for decentralized peers.
