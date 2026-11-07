"""RL-22 evaluator (PREREG v1). usage: python3 -I -B rl22_eval.py RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
import hashlib, json, pathlib, sys


def sha(p): return "sha256:" + hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main(runs_json, prereg, run_record, out_path):
    d = json.load(open(runs_json, encoding="utf-8")); c = d["counts"]
    n = c["transcript"] + c["binding"]; agree = c["transcriptAgree"] + c["bindingAgree"]; rate = agree / n if n else 0.0
    if n < 40: status, why = "UNRESOLVED", "fewer than 40 vectors"
    elif rate <= 0.70: status, why = "FAIL", "%d of %d reproduced (at most 70 percent)" % (agree, n)
    elif rate >= 0.95: status, why = "PASS", "%d of %d reproduced (at least 95 percent)" % (agree, n)
    else: status, why = "UNRESOLVED", "%d of %d reproduced (between 70 and 95 percent)" % (agree, n)
    value = "transcript vectors %d of %d; binding vectors %d of %d; rate %.3f; disagreements: %s" % (c["transcriptAgree"], c["transcript"], c["bindingAgree"], c["binding"], rate, json.dumps(d["disagreements"][:12]))
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    led = {"schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-22-RESULTS-v1", "supersedes": None, "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
           "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
           "evidence": [{"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(runs_json), "producedBy": "Research-Lab.rl22_board.run-001"}, {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"}, {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl22_eval"}],
           "claims": [{"claimId": "H-23-coord", "requirement": "H-23 (coordinator half): a board state machine written from the README alone reproduces at least 95 percent of the record's transcript and binding vectors", "delivered": value, "rolloutValues": [{"rollout": "run-001", "value": status}]}],
           "checks": [{"checkId": "C1", "claimId": "H-23-coord", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "DELIVERED", "establishedValue": value + "; gate: " + why, "outcome": status, "evidence": ["E1", "E3"]}],
           "claimVerdicts": [{"claimId": "H-23-coord", "checks": ["C1"], "verdict": {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(status, "UNRESOLVED"), "value": value}],
           "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": ["C1"] if status == "UNRESOLVED" else [], "policyViolations": [], "scores": {"vectors": n, "reproduced": agree, "rate_permille": int(round(rate * 1000))}, "evidenceRefs": [sha(runs_json), sha(run_record), sha(prereg), self_digest]}}
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, "|", why)


if __name__ == "__main__":
    main(*sys.argv[1:5])
