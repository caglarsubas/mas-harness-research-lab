"""RL-15b acceptance-boundary check (R13 issue 3; charter step 1b (vii)): derives five mutated copies of a run record
deterministically, runs the frozen evaluator and the companion validator on the original and on each copy, and writes
the table. The frozen evaluator's output on a mutated copy is reported as what it prints; nothing here edits a ledger.

usage: python3 -I -B rl15b_boundary.py RUNS_JSON CASE_SET_JSON EVAL_PY PREREG_MD RUN_RECORD_MD RESULTS_JSON OUT_DIR
Writes OUT_DIR/<mutation>.json copies, OUT_DIR/<mutation>.ledger.json evaluator outputs, OUT_DIR/boundary.json table.
Standard library only; sub-second."""
import copy
import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rl15b_validate as V  # noqa: E402


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def mutations(rec):
    """Each returns (name, description, record, counts_recomputed)."""
    out = []
    m = copy.deepcopy(rec)
    m["runs"] = [r for r in m["runs"] if r["class"] != "M1"]
    m["counts"] = V.recount(m["runs"])
    out.append(("drop_class_M1", "every M1 row removed, every aggregate recomputed (denominator 14, M1 reads [0, 0, 0])", m, True))
    m = copy.deepcopy(rec)
    m["runs"] = [r for r in m["runs"] if r["class"] != "C"]
    m["counts"] = V.recount(m["runs"])
    out.append(("drop_controls", "every control removed, aggregates recomputed (controls 0 of 0)", m, True))
    m = copy.deepcopy(rec)
    first = next(i for i, r in enumerate(m["runs"]) if r["class"] != "C")
    r = m["runs"][first]
    r.update({"exit": 0, "refused": False, "attributed": False, "attributedToNewRule": False, "attributedToOlderRule": False,
              "crashed": False, "message": "", "messageLength": 0})
    out.append(("stale_counts", "the first seeded row set to built and unattributed with exit 0, the supplied counts kept as they were", m, False))
    m = copy.deepcopy(rec)
    m["runs"].append(copy.deepcopy(m["runs"][1]))
    m["counts"] = V.recount(m["runs"])
    out.append(("duplicate_case", "the second seeded row appended again, aggregates recomputed (denominator 18 with one identity twice)", m, True))
    m = copy.deepcopy(rec)
    idx = next(i for i, r in enumerate(m["runs"]) if r["class"] == "M3")
    del m["runs"][idx]
    m["counts"] = V.recount(m["runs"])
    out.append(("missing_case", "one M3 row removed, aggregates recomputed (denominator 16, M3 reads [2, 2, 2])", m, True))
    return out


def run_eval(py, eval_py, runs, prereg, run_record, out):
    p = subprocess.run([py, "-I", "-B", str(eval_py), str(runs), str(prereg), str(run_record), str(out)], capture_output=True, text=True, timeout=60)
    led = json.load(open(out, encoding="utf-8")) if pathlib.Path(out).exists() else {}
    status = led.get("verdict", {}).get("status", "NO_OUTPUT exit %d" % p.returncode)
    scores = led.get("verdict", {}).get("scores", {})
    return status, {k: scores.get(k) for k in ("catchable", "catchable_refused", "controls", "controls_refused")}


def main(runs_json, case_set, eval_py, prereg, run_record, results_json, out_dir):
    out_dir = pathlib.Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rec = json.load(open(runs_json, encoding="utf-8"))
    rows = []
    py = sys.executable
    # the original
    status, sc = run_eval(py, eval_py, runs_json, prereg, run_record, out_dir / "original.ledger.json")
    vcode = V.check(runs_json, case_set, results_json, str(out_dir / "original.validation.json"))
    rows.append({"mutation": "original", "description": "the committed record, unchanged", "countsRecomputed": None,
                 "recordSha256": sha(runs_json), "frozenEvaluator": status, "frozenEvaluatorScores": sc,
                 "validator": {0: "VALID", 3: "INCOMPLETE", 2: "INVALID"}[vcode]})
    for name, desc, m, recomputed in mutations(rec):
        p = out_dir / (name + ".json")
        json.dump(m, open(p, "w", encoding="utf-8"), indent=1, sort_keys=True)
        status, sc = run_eval(py, eval_py, p, prereg, run_record, out_dir / (name + ".ledger.json"))
        vcode = V.check(str(p), case_set, None, str(out_dir / (name + ".validation.json")))
        rows.append({"mutation": name, "description": desc, "countsRecomputed": recomputed, "recordSha256": sha(p),
                     "frozenEvaluator": status, "frozenEvaluatorScores": sc,
                     "validator": {0: "VALID", 3: "INCOMPLETE", 2: "INVALID"}[vcode]})
    table = {"schemaVersion": "planeon.research.acceptance-boundary/v1", "experiment": "RL-15b",
             "inputs": {"runs": sha(runs_json), "caseSet": sha(case_set), "frozenEvaluator": sha(eval_py), "ledger": sha(results_json),
                        "validator": sha(HERE / "rl15b_validate.py"), "boundaryTool": sha(__file__)},
             "rows": rows,
             "completion": {"originalValid": rows[0]["validator"] == "VALID",
                            "everyMutationRejected": all(r["validator"] != "VALID" for r in rows[1:]),
                            "frozenEvaluatorPassesMutations": sum(1 for r in rows[1:] if r["frozenEvaluator"] == "PASS")}}
    json.dump(table, open(out_dir / "boundary.json", "w", encoding="utf-8"), indent=1, sort_keys=True)
    for r in rows:
        print("%-16s evaluator %-6s validator %-10s %s" % (r["mutation"], r["frozenEvaluator"], r["validator"], r["description"]))
    print("completion:", json.dumps(table["completion"]))


if __name__ == "__main__":
    main(*sys.argv[1:8])
