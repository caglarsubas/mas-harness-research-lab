"""RL-15b evaluator (PREREG v1): applies the three-region gate over the catchable denominator, with the visionary's
restated expectation (ERRATUM to RL15-D1: 17 of 18 refused; the RL-15 rules run after load()'s rules, so an instance
that also breaks an older rule is refused there first; at least 2 of 3 M4 and 2 of 2 catchable M6 refused by the new
rules, read by their tag; 0 of 3 controls refused), and writes the verdict ledger.
usage: python3 -I -B rl15b_eval.py RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
import hashlib
import json
import pathlib
import sys


def sha(path):
    return "sha256:" + hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def main(runs_json, prereg, run_record, out_path):
    rec = json.load(open(runs_json, encoding="utf-8"))
    c = rec["counts"]; per = c["perClass"]
    baseline_ok = rec["baseline"]["exit"] == 0
    layout_ok = rec.get("layout", {}).get("work") == "roadmap"
    n, attributed, refused_any, ctrl = c["catchable"], c["attributed"], c["catchableRefused"], c["controls"]
    fp = c["controlsNonZero"]
    crashed = c["seededCrashed"]
    unattributed = c["unattributedRefusals"]
    new_m4, new_m6 = c["newRulePerClass"].get("M4", 0), c["newRulePerClass"].get("M6", 0)
    EXPECT_NEW = {"M4": 2, "M6": 2}  # ERRATUM to RL15-D1: at least 2 of 3 M4 and 2 of 2 catchable M6 refused by the new rules
    not_refused = [(r["class"], r["target"], "crashed" if r["crashed"] else "built") for r in rec["runs"] if r["class"] != "C" and r["catchable"] and not r["refused"]]
    unattributed_rows = [(r["class"], r["target"]) for r in rec["runs"] if r["class"] != "C" and r["catchable"] and r["refused"] and not r["attributed"]]
    false_pos = [(r["class"], r["target"], "refused" if r["refused"] else "crashed") for r in rec["runs"] if r["class"] == "C" and r["exit"] != 0]
    uncaught_class = [k for k, (a, r, m) in per.items() if m > 0 and r == 0]
    new_short = [k for k, want in EXPECT_NEW.items() if (new_m4 if k == "M4" else new_m6) < want]
    precision = (attributed / (refused_any + fp)) if (refused_any + fp) else None
    if not (baseline_ok and layout_ok):
        status, why = "UNRESOLVED", "precondition failed: baseline exit %d, layout %s" % (rec["baseline"]["exit"], rec.get("layout"))
    elif refused_any == n and unattributed == 0 and fp == 0 and not new_short:
        status, why = "PASS", "all %d catchable seeded edits refused and attributed (new rules: M4 %d, M6 %d), 0 of %d controls refused" % (n, new_m4, new_m6, ctrl)
    elif uncaught_class or fp > 0 or (new_m4 == 0 and new_m6 == 0):
        status, why = "FAIL", "; ".join(filter(None, ["class(es) with no instance refused: %s" % ", ".join(uncaught_class) if uncaught_class else "", "%d control(s) refused (false positive): %s" % (fp, false_pos) if fp else "", "neither new rule refused anything" if (new_m4 == 0 and new_m6 == 0) else ""]))
    else:
        status, why = "UNRESOLVED", "%d of %d catchable refused; not refused: %s; unattributed refusals: %s; new rules below the expectation: %s" % (refused_any, n, not_refused, unattributed_rows, new_short)
    value = "catchable refused %d/%d (attributed %d: new rules %d [M4 %d, M6 %d], older rules %d, unattributed %d); uncatchable instance %s; false positives %d/%d; precision %s; per class [attributed, refused, n] %s; baseline exit %d in %.2f s" % (
        refused_any, n, attributed, c["byNewRule"], new_m4, new_m6, c["byOlderRule"], unattributed, c["uncatchableOutcome"], fp, ctrl, "%.3f" % precision if precision is not None else "-", json.dumps(per, sort_keys=True), rec["baseline"]["exit"], rec["baseline"]["wall_s"])
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    led = {
        "schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-15b-RESULTS-v1", "supersedes": None,
        "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
        "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
        "evidence": [
            {"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(runs_json), "producedBy": "Research-Lab.rl15b_mutate.run-001"},
            {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"},
            {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl15b_eval"},
        ],
        "claims": [{"claimId": "H-30b", "requirement": "H-30 restated (RL-15b, ERRATUM to RL15-D1): on the lock-40 builder every catchable seeded inconsistency instance is refused, each refusal is attributed to a named rule (a new rule by its tag, or the older rule that runs first), the new rules refuse at least 2 of 3 M4 and both catchable M6 instances, and no benign control edit is refused",
                    "delivered": value, "rolloutValues": [{"rollout": "run-001", "value": status}]}],
        "checks": [
            {"checkId": "C1", "claimId": "H-30b", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "INTERMEDIATE",
             "establishedValue": "precondition: layout %s; baseline build of the unmodified copy exit %d in %.2f s" % (rec.get("layout"), rec["baseline"]["exit"], rec["baseline"]["wall_s"]), "outcome": "PASS" if (baseline_ok and layout_ok) else "FAIL", "evidence": ["E1"]},
            {"checkId": "C2", "claimId": "H-30b", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 2, "target": "DELIVERED",
             "establishedValue": "catchable refused %d of %d; attributed %d (new rules M4 %d, M6 %d; older rules %d; unattributed %d); per class [attributed, refused, n] %s; not refused: %s; unattributed: %s; bound: %d of %d refused, 0 unattributed, new rules M4 >= 2, M6 >= 2" % (refused_any, n, attributed, new_m4, new_m6, c["byOlderRule"], unattributed, json.dumps(per, sort_keys=True), not_refused, unattributed_rows, n, n), "outcome": "PASS" if (refused_any == n and unattributed == 0 and not new_short) else ("FAIL" if (uncaught_class or (new_m4 == 0 and new_m6 == 0)) else "UNRESOLVED"), "evidence": ["E1", "E3"]},
            {"checkId": "C3", "claimId": "H-30b", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 3, "target": "DELIVERED",
             "establishedValue": "controls refused %d of %d (bound 0): %s" % (fp, ctrl, false_pos), "outcome": "PASS" if fp == 0 else "FAIL", "evidence": ["E1"]},
            {"checkId": "C4", "claimId": "H-30b", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 4, "target": "INTERMEDIATE",
             "establishedValue": "uncatchable instance (declared, excluded from the denominator): %s; refusal messages (validator's words, %s) with attribution: %s" % (c["uncatchableOutcome"], rec.get("capture"), json.dumps([{"class": r["class"], "target": r["target"], "field": r["field"], "exit": r["exit"], "catchable": r["catchable"], "newRule": r["attributedToNewRule"], "olderRule": r["attributedToOlderRule"], "message": r["message"]} for r in rec["runs"]])), "outcome": "PASS", "evidence": ["E1"]},
        ],
        "claimVerdicts": [{"claimId": "H-30b", "checks": ["C1", "C2", "C3", "C4"], "verdict": {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(status, "UNRESOLVED"), "value": value}],
        "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": ["C2"] if status == "UNRESOLVED" else [], "policyViolations": [],
                    "scores": {"catchable": n, "catchable_refused": refused_any, "attributed": attributed, "by_new_rule": c["byNewRule"], "new_rule_m4": new_m4, "new_rule_m6": new_m6, "by_older_rule": c["byOlderRule"], "unattributed": unattributed, "seeded_crashed": crashed, "interpreter": rec.get("interpreter"), "precision_permille": int(round(precision * 1000)) if precision is not None else None, "controls": ctrl, "controls_refused": fp, "classes_uncaught": len(uncaught_class), "baseline_exit": rec["baseline"]["exit"]},
                    "evidenceRefs": [sha(runs_json), sha(run_record), sha(prereg), self_digest]},
    }
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, "|", why, "|", value)


if __name__ == "__main__":
    main(*sys.argv[1:5])
