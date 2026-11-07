"""RL-21 (H-26, contract-text half): one writer per governed state, as the published authority records of
harness-onion express it: every path under architecture/ is created by exactly one packet authority (newFiles); every
change to such a path names its creator among the changer's baselinePackets; every path owned by more than one meta
authority is owned by a chain of meta authorities linked by metaBaseline. usage: python3 -I -B rl21_writers.py
EXPORT_ARCHITECTURE_DIR OUT.json   (stdlib; deterministic; counts and ids only; no file content)"""
import json
import pathlib
import sys


def paths_of(v):
    return list(v.keys()) if isinstance(v, dict) else [e["path"] if isinstance(e, dict) else e for e in v]


def main(arch, out_path):
    X = pathlib.Path(arch)
    files = sorted(X.glob("*-authority.json")) + sorted(X.glob("*/authority.json"))
    docs = [(f.name if f.parent == X else f.parent.name + "/" + f.name, json.loads(f.read_bytes())) for f in files]
    packet = [(n, d) for n, d in docs if "newFiles" in d]; meta = [(n, d) for n, d in docs if "ownedPaths" in d]
    other = [n for n, d in docs if "newFiles" not in d and "ownedPaths" not in d]
    # H-26a: one creator per created path
    creator, dup = {}, []
    for n, d in packet:
        for p in paths_of(d["newFiles"]):
            if p in creator: dup.append({"path": p, "creators": [creator[p], d["authorityPacket"]]})
            else: creator[p] = d["authorityPacket"]
    # H-26b: every change to a created path names the creator among the changer's baseline packets
    changed_total = changed_in_scope = linked = 0; unlinked = []; out_of_scope = 0
    for n, d in packet:
        base = set(d["baselinePackets"].keys()) if isinstance(d["baselinePackets"], dict) else set(d["baselinePackets"])
        for p in paths_of(d["changedFiles"]):
            changed_total += 1
            c = creator.get(p)
            if c is None: out_of_scope += 1; continue
            changed_in_scope += 1
            if c in base or c == d["authorityPacket"]: linked += 1
            else: unlinked.append({"path": p, "changer": d["authorityPacket"], "creator": c})
    # H-26c: multiply owned paths are owned by a metaBaseline-linked chain
    owners = {}
    for n, d in meta:
        for p in paths_of(d["ownedPaths"]): owners.setdefault(p, []).append(d["authorityPacket"])
    ref = {}
    for n, d in meta:
        mb = d.get("metaBaseline"); names = set()
        if isinstance(mb, dict): names |= set(mb.keys()) | {v for v in mb.values() if isinstance(v, str)}
        elif isinstance(mb, list): names |= {x if isinstance(x, str) else json.dumps(x) for x in mb}
        elif isinstance(mb, str): names.add(mb)
        ref[d["authorityPacket"]] = names
    multi = {p: o for p, o in owners.items() if len(o) > 1}; chained = 0; broken = []
    for p, o in multi.items():
        ids = set(o)
        # a chain: every owner but one names another owner (or its digest) in its metaBaseline
        roots = [i for i in o if not (ref.get(i, set()) & ids) and not any(any(x in s for s in ref.get(i, set())) for x in ids)]
        if len(roots) <= 1: chained += 1
        else: broken.append({"path": p, "ownersWithoutBaselineAmongOwners": roots[:4]})
    out = {"authorityFiles": len(docs), "packetAuthorities": len(packet), "metaAuthorities": len(meta), "otherAuthorities": other,
           "created": len(creator), "createdTwice": dup, "changedEntries": changed_total, "changedInScope": changed_in_scope, "changedLinked": linked, "changedUnlinked": unlinked[:20], "changedUnlinkedCount": len(unlinked), "changedOutOfScope": out_of_scope,
           "ownedPathsDistinct": len(owners), "ownedByMoreThanOne": len(multi), "chained": chained, "broken": broken[:20], "brokenCount": len(broken),
           "metaBaselineForm": type(meta[0][1].get("metaBaseline")).__name__ if meta else None}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items() if k not in ("changedUnlinked", "broken", "otherAuthorities")}))


if __name__ == "__main__":
    main(*sys.argv[1:3])
