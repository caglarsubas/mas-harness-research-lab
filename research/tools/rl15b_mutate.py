"""RL-15b (H-30 restated): seeded-inconsistency benchmark for the roadmap build on the lock-40 builder, scratch copy only.
usage: python3 -I -B rl15b_mutate.py BASE_DIR WORK_DIR OUT.json
Derived from RL-15's frozen tool (b35e6009) with the PREREG v1 changes of RL-15b: (1) WORK_DIR must be named
`roadmap` under its own parent (the lock-40 paper-file validator resolves paper paths from the repository root);
(2) the refusal message is captured up to 400 characters; (3) the benign update-entry control carries a UTC offset
(lock 40's date rule); (4) M6's third instance (a secondary paper's digest; no file in the bridge) is applied and
reported but declared uncatchable (catchable=false) and excluded from the denominator; (5) attribution reads the
whole refusal message: a refusal is attributed to a NEW rule when the message carries the lock-40 tag "(RL-15 v1)"
or "(RL-15 v2)", and to an OLDER rule (one of load()'s rules, which run first) when it matches that rule's wording
as fixed in the PREREG from run-001 and run-002 (disclosed); a refusal with neither is unattributed. Seed 20261105
keeps run-002's targets so the visionary's restated expectation (ERRATUM to RL15-D1) applies instance by instance.
No item text is copied into the output."""
import hashlib
import json
import re
import pathlib
import random
import shutil
import subprocess
import sys
import time

SEED = 20261105
CAPTURE = None  # whole message
TAGS = ("(RL-15 v1)", "(RL-15 v2)")
ENV = {"PATH": "/usr/bin:/bin"}  # TMPDIR is set per build to the work copy's parent
OLDER_RULES = [  # load()'s rules as worded in run-001 and run-002 (any class may be refused by any of them first)
    r"unknown dependency", r"is DONE but its evidenceState is", r"rating \S+ out of range", r"factor keys",
    r"harnesses needs", r"unknown codebase reference", r"duplicate item id", r"is BLOCKED with nothing blocking it",
]


