"""RL-02 v2 (PREREG v2): H-09c carried-finding re-raise and H-09d between-round novelty on J2, plus descriptives.
usage: python3 -I -B rl02_v2.py J2.tsv OUT.json   (stdlib only; ids never printed)"""
import csv
import json
import math
import re
import sys

TOKEN = re.compile(r"^[A-Z0-9]+-[A-Z0-9]+-\d+$")
CARRIED = {"PARTLY", "NOT", "RECORDED"}


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


def main(j2_path, out_path):
    rows = list(csv.DictReader(open(j2_path, encoding="utf-8"), delimiter="\t"))
    for r in rows:
        r["roundRaised"] = int(r["roundRaised"])
        r["statusRound"] = int(r["statusRound"]) if r["statusRound"].isdigit() else None
        r["token"] = bool(TOKEN.match(r["findingId"]))
    tok = [r for r in rows if r["token"]]
    by_id = {}
    for r in tok:
        by_id.setdefault((r["packet"], r["seriesKind"], r["findingId"]), []).append(r["roundRaised"])
    # H-09c
    carried = [r for r in tok if r["latestStatus"] in CARRIED]
    reraised = [r for r in carried if any(x > r["roundRaised"] for x in by_id[(r["packet"], r["seriesKind"], r["findingId"])])]
    h09c = {"carried": len(carried), "reraised": len(reraised), "fraction": round(len(reraised) / len(carried), 4) if carried else None,
            "wilson95": wilson(len(reraised), len(carried)), "no_disposition_rows": sum(1 for r in rows if r["latestStatus"] == "")}
    # H-09d
    later = [r for r in tok if r["roundRaised"] >= 2]
    new = [r for r in later if not any(x < r["roundRaised"] for x in by_id[(r["packet"], r["seriesKind"], r["findingId"])])]
    lo, hi = wilson(len(new), len(later))
    outcome = "INCONCLUSIVE" if len(later) < 40 or lo is None else ("PASS" if lo > 0.5 else ("FAIL" if hi < 0.5 else "INCONCLUSIVE"))
    per_series = {}
    for r in later:
        k = r["packet"] + "/" + r["seriesKind"]
        per_series.setdefault(k, [0, 0])
        per_series[k][1] += 1
        per_series[k][0] += r in new
    h09d = {"later_findings": len(later), "new": len(new), "fraction": round(len(new) / len(later), 4) if later else None, "wilson95": [lo, hi], "outcome": outcome,
            "per_series_new_fraction_distribution": sorted(round(a / b, 2) for a, b in per_series.values())}
    # descriptives
    def bucket(n):
        return "1" if n == 1 else "2" if n == 2 else "3" if n == 3 else "4+"
    sev_by_round, blocks_by_sev, addressed_by_sev, lag = {}, {}, {}, []
    for r in rows:
        sev_by_round.setdefault(bucket(r["roundRaised"]), {}).setdefault(r["severity"], 0)
        sev_by_round[bucket(r["roundRaised"])][r["severity"]] += 1
        blocks_by_sev.setdefault(r["severity"], [0, 0])
        blocks_by_sev[r["severity"]][1] += 1
        blocks_by_sev[r["severity"]][0] += r["blocks"] == "True"
        if r["latestStatus"]:
            addressed_by_sev.setdefault(r["severity"], [0, 0])
            addressed_by_sev[r["severity"]][1] += 1
            addressed_by_sev[r["severity"]][0] += r["latestStatus"] == "ADDRESSED"
            if r["statusRound"] is not None:
                lag.append(r["statusRound"] - r["roundRaised"])
    out = {"rows": len(rows), "lane_token_rows": len(tok), "masked_id_rows": len(rows) - len(tok), "distinct_identities": len(by_id),
           "h09c": h09c, "h09d": h09d,
           "descriptive": {"severity_by_round_index": sev_by_round,
                           "blocks_fraction_by_severity": {k: round(a / b, 3) for k, (a, b) in blocks_by_sev.items()},
                           "addressed_fraction_by_severity": {k: {"fraction": round(a / b, 3), "n": b} for k, (a, b) in addressed_by_sev.items()},
                           "rounds_to_disposition_median": median(lag), "dispositioned": len(lag)}}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main(*sys.argv[1:3])
