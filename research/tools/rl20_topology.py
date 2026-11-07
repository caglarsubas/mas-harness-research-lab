"""RL-20 (H-25, TopologySpec half): the lab's static checker over MAS-RA-004's TopologySpec, written from the record's
README, checked against the record's topology vectors, then run on seeded graph mutations of the valid vectors.
usage: python3 -I -B rl20_topology.py CONTRACT_DIR RL18_TOOL_PATH OUT.json   (stdlib; deterministic; counts and ids only)"""
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

ROLES = ("COORDINATOR", "WORKER", "VERIFIER")


def sha(doc) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


class Refusal(Exception):
    def __init__(self, code, witness=""):
        super().__init__(code); self.code, self.witness = code, witness


def record_ok(rec, stores, validate, schemas):
    """MAS-RA-002's record check, the subset the topology vectors exercise: SHAPE, DUPLICATE_ID, UNKNOWN_REFERENCE,
    then the per-run rules; returns the first code or None."""
    if validate(schemas["record"], rec): return "SHAPE"
    runs = rec["runs"]
    if len({r["manifestDigest"] for r in runs}) != len(runs) or len({r["repetition"] for r in runs}) != len(runs): return "DUPLICATE_ID"
    for r in runs:
        ids = [x["taskId"] for x in r["results"]]
        if len(set(ids)) != len(ids): return "DUPLICATE_ID"
    split = stores["splits"].get(rec["split"]["declarationDigest"])
    if split is None: return "UNKNOWN_REFERENCE"
    mans = []
    for r in runs:
        m = stores["manifests"].get(r["manifestDigest"])
        if m is None: return "UNKNOWN_REFERENCE"
        mans.append(m)
    if validate(schemas["split"], split): return "SHAPE"
    locks, seedmode = None, None
    for m in mans:
        if validate(schemas["manifest"], m): return "SHAPE"
        same = (m["configuration"] == rec["configuration"] and m["scopeDigest"] == rec["scopeDigest"] and m["suiteDigest"] == rec["suiteDigest"] and m["split"] == rec["split"])
        if not same: return "CONFIGURATION_MIXED"
        if locks is None: locks, seedmode = m["locks"], m["seed"]["mode"]
        elif m["locks"] != locks or m["seed"]["mode"] != seedmode: return "CONFIGURATION_MIXED"
    if len({m["execution"]["cacheKeyDigest"] for m in mans}) != len(mans): return "DUPLICATE_ID"
    k = rec["repetitionsDeclared"]
    if any(not 1 <= r["repetition"] <= k for r in runs) or any(m["repetition"] != r["repetition"] for m, r in zip(mans, runs)): return "REPETITIONS"
    fixed = [m["seed"]["value"] for m in mans if m["seed"]["mode"] == "FIXED"]
    if len(set(fixed)) != len(fixed): return "SEED_REUSED"
    tasks = {t["taskId"] for t in split["partitions"][rec["split"]["partition"]]}
    for r in runs:
        if {x["taskId"] for x in r["results"]} != tasks: return "TASK_SET"
        if any(x["cacheReadTokens"] > x["tokensTotal"] for x in r["results"]): return "CACHE_EXCEEDS_TOKENS"
    return None


def baseline_eligible(rec, stores, validate, schemas):
    """A3's eligibility: complete, agentCount 1, clean tree, DEVELOPMENT, and no task held out by any valid declaration."""
    if len(rec["runs"]) < rec["repetitionsDeclared"] or rec["configuration"]["agentCount"] != 1 or rec["configuration"]["harness"]["dirty"] or rec["split"]["partition"] != "DEVELOPMENT":
        return False
    split = stores["splits"][rec["split"]["declarationDigest"]]
    scored = {t["taskId"] for r in rec["runs"] for t in r["results"]}
    digests = {t["taskId"]: t["taskDigest"] for t in split["partitions"]["DEVELOPMENT"]}
    for d, s in stores["splits"].items():
        if validate(schemas["split"], s) or sha(s) != d: continue
        for t in s["partitions"]["HELD_OUT"]:
            if (s["suiteDigest"] == split["suiteDigest"] and t["taskId"] in scored) or t["taskDigest"] in {digests.get(x) for x in scored}:
                return False
    return True


