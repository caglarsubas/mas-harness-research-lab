"""RL-08 (PREREG v1): concentration of the chain's cost from the published cost report. usage: python3 -I -B
rl08_cost.py COST_REPORT AB_JSON OUT.json   (stdlib; prints the summary; no local path in the output)"""
import json
import sys


def gini(values):
    xs = sorted(v for v in values if v >= 0)
    n = len(xs)
    if n == 0 or sum(xs) == 0:
        return None
    cum = 0.0
    for i, x in enumerate(xs, 1):
        cum += i * x
    return round((2 * cum) / (n * sum(xs)) - (n + 1) / n, 4)


def shares(d, top):
    items = sorted(d.items(), key=lambda kv: -kv[1])
    total = sum(v for _, v in items)
    return {"n": len(items), "total": total, "top_k": top, "top_k_share": round(sum(v for _, v in items[:top]) / total, 4) if total else None,
            "top_5": [(k, round(v / total, 4)) for k, v in items[:5]] if total else [], "gini": gini(d.values())}


def main(cost_path, ab_path, out_path):
    r = json.load(open(cost_path)); ab = json.load(open(ab_path))
    a = r["argv63"]
    per_file = {k: v[0] for k, v in a["perFile"].items()}
    layers = {k: v.get("bytes:read:authority", 0) for k, v in r["passC"].items() if v}
    reads = {k: v.get("reads:authority", 0) for k, v in r["passC"].items() if v}
    own = {k: v.get("call:_checked_own_authority_raw", 0) for k, v in r["passC"].items() if v}
    argv = {"argv%02d" % x["argv"]: x["cpu"] for x in r["argv"]}
    out = {
        "B2_per_file_cpu": shares(per_file, max(1, round(0.10 * len(per_file)))),
        "B3_per_layer_authority_bytes": shares(layers, max(1, round(0.10 * len(layers)))),
        "per_layer_authority_reads": shares(reads, max(1, round(0.10 * len(reads)))),
        "per_layer_own_authority_calls": shares(own, max(1, round(0.10 * len(own)))),
        "B1_per_argv_cpu": dict(shares(argv, 3), top_1_share=round(max(argv.values()) / sum(argv.values()), 4)),
        "authority_reads_per_path": shares(r["authorityReadsPerVerify"]["perPath"], 5),
        "B4_generic_scaffold_share": round(a["genericScaffoldCpu"] / a["cpuSeconds"], 4),
        "argv63_cpu_s": a["cpuSeconds"], "argv_total_cpu_s": round(sum(argv.values()), 1), "argv_total_wall_s": round(sum(x["wall"] for x in r["argv"]), 1), "tests": a["tests"],
        "scaffold_class_cpu_s": {k: v[0] for k, v in a["scaffoldClass"].items()},
        "ab_keys": sorted(ab.keys()) if isinstance(ab, dict) else len(ab), "run": r["run"],
    }
    b2, b3 = out["B2_per_file_cpu"]["top_k_share"], out["B3_per_layer_authority_bytes"]["top_k_share"]
    out["gate"] = {"B2_top_decile_share": b2, "B3_top_decile_share": b3,
                   "outcome": "PASS" if b2 >= 0.5 and b3 >= 0.5 else ("FAIL" if b2 < 0.3 or b3 < 0.3 else "INCONCLUSIVE")}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main(*sys.argv[1:4])
