"""RL-04 (PREREG v1): leased (committed) vs advisory (bypass HELD, VERSION) over the harness's scaling points, paired by
seed. usage: python3 -I -B rl04_scaling.py EXPORT_TESTS_MAS OUT.json [POINT_ID ...]   (stdlib only; never writes
into the export). Readings per run from the harness's own scaling_readings; the safety counters from measured counts."""
import importlib
import json
import random
import sys
import time
from pathlib import Path

SEED, RESAMPLES = 20261104, 1000
ADVISORY = ("HELD", "VERSION")


def quantiles(xs):
    xs = sorted(xs)
    pick = lambda q: xs[min(len(xs) - 1, int(q * len(xs)))]
    return {"min": xs[0], "p50": pick(0.5), "p95": pick(0.95), "max": xs[-1]}


def main(export, out_path, only):
    export = Path(export).resolve()
    sys.path.insert(0, str(export))
    ledger = importlib.import_module("_ledger")
    config, classes_sha = ledger.load_config()
    spec = config["scaling"]
    safety = spec["safetyCounters"]
    entries = [e for e in spec["points"] if not only or e["id"] in only]
    out = {"classesSha256": classes_sha, "seeds": len(config["seeds"]), "points": {}, "wall_s": {}}
    pairs = []
    for entry in entries:
        t0 = time.monotonic()
        per_arm = {}
        for arm, bypass in (("leased", ()), ("advisory", ADVISORY)):
            runs, overlap_seeds, finished = [], 0, 0
            for seed in config["seeds"]:
                rows, measured = ledger.run(config, entry, seed, bypass=bypass)
                counts = measured["counts"]
                readings, done = ledger.scaling_readings(rows, entry, counts)
                readings["claimOverlap"] = counts.get("claimOverlap", 0)
                readings["safetyAboveZero"] = sorted(n for n in safety if counts.get(n))
                runs.append(readings)
                overlap_seeds += bool(counts.get("claimOverlap"))
                finished += int(done)
            per_arm[arm] = {"finishedSeeds": finished, "claimOverlapSeeds": overlap_seeds,
                            "safetyAboveZeroSeeds": sum(1 for r in runs if r["safetyAboveZero"]),
                            "readings": {n: quantiles([r[n] for r in runs]) for n in ("duplicatedWorkRatioPpm", "completionPpm", "lostWorkPpm", "lastMergeTick")},
                            "_dup": [r["duplicatedWorkRatioPpm"] for r in runs]}
        d = [a - l for a, l in zip(per_arm["advisory"]["_dup"], per_arm["leased"]["_dup"])]
        for arm in per_arm:
            del per_arm[arm]["_dup"]
        out["points"][entry["id"]] = {"family": entry["family"], "workers": entry["workers"], "items": entry["load"]["items"], "arms": per_arm,
                                      "paired_d": {"median": sorted(d)[len(d) // 2], "mean": round(sum(d) / len(d), 1), "positive": sum(x > 0 for x in d), "negative": sum(x < 0 for x in d), "zero": sum(x == 0 for x in d)},
                                      "d_values": d}
        if entry["workers"] >= 2:
            pairs.extend(d)
        out["wall_s"][entry["id"]] = round(time.monotonic() - t0, 2)
    if pairs:
        rng = random.Random(SEED)
        means = sorted(sum(rng.choices(pairs, k=len(pairs))) / len(pairs) for _ in range(RESAMPLES))
        lo, hi = means[int(0.025 * RESAMPLES)], means[int(0.975 * RESAMPLES) - 1]
        out["pooled_n_ge_2"] = {"pairs": len(pairs), "mean_d": round(sum(pairs) / len(pairs), 1), "bootstrap95": [round(lo, 1), round(hi, 1)], "seed": SEED, "resamples": RESAMPLES}
    Path(out_path).write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "points"}, indent=1, sort_keys=True))
    for pid, p in out["points"].items():
        print(pid, p["workers"], "leased dup", p["arms"]["leased"]["readings"]["duplicatedWorkRatioPpm"], "advisory dup", p["arms"]["advisory"]["readings"]["duplicatedWorkRatioPpm"], "overlap seeds L/A", p["arms"]["leased"]["claimOverlapSeeds"], p["arms"]["advisory"]["claimOverlapSeeds"], "d", p["paired_d"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
