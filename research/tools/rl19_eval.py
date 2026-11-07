"""RL-19 evaluator (PREREG v1). usage: python3 -I -B rl19_eval.py RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
import hashlib, json, pathlib, sys


def sha(p): return "sha256:" + hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main(runs_json, prereg, run_record, out_path):
    d = json.load(open(runs_json, encoding="utf-8")); n, f = d["claims"], d["found"]
    rate = f / n if n else 0.0
    thin = [k for k, v in d["textChars"].items() if v < 5000]
    if thin or n < 20:
        status, why = "UNRESOLVED", "extraction too thin for %s or fewer than 20 claims" % thin
    elif rate <= 0.70:
        status, why = "FAIL", "%d of %d found (at most 70 percent)" % (f, n)
    elif rate >= 0.90:
        status, why = "PASS", "%d of %d found (at least 90 percent)" % (f, n)
    else:
        status, why = "UNRESOLVED", "%d of %d found (between 70 and 90 percent)" % (f, n)
    value = "found %d of %d claims (%.3f); by source %s; by paper %s; not found: %s" % (f, n, rate, json.dumps(d["bySource"], sort_keys=True), json.dumps(d["byPaper"], sort_keys=True), [r["id"] for r in d["results"] if r["status"] != "FOUND"])
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    led = {"schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-19-RESULTS-v1", "supersedes": None, "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
           "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
           "evidence": [{"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(runs_json), "producedBy": "Research-Lab.rl19_figures.run-001"}, {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"}, {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl19_eval"}],
           "claims": [{"claimId": "H-24-fig", "requirement": "H-24 (figure grounding): the figures the three syntheses attribute to the five held papers are found in the papers' own text at a rate of at least 90 percent", "delivered": value, "rolloutValues": [{"rollout": "run-001", "value": status}]}],
           "checks": [{"checkId": "C1", "claimId": "H-24-fig", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "DELIVERED", "establishedValue": value + "; gate: " + why, "outcome": status, "evidence": ["E1", "E3"]}],
           "claimVerdicts": [{"claimId": "H-24-fig", "checks": ["C1"], "verdict": {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(status, "UNRESOLVED"), "value": value}],
           "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": ["C1"] if status == "UNRESOLVED" else [], "policyViolations": [], "scores": {"claims": n, "found": f, "rate_permille": int(round(rate * 1000))}, "evidenceRefs": [sha(runs_json), sha(run_record), sha(prereg), self_digest]}}
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, "|", why)


if __name__ == "__main__":
    main(*sys.argv[1:5])
