"""RL-15b companion validator (R13 issue 3, 2026-11-09): enforces the frozen case set and the row-to-count consistency
that the frozen evaluator rl15b_eval.py (2d6c349b) does not check. It never emits PASS or FAIL: its outcomes are VALID,
INCOMPLETE (required observations absent) or INVALID (duplicates, extras, malformed rows, inconsistent fields or a
supplied summary that disagrees with its rows). The frozen evaluator, ledger and report are not touched.

usage:
  python3 -I -B rl15b_validate.py derive RL15_RUN002_JSON OUT_CASE_SET_JSON
      the frozen case set from RL-15 run-002's record (the PREREG pins its targets at seed 20261105): the 18 seeded
      (class, target, field) identities and the 3 controls, the declared uncatchable instance, the expected counts.
  python3 -I -B rl15b_validate.py check RUNS_JSON CASE_SET_JSON [--ledger RESULTS_JSON] [--write OUT_JSON]
      exit 0 VALID, 3 INCOMPLETE, 2 INVALID; prints the outcome and the failed checks, counts only.
Standard library only."""
import datetime
import hashlib
import json
import pathlib
import platform
import sys

SCHEMA_CASE_SET = "planeon.research.rl15b-case-set/v1"
SCHEMA_VALIDATION = "planeon.research.case-set-validation/v1"
# The PREREG (v1 e5a75db2) declares one seeded instance uncatchable by design: the secondary-paper digest instance
# (no file in the bridge to compare), excluded from the catchable denominator.
DECLARED_UNCATCHABLE = ["M6", "MCP faults", "sha256"]
SEEDED_CLASSES = ("M1", "M2", "M3", "M4", "M5", "M6")
ROW_TYPES = {"class": str, "target": str, "field": str, "catchable": bool, "exit": int, "refused": bool,
             "attributed": bool, "crashed": bool, "attributedToNewRule": bool, "message": str, "messageLength": int,
             "tokens": list, "wall_s": (int, float)}
LEDGER_SCORE_KEYS = ("catchable", "catchable_refused", "attributed", "by_new_rule", "by_older_rule", "new_rule_m4",
                     "new_rule_m6", "controls", "controls_refused", "unattributed", "seeded_crashed", "classes_uncaught")


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def ident(r):
    return (r.get("class"), r.get("target"), r.get("field"))