def reset(base, work):
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(base, work, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def build(work):
    t0 = time.monotonic()
    r = subprocess.run([sys.executable, "-I", "-B", "build_roadmap.py"], cwd=str(work), capture_output=True, text=True, timeout=600, env=dict(ENV, TMPDIR=str(work.parent)))
    msg = (r.stderr.strip().splitlines() or [""])[-1] if r.returncode != 0 else ""
    refused = r.returncode != 0 and msg.startswith("roadmap.json:")
    crashed = r.returncode != 0 and not refused
    return {"exit": r.returncode, "refused": refused, "crashed": crashed, "message": msg, "messageLength": len(msg), "wall_s": round(time.monotonic() - t0, 2)}


QUALIFYING = {}


def pick(rng, items, pred, k, klass):
    pool = [i for i in items if pred(i)]
    QUALIFYING[klass] = QUALIFYING.get(klass, 0) + len(pool)
    if len(pool) < k:
        raise SystemExit("rl15b: class %s has %d qualifying targets, fewer than %d" % (klass, len(pool), k))
    return rng.sample(pool, k)


def item(d, iid):
    return next(i for i in d["items"] if i["id"] == iid)


def mutations(data, rng):
    items = data["items"]
    out = []  # (class, target, field, tokens, catchable, apply)
    for it in pick(rng, items, lambda i: isinstance(i.get("dependsOn"), list), 3, "M1"):
        out.append(("M1", it["id"], "dependsOn", ["dependsOn", "NO-SUCH-ITEM-999"], True, lambda d, iid=it["id"]: item(d, iid)["dependsOn"].append("NO-SUCH-ITEM-999")))
    for it in pick(rng, items, lambda i: i.get("status") == "DONE" and i.get("evidenceState") != "PLANNED", 3, "M2"):
        out.append(("M2", it["id"], "evidenceState", ["evidenceState", "PLANNED"], True, lambda d, iid=it["id"]: item(d, iid).__setitem__("evidenceState", "PLANNED")))
    picks = pick(rng, items, lambda i: isinstance(i.get("benefit"), dict) and "B2" in i["benefit"], 3, "M3")
    out.append(("M3", picks[0]["id"], "benefit", ["benefit", "B2"], True, lambda d, iid=picks[0]["id"]: item(d, iid)["benefit"]["B2"].__setitem__(0, 7)))
    out.append(("M3", picks[1]["id"], "benefit", ["benefit", "B2"], True, lambda d, iid=picks[1]["id"]: item(d, iid)["benefit"]["B2"].__setitem__(0, 0)))
    out.append(("M3", picks[2]["id"], "benefit", ["benefit", "B2"], True, lambda d, iid=picks[2]["id"]: item(d, iid)["benefit"].pop("B2")))
    for it in pick(rng, items, lambda i: i.get("status") in ("READY", "IN_PROGRESS") and i.get("evidenceState") in ("IMPLEMENTED", "CONTRACT_ADOPTED"), 3, "M4"):
        out.append(("M4", it["id"], "status", ["updates", "update"], True, lambda d, iid=it["id"]: item(d, iid).__setitem__("status", "DONE")))
    picks = pick(rng, items, lambda i: isinstance(i.get("harnesses"), dict) and i["harnesses"], 1, "M5")
    out.append(("M5", picks[0]["id"], "harnesses", ["harnesses", "H99"], True, lambda d, iid=picks[0]["id"]: item(d, iid)["harnesses"].__setitem__("H99", "NO-SUCH-HARNESS")))
    picks = pick(rng, items, lambda i: True, 1, "M5")
    out.append(("M5", picks[0]["id"], "codebases", ["codebases", "NO-SUCH-CODEBASE-999"], True, lambda d, iid=picks[0]["id"]: item(d, iid).__setitem__("codebases", ["NO-SUCH-CODEBASE-999"])))
    picks = pick(rng, items, lambda i: True, 1, "M5")
    out.append(("M5", picks[0]["id"], "id", ["duplicate", "duplicated", picks[0]["id"]], True, lambda d, iid=picks[0]["id"]: d["items"].append(dict(item(d, iid)))))
    res = data["research"]
    s = rng.choice([e for e in res["sources"] if re.fullmatch(r"[0-9a-f]{64}", e.get("sha256", ""))])
    QUALIFYING["M6"] = len(res["sources"]) + len(res["papers"]) + len(res["secondaryPapers"])
    out.append(("M6", s["id"], "sha256", ["sha256", s["id"], str(s.get("file", ""))], True, lambda d, sid=s["id"]: next(e for e in d["research"]["sources"] if e["id"] == sid).__setitem__("sha256", next(e for e in d["research"]["sources"] if e["id"] == sid)["sha256"][:63])))
    pp = rng.choice([e for e in res["papers"] if re.fullmatch(r"[0-9a-f]{64}", e.get("sha256", ""))])
    out.append(("M6", pp["short"], "sha256", ["sha256", pp["short"], str(pp.get("file", ""))], True, lambda d, sh=pp["short"]: next(e for e in d["research"]["papers"] if e["short"] == sh).__setitem__("sha256", "0" * 63 + "1")))
    sp = rng.choice([e for e in res["secondaryPapers"] if re.fullmatch(r"[0-9a-f]{64}", e.get("sha256", ""))])
    out.append(("M6", sp["short"], "sha256", ["sha256", sp["short"]], False, lambda d, sh=sp["short"]: next(e for e in d["research"]["secondaryPapers"] if e["short"] == sh).__setitem__("sha256", "0" * 63 + "2")))  # declared uncatchable: no file to compare
    picks = pick(rng, items, lambda i: isinstance(i.get("description"), str), 3, "C")
    out.append(("C", picks[0]["id"], "description", ["description"], True, lambda d, iid=picks[0]["id"]: item(d, iid).__setitem__("description", item(d, iid)["description"] + " (RL-15b control edit.)")))
    out.append(("C", "updates", "updates", ["updates"], True, lambda d: d["updates"].append({"at": "2026-11-07T23:00:00+08:00", "note": "RL-15b control: a benign dated update entry with a UTC offset."})))
    out.append(("C", picks[2]["id"], "title", ["title"], True, lambda d, iid=picks[2]["id"]: item(d, iid).__setitem__("title", item(d, iid)["title"] + " (RL-15b)")))
    return out


def new_rule(message):
    return any(tag in message for tag in TAGS)


def older_rule(message):
    return next((pat for pat in OLDER_RULES if re.search(pat, message)), None)


def main(base, work, out_path):
    base, work = pathlib.Path(base), pathlib.Path(work)
    assert "scratch" in str(base), "never the bridge's roadmap/"
    assert work.name == "roadmap", "the work copy must be named roadmap/ under its own parent (paper paths resolve from the repository root)"
    rng = random.Random(SEED)
    data = json.loads((base / "roadmap.json").read_text(encoding="utf-8"))
    manifest = {str(q.relative_to(base)): hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(base.rglob("*")) if q.is_file() and "__pycache__" not in q.parts}
    rec = {"seed": SEED, "capture": "whole message", "tags": list(TAGS), "olderRules": OLDER_RULES, "interpreter": sys.version.split()[0], "layout": {"work": work.name, "parent": work.parent.name},
           "baseManifestFiles": len(manifest), "baseManifestDigest": hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest(), "base": manifest, "runs": []}
    reset(base, work)
    rec["baseline"] = build(work)
    for klass, target, field, tokens, catchable, apply in mutations(data, rng):
        reset(base, work)
        d = json.loads((work / "roadmap.json").read_text(encoding="utf-8"))
        apply(d)
        (work / "roadmap.json").write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        res = build(work)
        by_new = bool(res["refused"] and new_rule(res["message"]))
        by_older = older_rule(res["message"]) if (res["refused"] and not by_new) else None
        res.update({"class": klass, "target": target, "field": field, "tokens": tokens, "catchable": catchable,
                    "attributedToNewRule": by_new, "attributedToOlderRule": by_older, "attributed": bool(by_new or by_older)})
        rec["runs"].append(res)
        print(klass, target, "refused" if res["refused"] else "built", res["exit"], res["wall_s"], "s", "NEW" if by_new else (by_older or ""))
    seeded = [r for r in rec["runs"] if r["class"] != "C"]
    catchable = [r for r in seeded if r["catchable"]]
    controls = [r for r in rec["runs"] if r["class"] == "C"]
    rec["qualifying"] = dict(QUALIFYING)
    rec["counts"] = {"seeded": len(seeded), "catchable": len(catchable), "uncatchable": len(seeded) - len(catchable),
                     "seededRefused": sum(r["refused"] for r in seeded), "catchableRefused": sum(r["refused"] for r in catchable),
                     "attributed": sum(r["attributed"] for r in catchable), "byNewRule": sum(r["attributedToNewRule"] for r in catchable), "byOlderRule": sum(1 for r in catchable if r["attributedToOlderRule"]),
                     "unattributedRefusals": sum(1 for r in catchable if r["refused"] and not r["attributed"]),
                     "newRulePerClass": {k: sum(1 for r in catchable if r["class"] == k and r["attributedToNewRule"]) for k in ("M4", "M6")},
                     "seededCrashed": sum(r["crashed"] for r in seeded), "controls": len(controls), "controlsRefused": sum(r["refused"] for r in controls), "controlsNonZero": sum(1 for r in controls if r["exit"] != 0),
                     "uncatchableOutcome": [("refused" if r["refused"] else "built") for r in seeded if not r["catchable"]],
                     "perClass": {k: [sum(1 for r in catchable if r["class"] == k and r["attributed"]), sum(1 for r in catchable if r["class"] == k and r["refused"]), sum(1 for r in catchable if r["class"] == k)] for k in ("M1", "M2", "M3", "M4", "M5", "M6")}}
    json.dump(rec, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(rec["counts"]))


if __name__ == "__main__":
    main(*sys.argv[1:4])
