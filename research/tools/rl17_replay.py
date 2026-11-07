"""RL-17 (H-27, replay half): determinism of the exported simulation harness's effect log, reproduction of the
committed REPLAY_STALE class row, and refusal of duplicated and stale (reordered) board operations replayed after a
run. usage: python3 -I -B rl17_replay.py EXPORT_TESTS_MAS OUT.json [--seeds N]
The export is the pinned git-archive of conformance-labs tests/mas (no oracle member); it is imported by path from an
isolated scratch folder; nothing is written into it. Output: counts and digests only, no row text."""
import hashlib
import importlib
import json
import sys
import time
from pathlib import Path

VERSIONED = ("ACQUIRE", "ASSIGN", "RENEW", "RELEASE", "MERGE")
OP_FIELDS = ("agent", "to", "item", "op", "opId", "expectedVersion", "claimOpId", "workDigest")


def op_from_row(r):
    op = {k: r[k] for k in OP_FIELDS if r.get(k) is not None}
    op["retryOf"] = r.get("retryOf")
    if r.get("scheduledEvent") is not None:
        op["event"] = r["scheduledEvent"]
    return op


def replay_log(sim_mod, classes_mod, config, cls, seed, rows):
    """H-27d (PREREG v2): the recorded operation sequence replayed in order at its ticks through a fresh simulation's
    board (never run); the answers compared with the recorded ones, by operation kind."""
    fresh = sim_mod.Sim(config, cls, seed, (), classes_mod.scenario_for(cls))
    ops = [r for r in rows if r["kind"] == "BOARD_ANSWER"]
    agree = {}; total = {}; first_divergence = None; exceptions = 0
    for i, r in enumerate(ops):
        kind = r["op"]; total[kind] = total.get(kind, 0) + 1
        try:
            ans = fresh.board.apply(r["t"], op_from_row(r))
            same = ans["result"]["answer"] == r["answer"] and ans["row"]["recordVersionBefore"] == r["recordVersionBefore"]
        except Exception:
            exceptions += 1; same = False
        if same:
            agree[kind] = agree.get(kind, 0) + 1
        elif first_divergence is None:
            first_divergence = {"index": i, "op": kind, "recordedAnswer": r["answer"]}
    versioned_total = sum(total.get(k, 0) for k in VERSIONED); versioned_agree = sum(agree.get(k, 0) for k in VERSIONED)
    return {"ops": len(ops), "agreeByOp": agree, "totalByOp": total, "versionedTotal": versioned_total, "versionedAgree": versioned_agree,
            "claimMergeSequenceIdentical": versioned_total > 0 and versioned_agree == versioned_total, "firstDivergence": first_divergence, "exceptions": exceptions}


def digest_rows(rows):
    return hashlib.sha256(json.dumps(rows, sort_keys=True, default=str).encode()).hexdigest()


def strip(row):
    return json.loads(json.dumps(row, sort_keys=True))


