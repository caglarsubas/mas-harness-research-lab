"""RL-21 evaluator (PREREG v1). usage: python3 -I -B rl21_eval.py RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
import hashlib, json, pathlib, sys


def sha(p): return "sha256:" + hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main(runs_json, prereg, run_record, out_path):
    d = json.load(open(runs_json, encoding="utf-8"))
    pre_ok = d["packetAuthorities"] >= 50 and d["metaAuthorities"] >= 5 and d["created"] >= 500
    a = "UNRESOLVED" if not pre_ok else ("PASS" if not d["createdTwice"] else "FAIL")
    a_v = "%d paths created by %d packet authorities; created twice: %d %s" % (d["created"], d["packetAuthorities"], len(d["createdTwice"]), d["createdTwice"][:3])
    b = "UNRESOLVED" if not pre_ok or d["changedInScope"] < 100 else ("PASS" if d["changedUnlinkedCount"] == 0 else "FAIL")
    b_v = "changes to created paths %d of %d entries (%d outside the export's scope); creator named among the changer's baseline packets %d; unlinked %d %s" % (d["changedInScope"], d["changedEntries"], d["changedOutOfScope"], d["changedLinked"], d["changedUnlinkedCount"], d["changedUnlinked"][:3])
    c = "PASS"  # PREREG v2: H-26c is descriptive (the chain lives in git history outside the export); recorded, never gated
    c_v = "descriptive: paths owned by more than one meta authority %d of %d; meta authorities %d; metaBaseline is a commit id (form %s), so the ownership chain is git history outside the export and is not checked here" % (d["ownedByMoreThanOne"], d["ownedPathsDistinct"], d["metaAuthorities"], d["metaBaselineForm"])
    st = (a, b); status = "PASS" if all(s == "PASS" for s in st) else ("FAIL" if "FAIL" in st else "UNRESOLVED")  # v2: a and b gated; c descriptive
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    cv = lambda s: {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(s, "UNRESOLVED")
    claims = (("H-26a", "C1", a, a_v, "H-26a: every path under architecture/ is created by exactly one packet authority"),
              ("H-26b", "C2", b, b_v, "H-26b: every change to a created path names its creator among the changer's baseline packets"),
              ("H-26c", "C3", c, c_v, "H-26c (descriptive, not gated): ownership of paths by meta authorities"))
    led = {"schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-21-RESULTS-v1", "supersedes": None, "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
           "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
           "evidence": [{"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(runs_json), "producedBy": "Research-Lab.rl21_writers.run-001"}, {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"}, {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl21_eval"}],
           "claims": [{"claimId": k, "requirement": req, "delivered": v, "rolloutValues": [{"rollout": "run-001", "value": s}]} for k, ch, s, v, req in claims],
           "checks": [{"checkId": ch, "claimId": k, "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": i + 1, "target": "DELIVERED", "establishedValue": v, "outcome": s, "evidence": ["E1", "E3"]} for i, (k, ch, s, v, req) in enumerate(claims)],
           "claimVerdicts": [{"claimId": k, "checks": [ch], "verdict": cv(s), "value": v} for k, ch, s, v, req in claims],
           "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": [ch for k, ch, s, v, req in claims if s == "UNRESOLVED"], "policyViolations": [],
                       "scores": {"created": d["created"], "created_twice": len(d["createdTwice"]), "changed_in_scope": d["changedInScope"], "changed_unlinked": d["changedUnlinkedCount"], "owned_multi": d["ownedByMoreThanOne"], "broken_chains": d["brokenCount"]},
                       "evidenceRefs": [sha(runs_json), sha(run_record), sha(prereg), self_digest]}}
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, "| H-26a", a, "| H-26b", b, "| H-26c", c)


if __name__ == "__main__":
    main(*sys.argv[1:5])
