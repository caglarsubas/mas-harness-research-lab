"""Outcome collector (R13 issue 4, 2026-11-09): the successor to prereg_review_meta.py's stop anchors. The cohort is every
experiment id in the register's "Experiments started" table; each must hold an OUTCOME.json in the expected form; an
absent or malformed record is a failure (exit 1), never a no-stop. The 001 meta-review snapshot and its checker are
untouched. Counts only; no prose parsed.

usage: python3 -I -B outcome_collect.py REGISTER_MD EXPERIMENTS_DIR [--from RL-nn] [--write OUT_JSON] [--check OUT_JSON]
  --from RL-nn   restricts the cohort to ids at or after RL-nn in the table's order (the H-36 cohort starts at RL-23)
  --write        writes the summary; --check compares a written summary with the current collection (exit 1 on a difference)
Standard library only."""
import hashlib
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import outcome_record as OR  # noqa: E402

ROW = re.compile(r"^\|\s*(RL-\d{2}[a-z]?)\s*\|", re.M)


def cohort_ids(register_md):
    text = pathlib.Path(register_md).read_text(encoding="utf-8")
    tail = text.split("## Experiments started", 1)[1]
    return ROW.findall(tail)


def collect(register_md, exp_dir, start=None):
    ids = cohort_ids(register_md)
    if start:
        if start not in ids:  # a cohort that has not started yet is an empty, valid cohort
            ids = []
        else:
            ids = ids[ids.index(start):]
    absent, defective, rows = [], [], []
    for exp in ids:
        p = pathlib.Path(exp_dir) / exp / "OUTCOME.json"
        if not p.exists():
            absent.append(exp)
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        problems = OR.validate(doc)
        if problems or doc.get("experiment") != exp:
            defective.append(exp)
            continue
        for a in doc["attempts"]:
            rows.append({"experiment": exp, "attempt": a["attempt"], "preregVersion": a.get("preregVersion"), "reviewRounds": a.get("reviewRounds"),
                         "reviewVerdict": a.get("reviewVerdict"), "stageReached": a["stageReached"], "outcome": a["outcome"], "class": a["class"],
                         "stopStage": (a.get("stop") or {}).get("stage"), "detector": (a.get("stop") or {}).get("detector"),
                         "evidenceSha256": (a.get("evidence") or {}).get("sha256"), "recordSha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    by_outcome = {k: sum(1 for r in rows if r["outcome"] == k) for k in OR.OUTCOMES}
    by_class = {k: sum(1 for r in rows if r["class"] == k) for k in OR.CLASSES}
    first_round_pass = sum(1 for r in rows if r["attempt"] == 1 and r["reviewRounds"] and r["reviewVerdict"] == "PASS" and r["reviewRounds"] == 1)
    reviewed_first_attempts = sum(1 for r in rows if r["attempt"] == 1 and r["reviewRounds"])
    return {"schemaVersion": "planeon.research.outcome-summary/v1", "cohort": {"from": start, "ids": ids, "count": len(ids)},
            "absent": absent, "defective": defective, "attempts": len(rows), "byOutcome": by_outcome, "byClass": by_class,
            "stops": [r for r in rows if r["outcome"] == "STOPPED"], "pending": [r["experiment"] for r in rows if r["outcome"] == "PENDING"],
            "firstRoundPass": {"numerator": first_round_pass, "denominator": reviewed_first_attempts,
                               "definition": "first attempts whose only review round passed, over first attempts that had a review"},
            "rows": rows}


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 64
    start = argv[argv.index("--from") + 1] if "--from" in argv else None
    s = collect(argv[0], argv[1], start)
    ok = not s["absent"] and not s["defective"]
    print("cohort %d ids (from %s): attempts %d, outcomes %s, classes with events %s, stops %d, pending %d, absent %d, defective %d, first-round PASS %d of %d" % (
        s["cohort"]["count"], start or "the first", s["attempts"], json.dumps(s["byOutcome"]),
        json.dumps({k: v for k, v in s["byClass"].items() if v and k != "NONE"}), len(s["stops"]), len(s["pending"]),
        len(s["absent"]), len(s["defective"]), s["firstRoundPass"]["numerator"], s["firstRoundPass"]["denominator"]))
    if "--write" in argv:
        out = argv[argv.index("--write") + 1]
        json.dump(s, open(out, "w", encoding="utf-8"), indent=1, sort_keys=True)
        print("summary written")
    if "--check" in argv:
        ref = json.load(open(argv[argv.index("--check") + 1], encoding="utf-8"))
        same = all(ref.get(k) == s.get(k) for k in ("cohort", "absent", "defective", "attempts", "byOutcome", "byClass", "stops", "pending", "firstRoundPass", "rows"))
        print("summary check:", "SAME" if same else "DIFFERENT")
        ok = ok and same
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
