"""RL-20 evaluator (PREREG v1). usage: python3 -I -B rl20_eval.py RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
import hashlib, json, pathlib, sys


def sha(p): return "sha256:" + hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main(runs_json, prereg, run_record, out_path):
    d = json.load(open(runs_json, encoding="utf-8")); c = d["counts"]
    a_status = "PASS" if c["vectorAgree"] == c["vectorCases"] and c["vectorCases"] >= 40 else "UNRESOLVED"
    a_value = "the lab's checker agrees with %d of %d topology vectors; disagreements: %s" % (c["vectorAgree"], c["vectorCases"], [(a["id"], a["expect"], a["lab"]) for a in d["agreement"] if not a["agrees"]][:8])
    if a_status != "PASS":
        b_status, b_why = "UNRESOLVED", "instrument check not met"
    elif c["gatedAccepted"] > 0 or c["validAccepted"] < c["valid"]:
        b_status, b_why = "FAIL", "%d seeded edits accepted or %d of %d valid vectors refused" % (c["gatedAccepted"], c["valid"] - c["validAccepted"], c["valid"])
    elif c["gatedRefusedAsExpected"] < c["gatedMutations"]:
        b_status, b_why = "UNRESOLVED", "%d of %d seeded edits refused but not with the expected code or without a witness" % (c["gatedMutations"] - c["gatedRefusedAsExpected"], c["gatedMutations"])
    else:
        b_status, b_why = "PASS", "all %d gated seeded edits refused with the expected code and a witness; all %d valid vectors accepted" % (c["gatedMutations"], c["valid"])
    b_value = "gated seeded edits refused as expected %d of %d (accepted %d); valid vectors accepted %d of %d; descriptive (decentralized isolated peer): %s" % (c["gatedRefusedAsExpected"], c["gatedMutations"], c["gatedAccepted"], c["validAccepted"], c["valid"], json.dumps(c["descriptive"]))
    status = "PASS" if a_status == "PASS" and b_status == "PASS" else ("FAIL" if b_status == "FAIL" else "UNRESOLVED")
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    cv = lambda s: {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(s, "UNRESOLVED")
    led = {"schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-20-RESULTS-v1", "supersedes": None, "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
           "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
           "evidence": [{"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(runs_json), "producedBy": "Research-Lab.rl20_topology.run-001"}, {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"}, {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl20_eval"}],
           "claims": [{"claimId": "H-25a", "requirement": "H-25a (instrument): the lab's checker reproduces the record's topology vectors", "delivered": a_value, "rolloutValues": [{"rollout": "run-001", "value": a_status}]},
                      {"claimId": "H-25b", "requirement": "H-25b: the seeded graph classes the TopologySpec can express (cycle, unreachable node, budget escape) are refused with the record's code and a witness, and no valid vector is refused", "delivered": b_value, "rolloutValues": [{"rollout": "run-001", "value": b_status}]}],
           "checks": [{"checkId": "C1", "claimId": "H-25a", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "INTERMEDIATE", "establishedValue": a_value, "outcome": a_status, "evidence": ["E1", "E3"]},
                      {"checkId": "C2", "claimId": "H-25b", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 2, "target": "DELIVERED", "establishedValue": b_value + "; gate: " + b_why, "outcome": b_status, "evidence": ["E1", "E3"]}],
           "claimVerdicts": [{"claimId": "H-25a", "checks": ["C1"], "verdict": cv(a_status), "value": a_value}, {"claimId": "H-25b", "checks": ["C2"], "verdict": cv(b_status), "value": b_value}],
           "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": [ch for ch, s in (("C1", a_status), ("C2", b_status)) if s == "UNRESOLVED"], "policyViolations": [],
                       "scores": {"vector_agree": c["vectorAgree"], "vector_cases": c["vectorCases"], "gated_mutations": c["gatedMutations"], "gated_refused_as_expected": c["gatedRefusedAsExpected"], "gated_accepted": c["gatedAccepted"], "valid_accepted": c["validAccepted"]},
                       "evidenceRefs": [sha(runs_json), sha(run_record), sha(prereg), self_digest]}}
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, "| H-25a", a_status, "| H-25b", b_status, b_why)


if __name__ == "__main__":
    main(*sys.argv[1:5])