def check_topology(doc, stores, validate, schemas, threshold):
    if validate(schemas["topology"], doc): raise Refusal("SHAPE")
    nodes = [n["nodeId"] for n in doc["nodes"]]; roles = [a["role"] for a in doc["agents"]]
    edges = [(e["from"], e["to"], e["kind"]) for e in doc["edges"]]
    if len(set(nodes)) != len(nodes): raise Refusal("DUPLICATE_ID", "node")
    if len(set(roles)) != len(roles): raise Refusal("DUPLICATE_ID", "role")
    if len(set(edges)) != len(edges): raise Refusal("DUPLICATE_ID", "edge")
    node_roles = {n["nodeId"]: n["role"] for n in doc["nodes"]}
    if any(r not in roles for r in node_roles.values()) or any(r not in node_roles.values() for r in roles):
        raise Refusal("UNKNOWN_REFERENCE", "role")
    for f, t, _ in edges:
        if f not in node_roles or t not in node_roles: raise Refusal("UNKNOWN_REFERENCE", "edge %s->%s" % (f, t))
    bd = doc["selection"]["baselineRecordDigest"]; base = stores["records"].get(bd)
    if base is None or sha(base) != bd or record_ok(base, stores, validate, schemas): raise Refusal("UNKNOWN_REFERENCE", "baseline")
    if any(a["objectiveId"] != doc["objectiveId"] for a in doc["agents"]): raise Refusal("CONFLICTING_OBJECTIVE")
    vec = [sum(1 for r in node_roles.values() if r == R) for R in ROLES]
    mode, ap = doc["mode"], doc["assignmentPolicy"]
    coord = [n for n, r in node_roles.items() if r == "COORDINATOR"]
    if any(f == t for f, t, _ in edges): raise Refusal("MODE_STRUCTURE", "self-edge")
    depth = {a["role"]: a["budgets"]["recursionDepth"] for a in doc["agents"]}
    if any((r == "COORDINATOR") != (d == 1) for r, d in depth.items()): raise Refusal("MODE_STRUCTURE", "recursion depth")
    if mode == "SINGLE_AGENT":
        if not (vec == [0, 1, 0] and not edges and doc["concurrency"] == 1 and ap == "NONE"): raise Refusal("MODE_STRUCTURE", "single agent")
    elif mode == "CENTRAL":
        if not (vec[0] == 1 and vec[1] >= 1 and ap == "COORDINATOR_ASSIGNS"): raise Refusal("MODE_STRUCTURE", "central counts")
        c = coord[0]; want = {(c, n, "DELEGATE") for n in nodes if n != c}
        if {e for e in edges if e[2] == "DELEGATE"} != want: raise Refusal("MODE_STRUCTURE", "delegate edges")
    else:
        if not (vec[0] == 0 and vec[1] >= 2 and ap == "CLAIM_FROM_BOARD" and not any(k == "DELEGATE" for _, _, k in edges)): raise Refusal("MODE_STRUCTURE", "board")
    if sum(vec) > doc["agentBudget"] or doc["concurrency"] > vec[1]: raise Refusal("BUDGET", "vector %s budget %d concurrency %d" % (vec, doc["agentBudget"], doc["concurrency"]))
    sel = doc["selection"]
    if not baseline_eligible(base, stores, validate, schemas): raise Refusal("SELECTION", "baseline ineligible")
    total = sum(t["score"] for r in base["runs"] for t in r["results"]); n_tasks = len(base["runs"][0]["results"]) if base["runs"] else 0
    score = Fraction(total, n_tasks * len(base["runs"]) * 1000000) if n_tasks else Fraction(0)
    restricted = sel["taskShape"] in ("SEQUENTIAL", "TOOL_HEAVY") or score >= Fraction(*threshold)
    allowed = {"SINGLE_AGENT", "ORCHESTRATOR_WORKER"} | (set() if restricted else {"SELF_ORGANIZING"})
    out = sel["outcome"]
    if out not in allowed: raise Refusal("SELECTION", "outcome not allowed")
    if (out == "SINGLE_AGENT") != (mode == "SINGLE_AGENT") or (out == "ORCHESTRATOR_WORKER") != (mode == "CENTRAL" and vec[1] <= 4) or (out == "SELF_ORGANIZING") != (mode == "DECENTRALIZED"):
        raise Refusal("SELECTION", "outcome vs mode")
    return vec


def run_check(doc, stores, validate, schemas, threshold):
    try:
        check_topology(doc, stores, validate, schemas, threshold); return None, ""
    except Refusal as r:
        return r.code, r.witness


