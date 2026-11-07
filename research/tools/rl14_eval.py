"""RL-14 evaluator (PREREG v1): Spearman rho between a resume block's typedness and the dated MON-line rate of the
window it opens, with a seeded percentile bootstrap, the secondary medians and the preregistered gate; writes the
verdict ledger. usage: python3 -I -B rl14_eval.py WINDOWS_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
import hashlib
import json
import pathlib
import random
import statistics
import sys


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    r = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return r


def pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    sa = sum((x - ma) ** 2 for x in a) ** 0.5
    sb = sum((y - mb) ** 2 for y in b) ** 0.5
    if sa == 0 or sb == 0:
        return None  # undefined: no variance (PREREG v4)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def sha(path):
    return "sha256:" + hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def main(windows_json, prereg, run_record, out_path):
    rec = json.load(open(windows_json, encoding="utf-8"))
    w = [v for v in rec["windows"] if v["days"] >= 1]
    x = [v["typedness"] for v in w]; y = [v["ratePerDay"] for v in w]
    n = len(w)
    rho = spearman(x, y) if n >= 3 else None
    per_cluster = {f: sum(1 for v in w if v["file"] == f) for f in sorted({v["file"] for v in w})}
    rng = random.Random(20261105)
    files = sorted({v["file"] for v in w})
    by_file = {f: [i for i, v in enumerate(w) if v["file"] == f] for f in files}
    boots, undefined = [], 0
    for _ in range(1000):  # file-clustered: resample files with replacement, keep every window of a drawn file (PREREG v2)
        idx = [i for f in (files[rng.randrange(len(files))] for _ in files) for i in by_file[f]]
        r = spearman([x[i] for i in idx], [y[i] for i in idx]) if len(idx) >= 3 else None
        if r is None:
            undefined += 1  # dropped and counted (PREREG v4)
        else:
            boots.append(r)
    boots.sort()
    defined = len(boots)
    if defined >= 900:
        lo, hi = boots[int(0.025 * defined)], boots[int(0.975 * defined) - 1]
    else:
        lo, hi = None, None
    mx = statistics.median(x)
    above = [v["ratePerDay"] for v in w if v["typedness"] > mx]
    below = [v["ratePerDay"] for v in w if v["typedness"] <= mx]
    med_above = statistics.median(above) if above else None
    med_below = statistics.median(below) if below else None
    MEI = -0.30  # the minimum effect of interest (PREREG v3)
    if n < 20:
        status, why = "UNRESOLVED", "n below 20"
    elif rho is None:
        status, why = "UNRESOLVED", "rho undefined: no variance in X or Y"
    elif lo is None:
        status, why = "UNRESOLVED", "fewer than 900 of 1,000 resamples defined (%d)" % defined
    elif rho <= MEI and hi < 0:
        status, why = "PASS", "rho <= -0.30 and the interval's upper bound is below 0"
    elif lo > MEI:
        status, why = "FAIL", ("the interval excludes the minimum effect of interest (lower bound above -0.30)" + ("; opposite association (lower bound above 0)" if lo > 0 else ""))
    else:
        status, why = "UNRESOLVED", "the interval reaches the minimum effect of interest but PASS is not met"
    # descriptive sensitivity (PREREG v3): X with digests only (no line-pin term); never gated
    xd = [v["typednessDigestsOnly"] for v in w]
    rho_d = spearman(xd, y) if n >= 3 else None
    rho_d = float("nan") if rho_d is None else rho_d
    rho_s = float("nan") if rho is None else rho
    lo_s = float("nan") if lo is None else lo; hi_s = float("nan") if hi is None else hi
    ties_x = n - len(set(x)); ties_y = n - len(set(y))
    value = "n %d; rho %.3f; 95 percent clustered bootstrap [%.3f, %.3f] (%d of 1,000 resamples defined); digests-only rho %.3f (descriptive); tied X values %d, tied Y values %d; windows per cluster %s; median rate above-median typedness %s vs at-or-below %s (n %d / %d)" % (
        n, rho_s, lo_s, hi_s, defined, rho_d, ties_x, ties_y, json.dumps(per_cluster, sort_keys=True), "%.3f" % med_above if med_above is not None else "-", "%.3f" % med_below if med_below is not None else "-", len(above), len(below))
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    led = {
        "schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-14-RESULTS-v1", "supersedes": None,
        "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
        "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
        "evidence": [
            {"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(windows_json), "producedBy": "Research-Lab.rl14_handoff.run-001"},
            {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"},
            {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl14_eval"},
        ],
        "claims": [{"claimId": "H-28-obs", "requirement": "H-28 (observational half): typed resume blocks are followed by fewer dated MON lines per day",
                    "delivered": value, "rolloutValues": [{"rollout": "run-001", "value": status}]}],
        "checks": [
            {"checkId": "C1", "claimId": "H-28-obs", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "INTERMEDIATE",
             "establishedValue": "windows with days >= 1: %d (of %d); files %d (clusters %d, windows per cluster %s); blocks %d (the last block of each lane opens no window)" % (n, len(rec["windows"]), len(rec["files"]), len(files), json.dumps(per_cluster, sort_keys=True), len(rec["blocks"])), "outcome": "PASS" if n >= 20 else "FAIL", "evidence": ["E1"]},
            {"checkId": "C2", "claimId": "H-28-obs", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 2, "target": "DELIVERED",
             "establishedValue": "rho %.3f; bootstrap [%.3f, %.3f], %d defined resamples; gate: %s" % (rho_s, lo_s, hi_s, defined, why), "outcome": status if status != "UNRESOLVED" else "UNRESOLVED", "evidence": ["E1", "E3"]},
            {"checkId": "C3", "claimId": "H-28-obs", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 3, "target": "INTERMEDIATE",
             "establishedValue": "secondary, descriptive: median rate per day %s (typedness above median, n %d) vs %s (at or below, n %d)" % (med_above, len(above), med_below, len(below)), "outcome": "PASS", "evidence": ["E1"]},
            {"checkId": "C4", "claimId": "H-28-obs", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 4, "target": "INTERMEDIATE",
             "establishedValue": "sensitivity, descriptive: rho with digests-only typedness %.3f against %.3f; tied X %d of %d, tied Y %d of %d (average ranks)" % (rho_d, rho_s, ties_x, n, ties_y, n), "outcome": "PASS", "evidence": ["E1", "E3"]},
        ],
        "claimVerdicts": [{"claimId": "H-28-obs", "checks": ["C1", "C2", "C3", "C4"], "verdict": {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(status, "UNRESOLVED"), "value": value}],
        "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": ["C2"] if status == "UNRESOLVED" else [], "policyViolations": [],
                    "scores": {"n": n, "rho_permille": int(round(rho * 1000)) if rho is not None else None, "ci_lo_permille": int(round(lo * 1000)) if lo is not None else None, "ci_hi_permille": int(round(hi * 1000)) if hi is not None else None, "defined_resamples": defined, "rho_digests_only_permille": int(round(rho_d * 1000)) if rho_d == rho_d else None, "typed_blocks": sum(1 for b in rec["blocks"] if b["digests"] + b["linePins"] > 0), "blocks": len(rec["blocks"])},
                    "evidenceRefs": [sha(windows_json), sha(run_record), sha(prereg), self_digest]},
    }
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, value)


if __name__ == "__main__":
    main(*sys.argv[1:5])
