"""RL-05 allowlist predicate: evaluates P = R ∧ V ∧ A ∧ I ∧ H ∧ T per merge-decision record (PREREG v1 section 1).
usage: python3 -I -B rl05_predicate.py RECORD_DIR OUT.json > rows.tsv
Emits booleans, counts, enums, PR numbers and dates only; no string value of any record is ever printed."""
import json
import pathlib
import re
import sys

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
BRIDGE_SUFFIX = "/harness-onion"


def tri(value):
    return "MISSING" if value is None else ("TRUE" if value else "FALSE")


def evaluate(record):
    reviews = record.get("reviews")
    r = None
    if isinstance(reviews, list):
        r = len(reviews) > 0
    elif isinstance(reviews, str):
        r = len(reviews) > 0
    elif "packetReviews" in record or "contractReviews" in record:
        r = True
    verify = record.get("verify") if isinstance(record.get("verify"), dict) else None
    v = None if verify is None else (verify.get("conclusion") == "success" and bool(verify.get("checkRun")))
    a = None if "approver" not in record else bool(record.get("approver"))
    i = None if ("decidedBy" not in record or "approver" not in record) else (record.get("decidedBy") != record.get("approver"))
    hb = record.get("headBoundChecks")
    h = None if not isinstance(hb, dict) or not hb else all(x is True for x in hb.values())
    repo = record.get("repository") if isinstance(record.get("repository"), str) else ""
    repo_class = "bridge" if (repo == BRIDGE_SUFFIX[1:] or repo.endswith(BRIDGE_SUFFIX)) else ("hosted" if repo else "unknown")
    t = True if repo_class == "bridge" else (None if repo_class == "unknown" else ("transportApproval" in record))
    conj = {"R": tri(r), "V": tri(v), "A": tri(a), "I": tri(i), "H": tri(h), "T": tri(t)}
    status = "FAIL" if "FALSE" in conj.values() else ("UNEVALUATED" if "MISSING" in conj.values() else "PASS")
    return conj, status, repo_class


def main(record_dir, out_path):
    rows, summary = [], {"records": 0, "merged": 0, "non_merge": 0, "by_status": {}, "by_conjunct": {}, "by_form": {}, "by_repo_class": {}}
    print("\t".join(["file_date", "pr", "merged", "form", "repo_class", "R", "V", "A", "I", "H", "T", "status", "n_reviews", "has_exception", "has_erratum", "has_slips"]))
    for path in sorted(pathlib.Path(record_dir).glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        merged = isinstance(record.get("mergeCommit"), str) and bool(record.get("mergeCommit"))
        decided_clean = (not merged) and record.get("mergeState") == "CLEAN"
        form = "v1" if record.get("schema") == "planeon.merge-decision/v1" else "older"
        conj, status, repo_class = evaluate(record)
        reviews = record.get("reviews")
        n_reviews = len(reviews) if isinstance(reviews, list) else (1 if isinstance(reviews, str) and reviews else 0)
        pr = record.get("pr") if isinstance(record.get("pr"), int) else ""
        date = DATE.match(path.name).group(0) if DATE.match(path.name) else ""
        flags = ["exception" in record or "ownerException" in record, "erratumFor" in record, isinstance(record.get("slips"), list)]
        print("\t".join(str(x) for x in [date, pr, merged, form, repo_class] + [conj[k] for k in "RVAIHT"] + [status if merged else "n/a", n_reviews] + flags))
        summary["records"] += 1
        if not merged:
            summary["non_merge"] += 1
            if decided_clean:
                summary.setdefault("descriptive_earliest_form_clean", {}).setdefault(status, 0)
                summary["descriptive_earliest_form_clean"][status] += 1
            continue
        summary["merged"] += 1
        summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        for k, val in conj.items():
            summary["by_conjunct"].setdefault(k, {}).setdefault(val, 0)
            summary["by_conjunct"][k][val] += 1
        summary["by_form"].setdefault(form, {}).setdefault(status, 0)
        summary["by_form"][form][status] += 1
        summary["by_repo_class"].setdefault(repo_class, {}).setdefault(status, 0)
        summary["by_repo_class"][repo_class][status] += 1
        if status == "FAIL":
            summary.setdefault("fail_prs", []).append(pr)
    json.dump(summary, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
