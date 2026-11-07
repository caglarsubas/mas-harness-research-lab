"""RL-06 (PREREG v1): throughput and cost series from the lab's allowlist rows, and the MON-id taxonomy from the
handoff files. usage: python3 -I -B rl06_process.py HANDOFF_DIR I1_ROWS RL05_ROWS I2_TSV OUT.json   (counts only)"""
import csv
import datetime
import hashlib
import json
import pathlib
import re
import statistics
import sys

ID = re.compile(r"\bMON-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
CATS = [
    ("PRIVACY", "PRIVACY HANDLE PATH PATHS SCRUB MASK MASKED NAME NAMES HASH HASHES REDACT EMAIL URL TOKEN"),
    ("COMPUTE", "HEAVY LOAD GO HOLD PAUSE VERIFY DRY PRECHECK OLLAMA QUIET SLOT CAP TIMEOUT"),
    ("BRIEFS", "BRIEF BRIEFS KIT KITS REVIEWER REVIEW PIN PINS STOP CLASSIFIER QUOTING GLOB"),
    ("FILES", "SCRATCH TRASH BASETEMP TOOLS COPY LINK LINKS SYMLINK CHAIN SNAPSHOT EXPORT"),
    ("MERGE", "PUSH MERGE PR HEAD APPROVAL TRANSPORT BUNDLE ORDER PUBLISH RESUME"),
    ("SESSION", "USAGE CLEAR HANDOVER SESSION SESSIONS COMPACTION CHECKIN"),
]
CATS = [(name, set(words.split())) for name, words in CATS]


def category(mon_id):
    segs = mon_id.split("-")[1:]
    named = [s for s in segs if not s.isdigit()]
    for name, words in CATS:
        if any(s in words for s in named):
            return name
    return "OTHER"


def slot_of(mon_id):
    segs = mon_id.split("-")[1:]
    return int(segs[0]) if segs and segs[0].isdigit() and 200 <= int(segs[0]) <= 400 else None


def main(handoff, i1_path, rl05_path, i2_path, out_path):
    files = sorted(pathlib.Path(handoff).glob("*.md"))
    digests = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()[:8] for f in files}
    all_ids, rule_ids = set(), set()
    for f in files:
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            found = ID.findall(line)
            all_ids.update(found)
            if found and re.search(r"\brules?\b", line, re.IGNORECASE):
                rule_ids.update(found)
    def table(ids):
        counts = {}
        for i in ids:
            counts[category(i)] = counts.get(category(i), 0) + 1
        return dict(sorted(counts.items()))
    slot_rules = [(slot_of(i), category(i)) for i in rule_ids if slot_of(i) is not None]
    slots = sorted(s for s, _ in slot_rules)
    median_slot = slots[len(slots) // 2] if slots else None
    early = {c for s, c in slot_rules if s < median_slot} if slots else set()
    late = [(s, c) for s, c in slot_rules if s >= median_slot] if slots else []
    late_known = sum(1 for _, c in late if c in early and c != "OTHER")
    rule_table = table(rule_ids)
    other_frac = rule_table.get("OTHER", 0) / len(rule_ids) if rule_ids else None
    taxonomy = {"all_ids": len(all_ids), "rule_ids": len(rule_ids), "all_by_category": table(all_ids), "rule_by_category": rule_table,
                "other_fraction_rules": round(other_frac, 3) if other_frac is not None else None,
                "slot_bound_rule_ids": len(slot_rules), "median_slot": median_slot, "early_categories": sorted(early),
                "late_ids": len(late), "late_in_early_category": late_known, "late_fraction": round(late_known / len(late), 3) if late else None,
                "rule_ids_by_slot_decile": {}}
    if slots:
        for s, c in slot_rules:
            k = "%d-%d" % (s // 10 * 10, s // 10 * 10 + 9)
            taxonomy["rule_ids_by_slot_decile"].setdefault(k, {}).setdefault(c, 0)
            taxonomy["rule_ids_by_slot_decile"][k][c] += 1
    # throughput and cost
    rows5 = [r for r in csv.DictReader(open(rl05_path, encoding="utf-8"), delimiter="\t") if r["merged"] == "True"]
    rows1 = {r["pr"] + "|" + r["file_date"]: r for r in csv.DictReader(open(i1_path, encoding="utf-8"), delimiter="\t")}
    weeks = {}
    for r in rows5:
        d = datetime.date.fromisoformat(r["file_date"]); wk = "%d-W%02d" % d.isocalendar()[:2]
        weeks.setdefault(wk, {"bridge": 0, "hosted": 0, "unknown": 0})
        weeks[wk][r["repo_class"]] = weeks[wk].get(r["repo_class"], 0) + 1
    with_date = sum(1 for r in rows5 if r["file_date"])
    elapsed = [float(rows1[r["pr"] + "|" + r["file_date"]]["elapsed_s"]) for r in rows5 if (r["pr"] + "|" + r["file_date"]) in rows1 and rows1[r["pr"] + "|" + r["file_date"]]["elapsed_s"]]
    reviews = [int(r["n_reviews"]) for r in rows5 if int(r["n_reviews"]) > 0]
    i2 = [float(r["elapsed_s"]) for r in csv.DictReader(open(i2_path, encoding="utf-8"), delimiter="\t")]
    days = (max(datetime.date.fromisoformat(r["file_date"]) for r in rows5) - min(datetime.date.fromisoformat(r["file_date"]) for r in rows5)).days + 1
    cov = {"merged": len(rows5), "with_date": with_date, "with_verify_elapsed": len(elapsed), "with_review_count": len(reviews)}
    cov["min_coverage"] = round(min(with_date, len(elapsed), len(reviews)) / len(rows5), 3)
    throughput = {"window_days": days, "merges_per_day": round(len(rows5) / days, 2), "merges_per_week_by_class": dict(sorted(weeks.items())),
                  "verify_s_per_merge": {"n": len(elapsed), "median": statistics.median(elapsed), "min": min(elapsed), "max": max(elapsed)},
                  "verify_s_per_harness_onion_run": {"n": len(i2), "median": statistics.median(i2), "min": min(i2), "max": max(i2)},
                  "review_rounds_per_merge": {"n": len(reviews), "median": statistics.median(reviews), "min": min(reviews), "max": max(reviews)}}
    out = {"handoff_file_digests": digests, "coverage": cov, "throughput": throughput, "taxonomy": taxonomy}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps({k: out[k] for k in ("coverage", "throughput", "taxonomy")}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main(*sys.argv[1:6])