def mutations(doc):
    """H-25's graph classes the TopologySpec can express, as one edit each; expected refusal codes of the record."""
    out = []
    nodes = [n["nodeId"] for n in doc["nodes"]]; mode = doc["mode"]
    # cycle: a DELEGATE back-edge from a non-coordinator to the coordinator or to the first node
    d = json.loads(json.dumps(doc)); src = next((n["nodeId"] for n in doc["nodes"] if n["role"] != "COORDINATOR"), nodes[-1]); dst = nodes[0] if nodes[0] != src else nodes[-1]
    d["edges"].append({"from": src, "to": dst, "kind": "DELEGATE"}); out.append(("cycle", d, "MODE_STRUCTURE", "%s->%s" % (src, dst)))
    # unreachable: an added node with no edge (CENTRAL and SINGLE_AGENT: the record's rule; DECENTRALIZED: descriptive)
    d = json.loads(json.dumps(doc)); role = "WORKER"; d["nodes"].append({"nodeId": "rl20-isolated", "role": role}); d["agentBudget"] = max(d["agentBudget"], len(d["nodes"]) + 1)
    out.append(("unreachable", d, None if mode == "DECENTRALIZED" else "MODE_STRUCTURE", "rl20-isolated"))
    # budget escape: the agent budget below the vector's sum
    d = json.loads(json.dumps(doc)); d["agentBudget"] = max(1, len(d["nodes"]) - 1); out.append(("budget", d, "BUDGET", "agentBudget %d < nodes %d" % (d["agentBudget"], len(d["nodes"]))))
    return out


def main(contract, rl18_path, out_path):
    contract = Path(contract)
    spec = importlib.util.spec_from_file_location("rl18", rl18_path); rl18 = importlib.util.module_from_spec(spec); spec.loader.exec_module(rl18)
    validate = rl18.validate
    rm = contract / "run-manifest"; tc = contract / "topology-coordination"
    schemas = {"topology": json.loads((tc / "topology-spec.schema.json").read_bytes()), "record": json.loads((rm / "evaluation-record.schema.json").read_bytes()),
               "manifest": json.loads((rm / "run-manifest.schema.json").read_bytes()), "split": json.loads((rm / "split-declaration.schema.json").read_bytes())}
    v = json.loads((tc / "vectors.json").read_bytes()); stores = v["stores"]; thr = tuple(v["selectionThreshold"])
    agree = []
    for c in v["cases"]:
        if c["kind"] != "topology": continue
        code, w = run_check(c["document"], stores, validate, schemas, thr)
        agree.append({"id": c["id"], "expect": c["expect"], "lab": code, "agrees": code == c["expect"], "witness": w})
    valid = [c for c in v["cases"] if c["kind"] == "topology" and c["expect"] is None]
    muts, controls = [], []
    for c in valid:
        code, w = run_check(c["document"], stores, validate, schemas, thr); controls.append({"id": c["id"], "accepted": code is None})
        for klass, d, expected, seed_witness in mutations(c["document"]):
            code, w = run_check(d, stores, validate, schemas, thr)
            muts.append({"base": c["id"], "mode": c["document"]["mode"], "class": klass, "expected": expected, "lab": code, "witness": w, "seeded": seed_witness,
                         "gated": expected is not None, "refusedAsExpected": expected is not None and code == expected and bool(w)})
    gated = [m for m in muts if m["gated"]]
    rec = {"contractDigests": {"topology-coordination/" + n: rl18.sha((tc / n).read_bytes()) for n in ("README.md", "vectors.json", "topology-spec.schema.json")},
           "agreement": agree, "controls": controls, "mutations": muts,
           "counts": {"vectorCases": len(agree), "vectorAgree": sum(a["agrees"] for a in agree), "validAccepted": sum(c["accepted"] for c in controls), "valid": len(controls),
                      "gatedMutations": len(gated), "gatedRefusedAsExpected": sum(m["refusedAsExpected"] for m in gated), "gatedAccepted": sum(1 for m in gated if m["lab"] is None),
                      "descriptive": [{"base": m["base"], "class": m["class"], "lab": m["lab"]} for m in muts if not m["gated"]]}}
    json.dump(rec, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(rec["counts"])); print("disagreements:", [(a["id"], a["expect"], a["lab"]) for a in agree if not a["agrees"]][:10])


if __name__ == "__main__":
    main(*sys.argv[1:4])
