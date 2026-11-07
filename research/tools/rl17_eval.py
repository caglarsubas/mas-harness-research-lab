"""RL-17 evaluator (PREREG v1): gates on the replay driver's output; writes the verdict ledger.
usage: python3 -I -B rl17_eval.py RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
import hashlib
import json
import pathlib
import sys


def sha(path):
    return "sha256:" + hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def main(runs_json, prereg, run_record, out_path):
    d = json.load(open(runs_json, encoding="utf-8")); c = d["counts"]
    pre_ok = d["classesShaMatch"]
    # precedence (PREREG v2): precondition, then FAIL, then UNRESOLVED, then PASS, for every claim
    if not pre_ok: a_status = "UNRESOLVED"
    elif c["identical"] < c["pairs"]: a_status = "FAIL"
    elif c["pairs"] < 39: a_status = "UNRESOLVED"
    else: a_status = "PASS"
    a_value = "classes.json digest matches the committed results: %s; %d of %d run pairs identical (whole effect log)" % (pre_ok, c["identical"], c["pairs"])
    b_status = "PASS" if (pre_ok and d["replayStale"]["sameWholeRow"]) else ("UNRESOLVED" if not pre_ok else "FAIL")
    b_value = "REPLAY_STALE class %s: result %s (committed %s); whole row equal: %s; differing keys: %s" % (d["replayStale"]["id"], d["replayStale"]["result"], d["replayStale"]["committedResult"], d["replayStale"]["sameWholeRow"], d["replayStale"]["differingTopLevelKeys"])
    if not pre_ok:
        c_status, c_why = "UNRESOLVED", "precondition failed"
    elif c["staleAccepted"] > 0 or c["dupChanged"] > 0 or c["staleChanged"] > 0 or (c["dupAttempts"] - c["dupRefusedDuplicateId"] - 0) > 0 and any(k == "ACCEPTED" for r in d["replay"] for k in r["dupOtherAnswer"]):
        c_status, c_why = "FAIL", "a duplicate or a stale replay was accepted, or a replay changed state"
    elif c["dupAttempts"] == 0 or c["staleAttempts"] == 0 or c["exceptions"] > 0 or c["dupRefusedDuplicateId"] < c["dupAttempts"] or c["staleOtherRefusal"] > 0:
        c_status, c_why = "UNRESOLVED", "no vectors posed, or %d driver exceptions, or %d duplicates answered other than DUPLICATE_ID, or %d stale replays refused for another reason than STALE_VERSION" % (c["exceptions"], c["dupAttempts"] - c["dupRefusedDuplicateId"], c["staleOtherRefusal"])
    else:
        c_status, c_why = "PASS", "every duplicate answered DUPLICATE_ID and every stale replay answered STALE_VERSION, none changed state"
    # H-27d: the recorded operation sequence replayed through a fresh board
    lr = c["logReplayRuns"]; li = c["logReplayIdentical"]; le = c["logReplayExceptions"]
    if not pre_ok: d_status, d_why = "UNRESOLVED", "precondition failed"
    elif li < lr: d_status, d_why = "FAIL", "the claim and merge answers diverged from the recorded log in %d of %d runs" % (lr - li, lr)
    elif le > 0 or lr == 0: d_status, d_why = "UNRESOLVED", "driver exceptions or no runs"
    else: d_status, d_why = "PASS", "the claim and merge answer sequence replayed identically in every run"
    d_value = "log replay through a fresh board: claim and merge sequence identical in %d of %d runs; agreement by operation kind (agree, total): %s; exceptions %d" % (li, lr, json.dumps(c["logReplayAgreeByOp"], sort_keys=True), le)
    c_value = "duplicates: %d of %d answered DUPLICATE_ID, %d changed state; stale replays: %d of %d answered STALE_VERSION, %d refused otherwise, %d accepted, %d changed state, %d not posable (version unchanged); exceptions %d" % (
        c["dupRefusedDuplicateId"], c["dupAttempts"], c["dupChanged"], c["staleStaleVersion"], c["staleAttempts"], c["staleOtherRefusal"], c["staleAccepted"], c["staleChanged"], c["staleNotPosable"], c["exceptions"])
    statuses = (a_status, b_status, c_status, d_status)
    status = "PASS" if all(s == "PASS" for s in statuses) else ("FAIL" if "FAIL" in statuses else "UNRESOLVED")
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    cv = lambda s: {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(s, "UNRESOLVED")
    led = {
        "schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-17-RESULTS-v1", "supersedes": None,
        "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
        "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
        "evidence": [
            {"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(runs_json), "producedBy": "Research-Lab.rl17_replay.run-001"},
            {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"},
            {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl17_eval"},
        ],
        "claims": [
            {"claimId": "H-27a", "requirement": "H-27a: two runs of the same class and seed produce identical effect logs", "delivered": a_value, "rolloutValues": [{"rollout": "run-001", "value": a_status}]},
            {"claimId": "H-27b", "requirement": "H-27b: the committed REPLAY_STALE class row reproduces exactly on the pin", "delivered": b_value, "rolloutValues": [{"rollout": "run-001", "value": b_status}]},
            {"claimId": "H-27c", "requirement": "H-27c: duplicated and stale (reordered) board operations replayed after a run are refused and change nothing", "delivered": c_value, "rolloutValues": [{"rollout": "run-001", "value": c_status}]},
            {"claimId": "H-27d", "requirement": "H-27d: the recorded operation sequence replayed in order through a fresh board reproduces the claim and merge answers exactly", "delivered": d_value, "rolloutValues": [{"rollout": "run-001", "value": d_status}]},
        ],
        "checks": [
            {"checkId": "C1", "claimId": "H-27a", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "DELIVERED", "establishedValue": a_value + "; bound: all pairs identical, at least 39 pairs", "outcome": a_status, "evidence": ["E1", "E3"]},
            {"checkId": "C2", "claimId": "H-27b", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 2, "target": "DELIVERED", "establishedValue": b_value, "outcome": b_status, "evidence": ["E1", "E3"]},
            {"checkId": "C3", "claimId": "H-27c", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 3, "target": "DELIVERED", "establishedValue": c_value + "; gate: " + c_why, "outcome": c_status, "evidence": ["E1", "E3"]},
            {"checkId": "C4", "claimId": "H-27d", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 4, "target": "DELIVERED", "establishedValue": d_value + "; gate: " + d_why, "outcome": d_status, "evidence": ["E1", "E3"]},
        ],
        "claimVerdicts": [{"claimId": k, "checks": [ch], "verdict": cv(s), "value": v} for k, ch, s, v in (("H-27a", "C1", a_status, a_value), ("H-27b", "C2", b_status, b_value), ("H-27c", "C3", c_status, c_value), ("H-27d", "C4", d_status, d_value))],
        "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": [ch for ch, s in (("C1", a_status), ("C2", b_status), ("C3", c_status), ("C4", d_status)) if s == "UNRESOLVED"], "policyViolations": [],
                    "scores": {"pairs": c["pairs"], "identical": c["identical"], "dup_attempts": c["dupAttempts"], "dup_duplicate_id": c["dupRefusedDuplicateId"], "stale_attempts": c["staleAttempts"], "stale_stale_version": c["staleStaleVersion"], "stale_other_refusal": c["staleOtherRefusal"], "log_replay_identical": c["logReplayIdentical"], "log_replay_runs": c["logReplayRuns"], "stale_accepted": c["staleAccepted"], "changed": c["dupChanged"] + c["staleChanged"], "exceptions": c["exceptions"]},
                    "evidenceRefs": [sha(runs_json), sha(run_record), sha(prereg), self_digest]},
    }
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, "| H-27a", a_status, "| H-27b", b_status, "| H-27c", c_status, c_why, "| H-27d", d_status, d_why)


if __name__ == "__main__":
    main(*sys.argv[1:5])