def main(export, out_path, n_seeds):
    export = Path(export).resolve()
    sys.path.insert(0, str(export))
    sim_mod = importlib.import_module("_sim"); classes_mod = importlib.import_module("_classes"); ledger = importlib.import_module("_ledger")
    config, classes_sha = ledger.load_config()
    committed = json.loads((export / "results.json").read_bytes())
    seeds = config["seeds"][:n_seeds] if n_seeds else config["seeds"]
    out = {"export": export.name, "classesSha256": classes_sha, "committedClassesSha256": committed["classesSha256"],
           "classesShaMatch": classes_sha == committed["classesSha256"], "seeds": len(seeds), "classes": [c["id"] for c in config["classes"]],
           "determinism": [], "replay": [], "logReplay": [], "wall_s": {}}
    t0 = time.monotonic()
    # H-27a determinism: two runs per class and seed, whole-log digests compared
    for cls in config["classes"]:
        for seed in seeds:
            rows1, _ = ledger.run(config, cls, seed)
            rows2, _ = ledger.run(config, cls, seed)
            d1, d2 = digest_rows(rows1), digest_rows(rows2)
            out["determinism"].append({"class": cls["id"], "seed": seed, "rows": len(rows1), "identical": d1 == d2, "digest": d1[:16]})
    out["wall_s"]["determinism"] = round(time.monotonic() - t0, 2)
    # H-27b: the committed REPLAY_STALE class row (C3) reproduces exactly
    t0 = time.monotonic()
    c3 = next(c for c in config["classes"] if c["kind"] == "REPLAY_STALE")
    row = ledger.class_row(config, c3); c = next(r for r in committed["classes"] if r["id"] == c3["id"])
    out["replayStale"] = {"id": c3["id"], "result": row.get("result"), "committedResult": c.get("result"), "sameWholeRow": strip(row) == strip(c),
                          "differingTopLevelKeys": sorted(k for k in set(row) | set(c) if strip(row.get(k)) != strip(c.get(k)))}
    out["wall_s"]["replayStale"] = round(time.monotonic() - t0, 2)
    # H-27c: duplicated and stale replays of accepted board operations after the run
    t0 = time.monotonic()
    for cls in config["classes"]:
        for seed in seeds:
            sim = sim_mod.Sim(config, cls, seed, (), classes_mod.scenario_for(cls))
            rows = sim.run()
            accepted = [r for r in rows if r["kind"] == "BOARD_ANSWER" and r["answer"] == "ACCEPTED" and r["retryOf"] is None]
            t_end = sim.cfg["deadline"]
            out["logReplay"].append(dict(replay_log(sim_mod, classes_mod, config, cls, seed, rows), **{"class": cls["id"], "seed": seed}))
            rec = {"class": cls["id"], "seed": seed, "accepted": len(accepted), "dupAttempts": 0, "dupRefusedDuplicateId": 0, "dupChanged": 0, "dupOtherAnswer": {},
                   "staleAttempts": 0, "staleStaleVersion": 0, "staleOtherRefusal": 0, "staleAccepted": 0, "staleChanged": 0, "staleNotPosable": 0, "staleAnswers": {}, "exceptions": 0}
            for r in accepted:
                op = op_from_row(r)
                # (i) duplicate: the same operation, same opId
                rec["dupAttempts"] += 1
                try:
                    ans = sim.board.apply(t_end, dict(op))
                    a = ans["result"]["answer"]; changed = bool(ans["row"]["changed"])
                    if a == "DUPLICATE_ID": rec["dupRefusedDuplicateId"] += 1
                    else: rec["dupOtherAnswer"][a] = rec["dupOtherAnswer"].get(a, 0) + 1
                    if changed: rec["dupChanged"] += 1
                except Exception:
                    rec["exceptions"] += 1
                # (ii) stale (reordered): a fresh opId with the original expectedVersion, versioned operations only
                if r["op"] in VERSIONED and r.get("expectedVersion") is not None:
                    current = sim.board.records.get(r["item"], {}).get("version") if r.get("item") is not None else None
                    if current is None or current == r["expectedVersion"]:
                        rec["staleNotPosable"] += 1  # the version rule could not refuse it (PREREG v2: excluded and counted)
                        continue
                    rec["staleAttempts"] += 1
                    op2 = dict(op); op2["opId"] = str(r["opId"]) + "-RL17"
                    try:
                        ans = sim.board.apply(t_end, op2)
                        a = ans["result"]["answer"]; changed = bool(ans["row"]["changed"])
                        rec["staleAnswers"][a] = rec["staleAnswers"].get(a, 0) + 1
                        if a == "ACCEPTED": rec["staleAccepted"] += 1
                        elif a == "STALE_VERSION": rec["staleStaleVersion"] += 1
                        else: rec["staleOtherRefusal"] += 1
                        if changed: rec["staleChanged"] += 1
                    except Exception:
                        rec["exceptions"] += 1
            out["replay"].append(rec)
    out["wall_s"]["replay"] = round(time.monotonic() - t0, 2)
    det = out["determinism"]; rep = out["replay"]
    out["counts"] = {"pairs": len(det), "identical": sum(1 for d in det if d["identical"]),
                     "dupAttempts": sum(r["dupAttempts"] for r in rep), "dupRefusedDuplicateId": sum(r["dupRefusedDuplicateId"] for r in rep), "dupChanged": sum(r["dupChanged"] for r in rep),
                     "staleAttempts": sum(r["staleAttempts"] for r in rep), "staleStaleVersion": sum(r["staleStaleVersion"] for r in rep), "staleOtherRefusal": sum(r["staleOtherRefusal"] for r in rep), "staleAccepted": sum(r["staleAccepted"] for r in rep), "staleChanged": sum(r["staleChanged"] for r in rep), "staleNotPosable": sum(r["staleNotPosable"] for r in rep),
                     "exceptions": sum(r["exceptions"] for r in rep),
                     "logReplayRuns": len(out["logReplay"]), "logReplayIdentical": sum(1 for x in out["logReplay"] if x["claimMergeSequenceIdentical"]), "logReplayExceptions": sum(x["exceptions"] for x in out["logReplay"]),
                     "logReplayAgreeByOp": {k: [sum(x["agreeByOp"].get(k, 0) for x in out["logReplay"]), sum(x["totalByOp"].get(k, 0) for x in out["logReplay"])] for k in sorted({k for x in out["logReplay"] for k in x["totalByOp"]})}}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(out["counts"]), "| replayStale sameWholeRow", out["replayStale"]["sameWholeRow"], "| wall", out["wall_s"])


if __name__ == "__main__":
    n = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 0
    main(sys.argv[1], sys.argv[2], n)
