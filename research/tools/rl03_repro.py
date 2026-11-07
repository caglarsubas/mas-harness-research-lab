"""RL-03 reproduction (PREREG v1): recompute the four breach class rows (C2, C5, C7, C9) and the arms section from a
git-archive export of the conformance-labs simulation harness at a pinned commit, and compare with the committed
ledger rows in memory. Never writes into the export; never touches results.json or campaign-record.json.
usage: python3 -I -B rl03_repro.py EXPORT_TESTS_MAS OUT.json [--timing | --classes | --arms]
  --timing: one run (C2, first seed), wall time only.   --classes: the four class rows.   --arms: the arms section.
Runs with TMPDIR in the lab's scratch; stdlib only; the export directory is put on sys.path by this script (-I)."""
import importlib
import json
import sys
import time
from pathlib import Path

CLASSES = ("C2", "C5", "C7", "C9")
RATIOS = ("completionPpm", "duplicatedWorkRatioPpm", "lostWorkPpm")


def strip(row):
    """The comparable part of a class row: everything except per-seed readings lists that the ledger may elide."""
    return json.loads(json.dumps(row, sort_keys=True))


def main(export, out_path, mode):
    export = Path(export).resolve()
    sys.path.insert(0, str(export))
    ledger = importlib.import_module("_ledger")
    config, classes_sha = ledger.load_config()
    committed = json.loads((export / "results.json").read_bytes())
    out = {"export": str(export.name), "classesSha256": classes_sha, "committedClassesSha256": committed["classesSha256"],
           "classesShaMatch": classes_sha == committed["classesSha256"], "mode": mode, "seeds": len(config["seeds"]), "wall_s": {}}
    by_id = {c["id"]: c for c in config["classes"]}
    committed_rows = {r["id"]: r for r in committed["classes"]}
    if mode == "--timing":
        t0 = time.monotonic()
        rows, measured = ledger.run(config, by_id["C2"], config["seeds"][0])
        out["wall_s"]["one_run_C2"] = round(time.monotonic() - t0, 3)
        out["one_run_counts_keys"] = sorted(measured.get("counts", {}).keys())
    if mode == "--classes":
        out["classes"] = {}
        for cid in CLASSES:
            t0 = time.monotonic()
            row = ledger.class_row(config, by_id[cid])
            out["wall_s"][cid] = round(time.monotonic() - t0, 3)
            c = committed_rows[cid]
            same_result = row.get("result") == c.get("result")
            same_gates = strip(row.get("gates")) == strip(c.get("gates"))
            rq, cq = row.get("defended", {}).get("quantiles"), c.get("defended", {}).get("quantiles")
            same_quantiles = strip(rq) == strip(cq)
            same_row = strip(row) == strip(c)
            out["classes"][cid] = {"result": row.get("result"), "committedResult": c.get("result"), "sameResult": same_result,
                                   "sameGates": same_gates, "sameDefendedQuantiles": same_quantiles, "sameWholeRow": same_row,
                                   "duplicatedWorkRatioPpm": (rq or {}).get("duplicatedWorkRatioPpm"),
                                   "committedDuplicatedWorkRatioPpm": (cq or {}).get("duplicatedWorkRatioPpm"),
                                   "differingTopLevelKeys": sorted(k for k in set(row) | set(c) if strip(row.get(k)) != strip(c.get(k)))}
    if mode == "--arms":
        t0 = time.monotonic()
        arms = ledger.arms_section(config)
        out["wall_s"]["arms"] = round(time.monotonic() - t0, 3)
        c_arms = committed["arms"]
        key = lambda r: (r["arm"], r["class"])
        got = {key(r): r for r in arms["results"]}
        exp = {key(r): r for r in (c_arms["results"] if isinstance(c_arms["results"], list) else c_arms["results"].values())}
        out["arms"] = {"%s/%s" % k: {"sameQuantiles": strip(got[k]["quantiles"]) == strip(exp[k]["quantiles"]) if k in exp else None,
                                     "sameTotals": strip(got[k]["totals"]) == strip(exp[k]["totals"]) if k in exp else None,
                                     "duplicatedWorkRatioPpm": got[k]["quantiles"]["duplicatedWorkRatioPpm"],
                                     "wouldHoldBounds": got[k]["wouldHoldBounds"]} for k in sorted(got)}
        out["armsAllSame"] = all(v["sameQuantiles"] and v["sameTotals"] for v in out["arms"].values())
    Path(out_path).write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({k: out[k] for k in out if k not in ("arms",)}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "--classes")
