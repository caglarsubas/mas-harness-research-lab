"""RL-15 evaluator (PREREG v1): applies the three-region gate to the mutation tool's output and writes the verdict
ledger. usage: python3 -I -B rl15_eval.py RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
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
    seeded, refused_any, ctrl = c["seeded"], c["seededRefused"], c["controls"]
    fp = c["controlsNonZero"]  # PREREG v3: a control's non-zero exit of any kind is a false positive
    crashed = c["seededCrashed"]
    refused = c["seededAttributed"]  # PREREG v2: a seeded edit is caught only when the refusal names the edited item or field
    uncaught_class = [k for k, (a, r, n) in per.items() if a == 0]
    partial = [k for k, (a, r, n) in per.items() if 0 < a < n]
    missed = [(r["class"], r["target"], "unattributed refusal" if r["refused"] else ("crashed" if r["crashed"] else "built")) for r in rec["runs"] if r["class"] != "C" and not r["attributed"]]
    precision = (refused / (refused_any + fp)) if (refused_any + fp) else None
    false_pos = [(r["class"], r["target"], "refused" if r["refused"] else "crashed") for r in rec["runs"] if r["class"] == "C" and r["exit"] != 0]
    if not baseline_ok:
        status, why = "UNRESOLVED", "precondition failed: the unmodified copy does not build (exit %d)" % rec["baseline"]["exit"]
    elif refused == seeded and fp == 0:
        status, why = "PASS", "all %d seeded edits refused, 0 of %d controls refused" % (seeded, ctrl)
    elif uncaught_class or fp > 0:
        status, why = "FAIL", "; ".join(filter(None, ["class(es) with 0 of 3 refused: %s" % ", ".join(uncaught_class) if uncaught_class else "", "%d control(s) refused (false positive): %s" % (fp, false_pos) if fp else ""]))
    else:
        status, why = "UNRESOLVED", "every class caught at least once but %d of %d seeded edits refused; uncaught instances: %s" % (refused, seeded, missed)
    value = "attributed recall %d/%d (any refusal %d/%d); false positives %d/%d; precision %s; per class [attributed, refused, n] %s; baseline exit %d in %.2f s" % (refused, seeded, refused_any, seeded, fp, ctrl, "%.3f" % precision if precision is not None else "-", json.dumps(per, sort_keys=True), rec["baseline"]["exit"], rec["baseline"]["wall_s"])
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    led = {
        "schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-15-RESULTS-v1", "supersedes": None,
        "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
        "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
        "evidence": [
            {"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(runs_json), "producedBy": "Research-Lab.rl15_mutate.run-001"},
            {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"},
            {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl15_eval"},
        ],
        "claims": [{"claimId": "H-30", "requirement": "H-30: the roadmap build's validators refuse every seeded inconsistency class and no benign control edit",
                    "delivered": value, "rolloutValues": [{"rollout": "run-001", "value": status}]}],
        "checks": [
            {"checkId": "C1", "claimId": "H-30", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "INTERMEDIATE",
             "establishedValue": "precondition: baseline build of the unmodified copy exit %d in %.2f s" % (rec["baseline"]["exit"], rec["baseline"]["wall_s"]), "outcome": "PASS" if baseline_ok else "FAIL", "evidence": ["E1"]},
            {"checkId": "C2", "claimId": "H-30", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 2, "target": "DELIVERED",
             "establishedValue": "seeded attributed recall %d of %d (any refusal %d); per class [attributed, refused, n] %s; uncaught: %s; bound: %d of %d" % (refused, seeded, refused_any, json.dumps(per, sort_keys=True), missed, seeded, seeded), "outcome": "PASS" if refused == seeded else ("FAIL" if uncaught_class else "UNRESOLVED"), "evidence": ["E1", "E3"]},
            {"checkId": "C3", "claimId": "H-30", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 3, "target": "DELIVERED",
             "establishedValue": "controls refused %d of %d (bound 0): %s" % (fp, ctrl, false_pos), "outcome": "PASS" if fp == 0 else "FAIL", "evidence": ["E1"]},
            {"checkId": "C4", "claimId": "H-30", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 4, "target": "INTERMEDIATE",
             "establishedValue": "refusal messages (validator's words, first 120 characters) with attribution: %s" % json.dumps([{"class": r["class"], "target": r["target"], "field": r["field"], "exit": r["exit"], "attributed": r["attributed"], "message": r["message"]} for r in rec["runs"]]), "outcome": "PASS", "evidence": ["E1"]},
        ],
        "claimVerdicts": [{"claimId": "H-30", "checks": ["C1", "C2", "C3", "C4"], "verdict": {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(status, "UNRESOLVED"), "value": value}],
        "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": ["C2"] if status == "UNRESOLVED" else [], "policyViolations": [],
                    "scores": {"seeded": seeded, "seeded_attributed": refused, "seeded_refused_any": refused_any, "seeded_crashed": crashed, "interpreter": rec.get("interpreter"), "precision_permille": int(round(precision * 1000)) if precision is not None else None, "controls": ctrl, "controls_refused": fp, "classes_uncaught": len(uncaught_class), "classes_partial": len(partial), "baseline_exit": rec["baseline"]["exit"]},
                    "evidenceRefs": [sha(runs_json), sha(run_record), sha(prereg), self_digest]},
    }
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, "|", why, "|", value)


if __name__ == "__main__":
    main(*sys.argv[1:5])
