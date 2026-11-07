"""RL-18 evaluator (PREREG v1): the gates on the builder's output; the verdict ledger.
usage: python3 -I -B rl18_eval.py RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
import hashlib
import json
import pathlib
import sys


def sha(path):
    return "sha256:" + hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def main(runs_json, prereg, run_record, out_path):
    d = json.load(open(runs_json, encoding="utf-8")); vc = d["vectors"]["counts"]; ac = d["arms"]["counts"]
    pre_ok = d["arms"]["classesShaMatch"]
    # H-31a instrument check on the contract's vectors: a mismatch is an instrument gap (UNRESOLVED), never a finding against the contract
    a_ok = vc["shapeRefused"] == vc["shapeCases"] and vc["validAccepted"] == vc["validCases"] and vc["comparisonAgree"] == vc["comparisonCases"] and vc["mismatchFlagged"] == vc["mismatchCases"] and vc["comparisonCases"] >= 10
    a_status = "UNRESOLVED" if not pre_ok else ("PASS" if a_ok else "UNRESOLVED")
    a_value = "SHAPE vectors refused %d of %d; valid vectors accepted %d of %d; valid comparison vectors reproduced bit for bit %d of %d; DECISION_MISMATCH vectors flagged %d of %d" % (
        vc["shapeRefused"], vc["shapeCases"], vc["validAccepted"], vc["validCases"], vc["comparisonAgree"], vc["comparisonCases"], vc["mismatchFlagged"], vc["mismatchCases"])
    # H-31b expressibility
    b_all = ac["splitValid"] and ac["manifestsValid"] == ac["manifests"] and ac["recordsValid"] == ac["records"] and ac["comparisonsValid"] == ac["comparisons"] and ac["manifests"] == 640 and ac["records"] == 12 and ac["comparisons"] == 9
    if not pre_ok or a_status != "PASS":
        b_status, b_why = "UNRESOLVED", "precondition or the instrument check not met"
    elif not b_all:
        b_status, b_why = "FAIL", "a built instance was refused by the contract's schema or the counts are short"
    else:
        b_status, b_why = "PASS", "the split, 640 manifests, 12 records and 9 comparisons all validate"
    b_value = "split valid %s; manifests %d of %d valid; records %d of %d; comparisons %d of %d; refusals: %s" % (ac["splitValid"], ac["manifestsValid"], ac["manifests"], ac["recordsValid"], ac["records"], ac["comparisonsValid"], ac["comparisons"],
        json.dumps((d["arms"]["manifestRefused"][:3] + [r for r in d["arms"]["records"] if not r["valid"]][:3] + [{"c": c["arm"] + "/" + c["metric"], "where": c["where"]} for c in d["arms"]["comparisons"] if not c["valid"]][:3])))
    # H-31c agreement with the campaign's recorded arm verdicts
    agree, cells, unres = ac["agree"], ac["comparisons"], ac["comparisonsUnresolved"]
    if not pre_ok or a_status != "PASS":
        c_status, c_why = "UNRESOLVED", "precondition or the instrument check not met"
    elif unres > 0:
        c_status, c_why = "UNRESOLVED", "%d of %d comparisons UNRESOLVED by the gate" % (unres, cells)
    elif agree <= 5:
        c_status, c_why = "FAIL", "%d of %d cells agree (at most 5): the two gate forms disagree systematically" % (agree, cells)
    elif agree >= 8:
        c_status, c_why = "PASS", "%d of %d cells agree (at least 8)" % (agree, cells)
    else:
        c_status, c_why = "UNRESOLVED", "%d of %d cells agree (6 or 7)" % (agree, cells)
    c_value = "cells (arm, metric): " + "; ".join("%s/%s: gate %s nonInferior %s mean %s half %s, campaign bounds hold in all classes %s -> %s" % (
        c["arm"], c["metric"], c["decision"], c["statistics"]["nonInferior"] if c["statistics"] else None, c["statistics"]["meanDifferencePpm"] if c["statistics"] else None, c["statistics"]["halfWidthPpm"] if c["statistics"] else None, c["campaignBoundsHoldAllClasses"], "agree" if c["agrees"] else "DISAGREE") for c in d["arms"]["comparisons"])
    statuses = (a_status, b_status, c_status)
    status = "PASS" if all(s == "PASS" for s in statuses) else ("FAIL" if "FAIL" in statuses else "UNRESOLVED")
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    cv = lambda s: {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(s, "UNRESOLVED")
    led = {
        "schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-18-RESULTS-v1", "supersedes": None,
        "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
        "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
        "evidence": [
            {"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(runs_json), "producedBy": "Research-Lab.rl18_manifest.run-001"},
            {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"},
            {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl18_eval"},
        ],
        "claims": [
            {"claimId": "H-31a", "requirement": "H-31a (instrument): the lab's validator and integer gate reproduce the contract's vectors", "delivered": a_value, "rolloutValues": [{"rollout": "run-001", "value": a_status}]},
            {"claimId": "H-31b", "requirement": "H-31b: the CONF-MAS arms study is expressible as valid run manifests, evaluation records and comparisons", "delivered": b_value, "rolloutValues": [{"rollout": "run-001", "value": b_status}]},
            {"claimId": "H-31c", "requirement": "H-31c: the distribution gate's non-inferiority verdicts agree with the campaign's recorded bound verdicts per arm and metric", "delivered": c_value, "rolloutValues": [{"rollout": "run-001", "value": c_status}]},
        ],
        "checks": [
            {"checkId": "C1", "claimId": "H-31a", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "INTERMEDIATE", "establishedValue": a_value, "outcome": a_status, "evidence": ["E1", "E3"]},
            {"checkId": "C2", "claimId": "H-31b", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 2, "target": "DELIVERED", "establishedValue": b_value + "; gate: " + b_why, "outcome": b_status, "evidence": ["E1", "E3"]},
            {"checkId": "C3", "claimId": "H-31c", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 3, "target": "DELIVERED", "establishedValue": c_value + "; gate: " + c_why, "outcome": c_status, "evidence": ["E1", "E3"]},
        ],
        "claimVerdicts": [{"claimId": k, "checks": [ch], "verdict": cv(s), "value": v} for k, ch, s, v in (("H-31a", "C1", a_status, a_value), ("H-31b", "C2", b_status, b_value), ("H-31c", "C3", c_status, c_value))],
        "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": [ch for ch, s in (("C1", a_status), ("C2", b_status), ("C3", c_status)) if s == "UNRESOLVED"], "policyViolations": [],
                    "scores": {"shape_refused": vc["shapeRefused"], "shape_cases": vc["shapeCases"], "valid_accepted": vc["validAccepted"], "valid_cases": vc["validCases"], "comparison_agree": vc["comparisonAgree"], "comparison_cases": vc["comparisonCases"],
                               "manifests_valid": ac["manifestsValid"], "manifests": ac["manifests"], "records_valid": ac["recordsValid"], "comparisons_valid": ac["comparisonsValid"], "cells_agree": agree, "cells": cells, "cells_unresolved": unres},
                    "evidenceRefs": [sha(runs_json), sha(run_record), sha(prereg), self_digest]},
    }
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, "| H-31a", a_status, "| H-31b", b_status, b_why, "| H-31c", c_status, c_why)


if __name__ == "__main__":
    main(*sys.argv[1:5])
