"""RL-18 (H-31): the CONF-MAS arms study re-expressed as MAS-RA-002 run manifests, evaluation records and
distribution-gate comparisons, with the lab's own integer implementation of the gate checked against the contract's
vectors first. usage: python3 -I -B rl18_manifest.py EXPORT_TESTS_MAS CONTRACT_DIR HARNESS_COMMIT OUT.json
Standard library only; deterministic; counts, digests and statistics in the output, no record text."""
import hashlib
import importlib
import json
import math
import re
import sys
from pathlib import Path

SCHEMA_IDS = {"split": "split-declaration", "manifest": "run-manifest", "record": "evaluation-record", "comparison": "distribution-gate", "selection": "selection-record"}
METRICS = (("completionPpm", +1), ("duplicatedWorkRatioPpm", -1), ("lostWorkPpm", -1))  # +1 higher is better; -1 lower is better: score = 1e6 - ratio
TOLERANCE = {"version": "tolerance-v1", "ppm": 10000}
WRITTEN, STARTED = "2026-11-05T00:00:00Z", "2026-11-05T00:00:01Z"


def sha(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


def canon(doc) -> bytes:
    return json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


# ---------------------------------------------------------------- a JSON Schema subset validator (the contract's keywords)
def validate(schema, doc, path="$"):
    """Returns None when valid, else the path and keyword of the first violation."""
    if "oneOf" in schema:
        oks = [b for b in schema["oneOf"] if validate(b, doc, path) is None]
        return None if len(oks) == 1 else path + " oneOf(%d)" % len(oks)
    if "const" in schema and doc != schema["const"]:
        return path + " const"
    if "enum" in schema and doc not in schema["enum"]:
        return path + " enum"
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        ok = any((tt == "null" and doc is None) or (tt == "boolean" and isinstance(doc, bool)) or (tt == "integer" and isinstance(doc, int) and not isinstance(doc, bool))
                 or (tt == "number" and isinstance(doc, (int, float)) and not isinstance(doc, bool)) or (tt == "string" and isinstance(doc, str))
                 or (tt == "array" and isinstance(doc, list)) or (tt == "object" and isinstance(doc, dict)) for tt in types)
        if not ok:
            return path + " type"
    if isinstance(doc, (int, float)) and not isinstance(doc, bool):
        if "minimum" in schema and doc < schema["minimum"]: return path + " minimum"
        if "maximum" in schema and doc > schema["maximum"]: return path + " maximum"
    if isinstance(doc, str):
        if "minLength" in schema and len(doc) < schema["minLength"]: return path + " minLength"
        if "maxLength" in schema and len(doc) > schema["maxLength"]: return path + " maxLength"
        if "pattern" in schema and re.match(schema["pattern"], doc) is None: return path + " pattern"
    if isinstance(doc, list):
        if "minItems" in schema and len(doc) < schema["minItems"]: return path + " minItems"
        if "maxItems" in schema and len(doc) > schema["maxItems"]: return path + " maxItems"
        if "items" in schema:
            for i, v in enumerate(doc):
                r = validate(schema["items"], v, "%s[%d]" % (path, i))
                if r: return r
    if isinstance(doc, dict):
        for k in schema.get("required", []):
            if k not in doc: return path + " required:" + k
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for k in doc:
                if k not in props: return path + " additional:" + k
        for k, v in doc.items():
            if k in props:
                r = validate(props[k], v, path + "." + k)
                if r: return r
    return None


# ---------------------------------------------------------------- the distribution gate, exact integer arithmetic (README section "The distribution gate")
def critical_thousandths(df, table):
    rows = sorted(table, key=lambda r: r["df"])
    if df > 120:
        return next(r["thousandths"] for r in rows if r["df"] == 120)
    below = [r for r in rows if r["df"] <= df]
    return below[-1]["thousandths"]


def gate(baseline, candidate, tolerance_ppm, table):
    for rec, side in ((baseline, "baseline"), (candidate, "candidate")):
        if len(rec["runs"]) < rec["repetitionsDeclared"]:
            return {"decision": "UNRESOLVED", "unresolvedReason": "INCOMPLETE", "statistics": None}
        if rec["configuration"]["harness"]["dirty"]:
            return {"decision": "UNRESOLVED", "unresolvedReason": "DIRTY_TREE", "statistics": None}
    tasks = sorted({r["taskId"] for run in baseline["runs"] for r in run["results"]})
    n = len(tasks)
    if n < 2:
        return {"decision": "UNRESOLVED", "unresolvedReason": "TOO_FEW_TASKS", "statistics": None}
    kb, kc = len(baseline["runs"]), len(candidate["runs"])
    sum_b = {t: 0 for t in tasks}; sum_c = {t: 0 for t in tasks}
    for run in baseline["runs"]:
        for r in run["results"]: sum_b[r["taskId"]] += r["score"]
    for run in candidate["runs"]:
        for r in run["results"]: sum_c[r["taskId"]] += r["score"]
    D = [kb * sum_c[t] - kc * sum_b[t] for t in tasks]
    T = sum(D); Q = n * sum(d * d for d in D) - T * T
    tol = tolerance_ppm * kb * kc; L = T - n * tol; U = T + n * tol
    c = critical_thousandths(n - 1, table)
    cQ = c * c * Q
    improved = L > 0 and L * L * (n - 1) * 10**6 > cQ
    regressed = U < 0 and U * U * (n - 1) * 10**6 > cQ
    non_inferior = U > 0 and U * U * (n - 1) * 10**6 > cQ
    decision = "IMPROVED" if improved else ("REGRESSED" if regressed else "WITHIN_NOISE")
    denom = n * kb * kc
    mean_ppm = T // denom  # floor
    # halfWidthPpm = ceil( c * sqrt(Q) / (1000 * n * sqrt(n-1) * kb * kc) ): the smallest h with h^2 * (1000 n kb kc)^2 (n-1) >= c^2 Q
    d2 = (1000 * denom) ** 2 * (n - 1)
    h = math.isqrt((cQ + d2 - 1) // d2) if cQ > 0 else 0
    while h * h * d2 < cQ: h += 1
    while h > 0 and (h - 1) * (h - 1) * d2 >= cQ: h -= 1
    return {"decision": decision, "unresolvedReason": None,
            "statistics": {"tasks": n, "baselineRuns": kb, "candidateRuns": kc, "criticalThousandths": c, "meanDifferencePpm": mean_ppm, "halfWidthPpm": h, "nonInferior": non_inferior}}


# ---------------------------------------------------------------- part A: the contract's own vectors
def check_vectors(contract):
    v = json.loads((contract / "vectors.json").read_bytes())
    schemas = {k: json.loads((contract / (n + ".schema.json")).read_bytes()) for k, n in SCHEMA_IDS.items()}
    records = v["stores"]["records"]
    out = {"shape": [], "valid": [], "comparisons": [], "mismatchFlagged": []}
    for case in v["cases"]:
        s = schemas[case["kind"]]; r = validate(s, case["document"])
        if case["expect"] == "SHAPE":
            out["shape"].append({"id": case["id"], "refused": r is not None, "where": r})
        elif case["expect"] is None:
            out["valid"].append({"id": case["id"], "accepted": r is None, "where": r})
        if case["kind"] == "comparison" and case["expect"] in (None, "DECISION_MISMATCH"):
            doc = case["document"]; b = records.get(doc["baselineDigest"]); c = records.get(doc["candidateDigest"])
            if b is None or c is None or doc["decision"] == "UNRESOLVED" and doc.get("unresolvedReason") is None:
                continue
            g = gate(b, c, doc["tolerance"]["ppm"], v["criticalValues"])
            same = g["decision"] == doc["decision"] and g["statistics"] == doc["statistics"] and g["unresolvedReason"] == doc.get("unresolvedReason")
            (out["comparisons"] if case["expect"] is None else out["mismatchFlagged"]).append({"id": case["id"], "agrees": same, "labDecision": g["decision"], "documentDecision": doc["decision"]})
    out["counts"] = {"shapeCases": len(out["shape"]), "shapeRefused": sum(1 for x in out["shape"] if x["refused"]),
                     "validCases": len(out["valid"]), "validAccepted": sum(1 for x in out["valid"] if x["accepted"]),
                     "comparisonCases": len(out["comparisons"]), "comparisonAgree": sum(1 for x in out["comparisons"] if x["agrees"]),
                     "mismatchCases": len(out["mismatchFlagged"]), "mismatchFlagged": sum(1 for x in out["mismatchFlagged"] if not x["agrees"])}
    return out, v["criticalValues"], schemas


# ---------------------------------------------------------------- part B and C: the arms study as records
def build(export, contract, commit, table, schemas):
    sys.path.insert(0, str(export))
    ledger = importlib.import_module("_ledger")
    config, classes_sha = ledger.load_config()
    committed = json.loads((export / "results.json").read_bytes())
    by_id = {c["id"]: c for c in config["classes"]}
    arm_classes = config["arms"]["classes"]; policies = [None] + [p["id"] for p in config["arms"]["policies"]]
    held = [c["id"] for c in config["classes"] if c["id"] not in arm_classes]
    seeds = config["seeds"]
    digest_of = lambda name: sha((export / name).read_bytes())
    suite = sha(("CONF-MAS arms study: " + classes_sha).encode())
    scope = sha(("scope: conformance-labs tests/mas at " + commit).encode())
    task_digest = lambda cid: sha(canon(by_id[cid]))
    split = {"schemaVersion": "planeon.internal.split-declaration/v1", "splitId": "conf-mas-arms-split", "suiteDigest": suite, "declaredAt": "2026-11-05T00:00:00Z",
             "partitions": {"DEVELOPMENT": [{"taskId": c, "taskDigest": task_digest(c)} for c in arm_classes], "HELD_OUT": [{"taskId": c, "taskDigest": task_digest(c)} for c in held]}}
    split_digest = sha(canon(split))
    locks = {"specsDigest": digest_of("_sim.py"), "promptDigests": [sha(canon(config["instructions"]))], "toolSchemaDigests": [sha(canon(config["manifest"]))],
             "imageDigests": [sha(("CPython " + sys.version.split()[0]).encode())], "dependencyLockDigests": [sha(b"standard library only")],
             "fixtureDigest": sha(canon(config["topologies"])), "datasetDigest": "sha256:" + classes_sha, "evaluator": {"id": "_classes.measure", "version": commit[:8], "digest": digest_of("_classes.py")},
             "environmentDigest": sha(("macOS; CPython " + sys.version.split()[0] + "; stdlib").encode())}
    out = {"classesSha256": classes_sha, "committedClassesSha256": committed["classesSha256"], "classesShaMatch": classes_sha == committed["classesSha256"],
           "policies": policies, "classes": arm_classes, "heldOut": held, "seeds": len(seeds), "manifests": 0, "manifestRefused": [], "records": [], "comparisons": [], "splitValid": validate(schemas["split"], split) is None}
    ratios = {}  # (policy, class, seed) -> counts
    manifest_digest = {}
    for pol in policies:
        for cid in arm_classes:
            cls = by_id[cid]
            workers = config["topologies"][cls["topology"]]["workers"] if cls["topology"] in config["topologies"] else 1
            for i, seed in enumerate(seeds, 1):
                rows, measured = ledger.run(config, cls, seed, arm=pol)
                ratios[(pol, cid, seed)] = {m: measured["counts"][m] for m, _ in METRICS}
                run_id = "%s-%s-s%d" % (pol or "DEFENDED", cid, seed)
                man = {"schemaVersion": "planeon.internal.run-manifest/v1", "runId": run_id, "scopeDigest": scope, "suiteDigest": suite,
                       "configuration": {"model": {"id": (pol or "DEFENDED") + "@" + cid, "configurationDigest": sha(canon({"policy": pol, "class": cid}))},
                                         "harness": {"commit": commit, "dirty": False}, "budget": {"tokensPerTask": 0, "costMicrosPerTask": 0, "wallClockSecondsPerTask": cls["deadline"]}, "agentCount": int(workers) if isinstance(workers, int) else len(workers)},
                       "locks": locks, "seed": {"mode": "FIXED", "value": seed}, "execution": {"cacheKeyDigest": sha(run_id.encode()), "parallelism": 1},
                       "split": {"declarationDigest": split_digest, "partition": "DEVELOPMENT"}, "repetition": i, "writtenAt": WRITTEN, "startedAt": STARTED, "ledgerDigest": None}
                r = validate(schemas["manifest"], man); out["manifests"] += 1
                if r: out["manifestRefused"].append({"runId": run_id, "where": r})
                manifest_digest[(pol, cid, seed)] = sha(canon(man))
    # one evaluation record per (policy, metric): tasks = the arm classes; repetition = seed index. One configuration per policy
    # (the model id names the policy; the per-class model id above is reduced to the policy for the record's configuration).
    rec_docs = {}
    for pol in policies:
        for metric, sign in METRICS:
            runs = []
            for i, seed in enumerate(seeds, 1):
                results = []
                for cid in arm_classes:
                    v = ratios[(pol, cid, seed)][metric]; score = v if sign > 0 else 1000000 - v
                    results.append({"taskId": cid, "score": int(score), "tokensTotal": 0, "cacheReadTokens": 0, "costMicros": 0})
                runs.append({"manifestDigest": manifest_digest[(pol, arm_classes[0], seed)], "repetition": i, "results": results})
            rec = {"schemaVersion": "planeon.internal.evaluation-record/v1", "recordId": "%s-%s" % (pol or "DEFENDED", metric), "scopeDigest": scope, "suiteDigest": suite,
                   "configuration": {"model": {"id": pol or "DEFENDED", "configurationDigest": sha(canon({"policy": pol}))}, "harness": {"commit": commit, "dirty": False},
                                     "budget": {"tokensPerTask": 0, "costMicrosPerTask": 0, "wallClockSecondsPerTask": max(by_id[c]["deadline"] for c in arm_classes)}, "agentCount": 1},
                   "split": {"declarationDigest": split_digest, "partition": "DEVELOPMENT"}, "repetitionsDeclared": len(seeds), "runs": runs}
            r = validate(schemas["record"], rec); rec_docs[(pol, metric)] = rec
            out["records"].append({"recordId": rec["recordId"], "valid": r is None, "where": r, "digest": sha(canon(rec))[:23]})
    # comparisons: each arm against DEFENDED, per metric, NON_REGRESSION at the tolerance
    arms_rows = {(a["arm"], a["class"]): a for a in committed["arms"]["results"]}
    for pol in policies[1:]:
        for metric, _ in METRICS:
            g = gate(rec_docs[(None, metric)], rec_docs[(pol, metric)], TOLERANCE["ppm"], table)
            comp = {"schemaVersion": "planeon.internal.distribution-gate/v1", "comparisonId": "%s-vs-DEFENDED-%s" % (pol, metric), "purpose": "NON_REGRESSION",
                    "baselineDigest": sha(canon(rec_docs[(None, metric)])), "candidateDigest": sha(canon(rec_docs[(pol, metric)])), "tolerance": dict(TOLERANCE),
                    "decision": g["decision"], "unresolvedReason": g["unresolvedReason"], "statistics": g["statistics"]}
            r = validate(schemas["comparison"], comp)
            campaign_holds = all(arms_rows[(pol, cid)]["wouldHoldBounds"][metric] for cid in arm_classes)
            gate_pass = g["decision"] != "UNRESOLVED" and g["statistics"]["nonInferior"]
            out["comparisons"].append({"arm": pol, "metric": metric, "valid": r is None, "where": r, "decision": g["decision"], "statistics": g["statistics"],
                                       "campaignBoundsHoldAllClasses": campaign_holds, "campaignPerClass": {cid: arms_rows[(pol, cid)]["wouldHoldBounds"][metric] for cid in arm_classes},
                                       "gateNonInferior": gate_pass, "agrees": campaign_holds == gate_pass})
    out["counts"] = {"manifests": out["manifests"], "manifestsValid": out["manifests"] - len(out["manifestRefused"]), "records": len(out["records"]), "recordsValid": sum(1 for r in out["records"] if r["valid"]),
                     "comparisons": len(out["comparisons"]), "comparisonsValid": sum(1 for c in out["comparisons"] if c["valid"]), "comparisonsUnresolved": sum(1 for c in out["comparisons"] if c["decision"] == "UNRESOLVED"),
                     "agree": sum(1 for c in out["comparisons"] if c["agrees"]), "splitValid": out["splitValid"]}
    return out


def main(export, contract, commit, out_path):
    export, contract = Path(export).resolve(), Path(contract).resolve()
    vectors, table, schemas = check_vectors(contract)
    arms = build(export, contract, commit, table, schemas)
    rec = {"contractDigests": {n: sha((contract / n).read_bytes()) for n in ("README.md", "vectors.json", "run-manifest.schema.json", "evaluation-record.schema.json", "distribution-gate.schema.json", "split-declaration.schema.json", "selection-record.schema.json")},
           "vectors": vectors, "arms": arms}
    json.dump(rec, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("vectors", json.dumps(vectors["counts"]), "| arms", json.dumps(arms["counts"]))


if __name__ == "__main__":
    main(*sys.argv[1:5])
