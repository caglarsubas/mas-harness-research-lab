"""RL-02 v1 analysis (PREREG v1 section 3): H-09b on the head join and the descriptive review-round table.
usage: python3 -I -B rl02_table.py J1.tsv I2.tsv OUT.json   (stdlib only; prints the JSON)"""
import csv
import json
import math
import sys

KINDS = {"PACKET", "DESIGN", "CONTRACT"}
VERDICTS = {"CHANGES_REQUIRED", "PASS_FOR_PUSH", "PASS_FOR_PRECHECK", "PASS_FOR_ADOPTION", "PASS_FOR_BUILD"}


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 4), round(c + h, 4)]


def median(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else None


def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main(j1_path, i2_path, out_path):
    raw = list(csv.DictReader(open(j1_path, encoding="utf-8"), delimiter="\t"))
    rows, dropped = [], 0
    for r in raw:
        rnd = fnum(r["round"])
        if r["kind"] not in KINDS or r["verdict"] not in VERDICTS or rnd is None or rnd != int(rnd):
            dropped += 1
            continue
        r = dict(r)
        r["round"] = int(rnd)
        for c in ("findings", "major", "minor", "note", "disclosures", "interruptions", "duration_s"):
            r[c] = fnum(r[c])
        rows.append(r)
    i2 = list(csv.DictReader(open(i2_path, encoding="utf-8"), delimiter="\t"))
    by_head = {}
    for r in i2:
        by_head.setdefault(r["head8"], []).append(r["conclusion"])
    # H-09b
    push_heads = sorted({r["subject8"] for r in rows if r["kind"] == "PACKET" and r["verdict"] == "PASS_FOR_PUSH" and r["subject8"]})
    matched = [h for h in push_heads if h in by_head]
    refused = [h for h in matched if any(c != "success" for c in by_head[h])]
    h09b = {"push_heads": len(push_heads), "matched": len(matched), "unmatched": len(push_heads) - len(matched),
            "refused": len(refused), "fraction": round(len(refused) / len(matched), 4) if matched else None,
            "wilson95": wilson(len(refused), len(matched))}
    # descriptive
    def bucket(n):
        return "1" if n == 1 else "2" if n == 2 else "3" if n == 3 else "4+"
    per_round = {}
    for r in rows:
        b = per_round.setdefault(bucket(r["round"]), {"rounds": 0, "findings": [], "major": [], "minor": [], "note": [], "disclosures": [], "changes_required": 0, "with_finding": 0})
        b["rounds"] += 1
        for c in ("findings", "major", "minor", "note", "disclosures"):
            if r[c] is not None:
                b[c].append(r[c])
        b["changes_required"] += r["verdict"] == "CHANGES_REQUIRED"
        b["with_finding"] += (r["findings"] or 0) > 0
    desc_round = {}
    for k, b in sorted(per_round.items()):
        n = b["rounds"]
        desc_round[k] = {"rounds": n, "median_findings": median(b["findings"]), "mean_findings": round(sum(b["findings"]) / n, 2),
                         "median_major": median(b["major"]), "median_minor": median(b["minor"]), "median_note": median(b["note"]),
                         "median_disclosures": median(b["disclosures"]),
                         "changes_required_fraction": round(b["changes_required"] / n, 3), "changes_required_wilson95": wilson(b["changes_required"], n),
                         "with_finding_fraction": round(b["with_finding"] / n, 3), "with_finding_wilson95": wilson(b["with_finding"], n)}
    later = [r for r in rows if r["round"] >= 2]
    later_with = sum(1 for r in later if (r["findings"] or 0) > 0)
    by_form = {}
    for f in ("full", "delta"):
        sub = [r for r in rows if r["form"] == f]
        by_form[f] = {"rounds": len(sub), "median_findings": median([r["findings"] for r in sub if r["findings"] is not None]),
                      "changes_required_fraction": round(sum(r["verdict"] == "CHANGES_REQUIRED" for r in sub) / len(sub), 3) if sub else None}
    series = {}
    for r in rows:
        series.setdefault(r["seriesKind"], {}).setdefault(r["packet"], 0)
        series[r["seriesKind"]][r["packet"]] += 1
    by_series = {k: {"series": len(v), "rounds": sum(v.values()), "median_rounds_per_series": median(list(v.values())), "max_rounds": max(v.values())} for k, v in series.items()}
    durations = [r["duration_s"] for r in rows if r["duration_s"] is not None]
    out = {"rows_in": len(raw), "rows_used": len(rows), "dropped_junk": dropped,
           "h09b": h09b,
           "descriptive": {"by_round_index": desc_round,
                           "later_rounds_with_finding": {"rounds": len(later), "with_finding": later_with, "fraction": round(later_with / len(later), 3) if later else None, "wilson95": wilson(later_with, len(later))},
                           "by_form": by_form, "by_series_kind": by_series,
                           "duration_s": {"n": len(durations), "median": median(durations), "max": max(durations) if durations else None},
                           "interruptions": sum(1 for r in rows if (r["interruptions"] or 0) > 0),
                           "rulings": {k: sum(1 for r in rows if r["ruling"] == k) for k in ("KEEP", "PENDING", "VOID")},
                           "verdicts": {v: sum(1 for r in rows if r["verdict"] == v) for v in sorted(VERDICTS)}}}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main(*sys.argv[1:4])
