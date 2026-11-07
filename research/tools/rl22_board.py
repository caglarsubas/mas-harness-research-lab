"""RL-22 (H-23, coordinator half): a clean-room board state machine written from MAS-RA-004's README section A2 alone,
run on the record's transcript and binding vectors. Mismatches are the measurement (what the README underspecifies).
VERIFY's ledger binding and history rules (MAS-RA-001's model) are not modelled: an ACCEPTED VERIFY appends the stored
ledger's status for the scope's subjectDigest; a refused VERIFY is taken as recorded. usage:
python3 -I -B rl22_board.py CONTRACT_DIR RL18_TOOL RL20_TOOL OUT.json   (stdlib; deterministic; counts and ids only)"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def sha(doc):
    return "sha256:" + hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


class Board:
    def __init__(self, topo, items, stores):
        self.topo, self.stores = topo, stores
        self.roles = {n["nodeId"]: n["role"] for n in topo["nodes"]}
        self.delegates = {(e["from"], e["to"]) for e in topo["edges"] if e["kind"] == "DELEGATE"}
        self.msg_edges = {(e["from"], e["to"]) for e in topo["edges"] if e["kind"] == "MESSAGE"}
        self.rec = {i: {"state": "OPEN", "holder": None, "leaseUntil": None, "version": 0, "claimOp": None, "verdicts": []} for i in items}
        self.answered = {}

    def expire(self, t):
        for r in self.rec.values():
            if r["state"] == "HELD" and r["leaseUntil"] is not None and r["leaseUntil"] <= t:
                r.update(state="OPEN", holder=None, leaseUntil=None, claimOp=None, verdicts=[]); r["version"] += 1

    def held_by(self, agent):
        return sum(1 for r in self.rec.values() if r["state"] == "HELD" and r["holder"] == agent)

    def apply(self, op):
        t = op["t"]; self.expire(t)
        body = {k: v for k, v in op.items() if k not in ("result", "retryOf")}
        if op.get("retryOf") is not None:
            orig = self.answered.get(op["retryOf"])
            return orig["answer"] if orig else "RETRY_MISMATCH"
        if t > self.topo["deadlineSeconds"]:
            return self.finish(op, "DEADLINE")
        kind = op["op"]; mode = self.topo["mode"]; agent = op["agent"]; role = self.roles.get(agent)
        r = self.rec.get(op.get("item"))
        if kind in ("ACQUIRE", "ASSIGN"):
            holder = op.get("worker", agent) if kind == "ASSIGN" else agent
            if kind == "ACQUIRE" and not (role == "WORKER" and mode == "DECENTRALIZED"): return self.finish(op, "NOT_PERMITTED")
            if kind == "ASSIGN" and not (role == "COORDINATOR" and mode == "CENTRAL" and self.roles.get(holder) == "WORKER" and (agent, holder) in self.delegates): return self.finish(op, "NOT_PERMITTED")
            if r["state"] != "OPEN": return self.finish(op, r["state"])
            if op.get("expectedVersion") != r["version"]: return self.finish(op, "STALE_VERSION")
            if self.held_by(holder) >= self.topo["concurrency"]: return self.finish(op, "CONCURRENCY_LIMIT")
            r.update(state="HELD", holder=holder, leaseUntil=t + self.topo["leaseSeconds"], claimOp=op["opId"], verdicts=[]); r["version"] += 1
            return self.finish(op, "ACCEPTED")
        if kind in ("RENEW", "RELEASE", "MERGE"):
            allowed = r["state"] == "HELD" and (r["holder"] == agent or (kind == "RELEASE" and role == "COORDINATOR" and mode == "CENTRAL"))
            if not allowed: return self.finish(op, "NOT_HOLDER")
            if op.get("expectedVersion") != r["version"]: return self.finish(op, "STALE_VERSION")
            if kind == "RENEW": r["leaseUntil"] = t + self.topo["leaseSeconds"]; r["version"] += 1; return self.finish(op, "ACCEPTED")
            if kind == "RELEASE": r.update(state="OPEN", holder=None, leaseUntil=None, claimOp=None, verdicts=[]); r["version"] += 1; return self.finish(op, "ACCEPTED")
            if not r["verdicts"]: return self.finish(op, "NO_VERDICT")
            on_work = [s for w, s in r["verdicts"] if w == op.get("workDigest")]
            if not on_work: return self.finish(op, "WORK_MISMATCH")
            if on_work[-1] != "PASS": return self.finish(op, "VERDICT_NOT_PASS")
            r.update(state="MERGED", holder=None, leaseUntil=None); r["version"] += 1; return self.finish(op, "ACCEPTED")
        if kind == "VERIFY":
            if r["state"] != "HELD": return self.finish(op, "NOT_HELD")
            if r["holder"] == agent: return self.finish(op, "SELF_VERIFICATION")
            # binding and history are MAS-RA-001's model (not modelled): the recorded answer is taken; an ACCEPTED one appends the ledger's status
            ans = op["result"]
            if ans == "ACCEPTED":
                led = self.stores["ledgers"].get(op.get("verdict", {}).get("ledgerDigest"), {}); status = led.get("verdict", {}).get("status")
                r["verdicts"].append((op.get("verdict", {}).get("scope", {}).get("subjectDigest"), status))
            self.answered[op["opId"]] = {"answer": ans, "body": body}; return ans
        if kind == "MESSAGE":
            return self.finish(op, "ACCEPTED" if (agent, op.get("to")) in self.msg_edges else "OFF_EDGE")
        return self.finish(op, "NOT_PERMITTED")

    def finish(self, op, ans):
        self.answered[op["opId"]] = {"answer": ans, "body": {k: v for k, v in op.items() if k not in ("result", "retryOf")}}; return ans


def check_transcript(doc, stores, validate, schemas, rl20, thr):
    if validate(schemas["transcript"], doc): return "SHAPE", {}
    ops = doc["operations"]; ids = [o["opId"] for o in ops]
    if len(set(ids)) != len(ids) or len(set(doc["items"])) != len(doc["items"]): return "DUPLICATE_ID", {}
    topo = stores["topologies"].get(doc["topologyDigest"])
    if topo is None or sha(topo) != doc["topologyDigest"] or rl20.run_check(topo, stores, validate, schemas, thr)[0] is not None: return "UNKNOWN_REFERENCE", {}
    nodes = {n["nodeId"] for n in topo["nodes"]}
    for o in ops:
        if o["agent"] not in nodes or (o.get("worker") is not None and o["worker"] not in nodes) or (o.get("to") is not None and o["to"] not in nodes): return "UNKNOWN_REFERENCE", {}
        if o.get("item") is not None and o["item"] not in doc["items"]: return "UNKNOWN_REFERENCE", {}
        if o.get("retryOf") is not None and o["retryOf"] not in ids: return "UNKNOWN_REFERENCE", {}
        if o["op"] == "VERIFY":
            led = stores["ledgers"].get(o.get("verdict", {}).get("ledgerDigest"))
            if led is None or sha(led) != o["verdict"]["ledgerDigest"]: return "UNKNOWN_REFERENCE", {}
    if topo["mode"] == "SINGLE_AGENT" or doc["transcriptId"] in nodes: return "MODE", {}
    by_id = {o["opId"]: o for o in ops}
    order = sorted(ops, key=lambda o: (o["t"], o["agent"], o["opId"]))
    pos = {o["opId"]: i for i, o in enumerate(order)}
    for o in ops:
        if o.get("retryOf") is not None:
            orig = by_id[o["retryOf"]]
            if orig.get("retryOf") is not None or pos[orig["opId"]] > pos[o["opId"]]: return "RETRY", {}
            if {k: v for k, v in orig.items() if k not in ("opId", "t", "result", "retryOf")} != {k: v for k, v in o.items() if k not in ("opId", "t", "result", "retryOf")}: return "RETRY", {}
    board = Board(topo, doc["items"], stores); answers = {}
    for o in order:
        answers[o["opId"]] = board.apply(o)
    mism = {k: (answers[k], by_id[k]["result"]) for k in answers if answers[k] != by_id[k]["result"]}
    return ("REPLAY" if mism else None), mism


def main(contract, rl18_path, rl20_path, out_path):
    contract = Path(contract); rl18 = load(rl18_path, "rl18"); rl20 = load(rl20_path, "rl20"); validate = rl18.validate
    tc = contract / "topology-coordination"; rm = contract / "run-manifest"
    schemas = {"transcript": json.loads((tc / "board-transcript.schema.json").read_bytes()), "binding": json.loads((tc / "topology-run-binding.schema.json").read_bytes()),
               "topology": json.loads((tc / "topology-spec.schema.json").read_bytes()), "record": json.loads((rm / "evaluation-record.schema.json").read_bytes()),
               "manifest": json.loads((rm / "run-manifest.schema.json").read_bytes()), "split": json.loads((rm / "split-declaration.schema.json").read_bytes())}
    v = json.loads((tc / "vectors.json").read_bytes()); stores = v["stores"]; thr = tuple(v["selectionThreshold"])
    rows = []
    for c in v["cases"]:
        if c["kind"] == "transcript":
            code, mism = check_transcript(c["document"], stores, validate, schemas, rl20, thr)
            rows.append({"id": c["id"], "kind": "transcript", "expect": c["expect"], "lab": code, "agrees": code == c["expect"], "mismatchedAnswers": len(mism), "firstMismatch": next(iter(mism.items()), None)})
        elif c["kind"] == "binding":
            d = c["document"]; code = None
            if validate(schemas["binding"], d): code = "SHAPE"
            else:
                topo = stores["topologies"].get(d["topologyDigest"]); man = stores["manifests"].get(d["manifestDigest"])
                if topo is None or man is None or sha(topo) != d["topologyDigest"] or sha(man) != d["manifestDigest"] or rl20.run_check(topo, stores, validate, schemas, thr)[0] is not None or validate(schemas["manifest"], man): code = "UNKNOWN_REFERENCE"
                else:
                    vec = sum(1 for n in topo["nodes"]); code = None if man["configuration"]["agentCount"] == vec else "BINDING"
            rows.append({"id": c["id"], "kind": "binding", "expect": c["expect"], "lab": code, "agrees": code == c["expect"], "mismatchedAnswers": 0, "firstMismatch": None})
    out = {"cases": rows, "counts": {"transcript": sum(1 for r in rows if r["kind"] == "transcript"), "transcriptAgree": sum(1 for r in rows if r["kind"] == "transcript" and r["agrees"]),
                                     "binding": sum(1 for r in rows if r["kind"] == "binding"), "bindingAgree": sum(1 for r in rows if r["kind"] == "binding" and r["agrees"])},
           "disagreements": [(r["id"], r["expect"], r["lab"], r["firstMismatch"]) for r in rows if not r["agrees"]]}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(out["counts"])); print("disagreements:", out["disagreements"][:12])


if __name__ == "__main__":
    main(*sys.argv[1:5])