def derive(run002_json, out_path):
    rec = json.load(open(run002_json, encoding="utf-8"))
    ids = [list(ident(r)) for r in rec["runs"]]
    assert len(ids) == 21 and len({tuple(i) for i in ids}) == 21, "RL-15 run-002 must hold 21 unique cases"
    cases = []
    for i in ids:
        catchable = i != DECLARED_UNCATCHABLE
        cases.append({"class": i[0], "target": i[1], "field": i[2], "catchable": catchable})
    per_class = {k: sum(1 for c in cases if c["class"] == k) for k in SEEDED_CLASSES}
    assert all(v == 3 for v in per_class.values()) and sum(1 for c in cases if c["class"] == "C") == 3
    doc = {"schemaVersion": SCHEMA_CASE_SET, "derivedFrom": {"path": "experiments/RL-15/data/rl15_runs_002.json",
                                                             "sha256": sha(run002_json), "seed": rec.get("seed")},
           "declaredUncatchable": dict(zip(("class", "target", "field"), DECLARED_UNCATCHABLE)),
           "expected": {"seeded": 18, "catchable": 17, "uncatchable": 1, "controls": 3, "rowsPerClass": {**per_class, "C": 3},
                        "catchablePerClass": {k: sum(1 for c in cases if c["class"] == k and c["catchable"]) for k in SEEDED_CLASSES}},
           "cases": cases}
    json.dump(doc, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("case set written:", len(cases), "cases; source", doc["derivedFrom"]["sha256"][:8])


def recount(rows):
    seeded = [r for r in rows if r["class"] != "C"]
    catchable = [r for r in seeded if r["catchable"]]
    controls = [r for r in rows if r["class"] == "C"]
    return {"seeded": len(seeded), "catchable": len(catchable), "uncatchable": len(seeded) - len(catchable),
            "seededRefused": sum(bool(r["refused"]) for r in seeded), "catchableRefused": sum(bool(r["refused"]) for r in catchable),
            "attributed": sum(bool(r["attributed"]) for r in catchable), "byNewRule": sum(bool(r["attributedToNewRule"]) for r in catchable),
            "byOlderRule": sum(1 for r in catchable if r["attributedToOlderRule"]),
            "unattributedRefusals": sum(1 for r in catchable if r["refused"] and not r["attributed"]),
            "newRulePerClass": {k: sum(1 for r in catchable if r["class"] == k and r["attributedToNewRule"]) for k in ("M4", "M6")},
            "seededCrashed": sum(bool(r["crashed"]) for r in seeded), "controls": len(controls),
            "controlsRefused": sum(bool(r["refused"]) for r in controls), "controlsNonZero": sum(1 for r in controls if r["exit"] != 0),
            "uncatchableOutcome": [("refused" if r["refused"] else "built") for r in seeded if not r["catchable"]],
            "perClass": {k: [sum(1 for r in catchable if r["class"] == k and r["attributed"]), sum(1 for r in catchable if r["class"] == k and r["refused"]),
                             sum(1 for r in catchable if r["class"] == k)] for k in SEEDED_CLASSES}}


def derived_gate(c):
    return {"catchable": c["catchable"], "catchable_refused": c["catchableRefused"], "attributed": c["attributed"],
            "by_new_rule": c["byNewRule"], "by_older_rule": c["byOlderRule"], "new_rule_m4": c["newRulePerClass"]["M4"],
            "new_rule_m6": c["newRulePerClass"]["M6"], "controls": c["controls"], "controls_refused": c["controlsNonZero"],
            "unattributed": c["unattributedRefusals"], "seeded_crashed": c["seededCrashed"],
            "classes_uncaught": sum(1 for k, (a, r, m) in c["perClass"].items() if m > 0 and r == 0)}


def check(runs_json, case_set_json, ledger_json=None, out_path=None):
    rec = json.load(open(runs_json, encoding="utf-8"))
    cs = json.load(open(case_set_json, encoding="utf-8"))
    rows = rec.get("runs", [])
    checks = []

    def add(cid, name, ok, detail, kind):
        checks.append({"checkId": cid, "name": name, "outcome": "PASS" if ok else "FAIL", "detail": detail, "failureKind": None if ok else kind})

    # V5 first: the other checks read the fields it guards.
    bad_rows = []
    for i, r in enumerate(rows):
        for k, t in ROW_TYPES.items():
            if k not in r or isinstance(r[k], bool) and t is int or not isinstance(r[k], t):
                bad_rows.append((i, k))
        if "attributedToOlderRule" not in r or not (r["attributedToOlderRule"] is False or r["attributedToOlderRule"] is None or isinstance(r["attributedToOlderRule"], str)):
            bad_rows.append((i, "attributedToOlderRule"))
        if r.get("class") not in SEEDED_CLASSES + ("C",):
            bad_rows.append((i, "class"))
    add("V5", "row types", not bad_rows, "%d rows, %d malformed fields" % (len(rows), len(bad_rows)), "INVALID")
    if bad_rows:
        return finish(checks, None, runs_json, case_set_json, ledger_json, out_path)

    want = {tuple(ident(c)): c["catchable"] for c in cs["cases"]}
    have = [ident(r) for r in rows]
    dup = sorted({i for i in have if have.count(i) > 1})
    missing = sorted(set(want) - set(have))
    extra = sorted(set(have) - set(want))
    add("V1", "case identities equal the frozen case set", not missing and not extra,
        "%d of %d present, %d missing, %d extra" % (len(set(have) & set(want)), len(want), len(missing), len(extra)),
        "INVALID" if extra else "INCOMPLETE")
    add("V2", "no duplicate case", not dup, "%d duplicated identities" % len(dup), "INVALID")
    exp = cs["expected"]
    rows_per = {k: sum(1 for r in rows if r["class"] == k) for k in SEEDED_CLASSES + ("C",)}
    short = {k: (rows_per[k], v) for k, v in exp["rowsPerClass"].items() if rows_per[k] < v}
    over = {k: (rows_per[k], v) for k, v in exp["rowsPerClass"].items() if rows_per[k] > v}
    add("V3", "rows per class (M1 to M6 three each, controls three)", not short and not over,
        "short %d class(es), over %d class(es)" % (len(short), len(over)), "INVALID" if over else "INCOMPLETE")
    flags_bad = [i for i in have if i in want and any(r["catchable"] != want[i] for r in rows if ident(r) == i)]
    uncatch = [ident(r) for r in rows if r["class"] != "C" and not r["catchable"]]
    add("V4", "catchable flags and the one declared exclusion", not flags_bad and uncatch == [tuple(DECLARED_UNCATCHABLE)],
        "%d flag mismatches; uncatchable rows %d (expected 1, the declared instance)" % (len(flags_bad), len(uncatch)), "INVALID")
    incons = []
    for i, r in enumerate(rows):
        if r["refused"] and (r["exit"] == 0 or r["crashed"]):
            incons.append((i, "refused with exit 0 or crashed"))
        if r["attributed"] and not r["refused"]:
            incons.append((i, "attributed without refusal"))
        srcs = int(bool(r["attributedToNewRule"])) + int(bool(r["attributedToOlderRule"]))
        if r["attributed"] and srcs != 1:
            incons.append((i, "attributed with %d sources" % srcs))
        if not r["attributed"] and srcs != 0:
            incons.append((i, "attribution source without attributed"))
        if r["crashed"] and r["exit"] == 0:
            incons.append((i, "crashed with exit 0"))
        if r["messageLength"] != len(r["message"]):
            incons.append((i, "messageLength differs from message"))
    add("V6", "field consistency (exit, refusal, attribution, crash, message length)", not incons, "%d inconsistent rows" % len(incons), "INVALID")
    rc = recount(rows)
    sup = rec.get("counts", {})
    diff = sorted(k for k in rc if sup.get(k) != rc[k]) + sorted(k for k in sup if k not in rc)
    add("V7", "supplied counts equal the recount from rows", not diff, "%d of %d count keys differ" % (len(diff), len(rc)), "INVALID")
    gate = derived_gate(rc)
    if ledger_json:
        led = json.load(open(ledger_json, encoding="utf-8"))
        scores = led.get("verdict", {}).get("scores", {})
        sdiff = [k for k in LEDGER_SCORE_KEYS if scores.get(k) != gate[k]]
        e1 = [e for e in led.get("evidence", []) if e.get("evidenceId") == "E1"]
        bound = bool(e1) and e1[0].get("contentDigest") == "sha256:" + sha(runs_json)
        add("V8", "the frozen ledger's scores equal the gate quantities re-derived from rows, and its E1 names this record",
            not sdiff and bound, "%d of %d score keys differ; E1 bound %s" % (len(sdiff), len(LEDGER_SCORE_KEYS), bound), "INVALID")
    return finish(checks, gate, runs_json, case_set_json, ledger_json, out_path)


def finish(checks, gate, runs_json, case_set_json, ledger_json, out_path):
    failed = [c for c in checks if c["outcome"] == "FAIL"]
    if any(c["failureKind"] == "INVALID" for c in failed):
        outcome = "INVALID"
    elif failed:
        outcome = "INCOMPLETE"
    else:
        outcome = "VALID"
    doc = {"schemaVersion": SCHEMA_VALIDATION, "outcome": outcome, "checks": checks, "derivedGateQuantities": gate,
           "inputs": {"runs": {"path": str(runs_json), "sha256": sha(runs_json)}, "caseSet": {"path": str(case_set_json), "sha256": sha(case_set_json)},
                      "ledger": {"path": str(ledger_json), "sha256": sha(ledger_json)} if ledger_json else None},
           "validator": {"path": "research/tools/rl15b_validate.py", "sha256": sha(__file__)},
           "interpreter": "CPython " + platform.python_version(),
           "generatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "note": "outcomes are VALID, INCOMPLETE or INVALID; this record carries no verdict and alters no ledger"}
    if out_path:
        json.dump(doc, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(outcome, "|", ", ".join("%s %s" % (c["checkId"], c["outcome"]) for c in checks),
          "|", "; ".join("%s: %s" % (c["checkId"], c["detail"]) for c in failed) or "no failures")
    return {"VALID": 0, "INCOMPLETE": 3, "INVALID": 2}[outcome]


def main(argv):
    if argv[:1] == ["derive"] and len(argv) == 3:
        derive(argv[1], argv[2])
        return 0
    if argv[:1] == ["check"] and len(argv) >= 3:
        ledger = argv[argv.index("--ledger") + 1] if "--ledger" in argv else None
        out = argv[argv.index("--write") + 1] if "--write" in argv else None
        return check(argv[1], argv[2], ledger, out)
    print(__doc__)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
