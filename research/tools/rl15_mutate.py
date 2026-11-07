"""RL-15 (H-30): seeded-inconsistency benchmark for the roadmap build, on a scratch copy only.
usage: python3 -I -B rl15_mutate.py BASE_DIR WORK_DIR OUT.json
BASE_DIR is a pristine copy of roadmap/ (never roadmap/ itself); WORK_DIR is a sibling scratch directory that is
re-created from BASE_DIR before every build. Six mutation classes x 3 seeded instances plus 3 benign controls (PREREG v2: M6 = the register's 'stale snapshot digest'); each
instance is applied to WORK_DIR/roadmap.json and the build run there; refused = the build exits non-zero with a
message starting "roadmap.json:". Output: counts, per-instance outcome, exit code and the first 120 characters of
the refusal message (the validator's own words), the edited field and the target's name tokens for attribution; no item text is copied."""
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
ENV = {"PATH": "/usr/bin:/bin"}  # TMPDIR is set per build to the work copy's parent (post-run privacy edit: a literal system temp path removed)


def reset(base, work):
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(base, work, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def build(work):
    t0 = time.monotonic()
    r = subprocess.run([sys.executable, "-I", "-B", "build_roadmap.py"], cwd=str(work), capture_output=True, text=True, timeout=600, env=dict(ENV, TMPDIR=str(work.parent)))
    msg = (r.stderr.strip().splitlines() or [""])[-1] if r.returncode != 0 else ""
    refused = r.returncode != 0 and msg.startswith("roadmap.json:")
    crashed = r.returncode != 0 and not refused  # PREREG v3: a non-zero exit without the validators' prefix
    return {"exit": r.returncode, "refused": refused, "crashed": crashed, "message": msg[:120], "wall_s": round(time.monotonic() - t0, 2)}


QUALIFYING = {}


def pick(rng, items, pred, k, klass):
    pool = [i for i in items if pred(i)]
    QUALIFYING[klass] = QUALIFYING.get(klass, 0) + len(pool)
    if len(pool) < k:
        raise SystemExit("rl15: class %s has %d qualifying targets, fewer than %d" % (klass, len(pool), k))
    return rng.sample(pool, k)


def mutations(data, rng):
    items = data["items"]
    ids = {i["id"] for i in items}
    out = []
    # M1 dangling dependency
    for it in pick(rng, items, lambda i: isinstance(i.get("dependsOn"), list), 3, "M1"):
        out.append(("M1", it["id"], "dependsOn", ["dependsOn", "NO-SUCH-ITEM-999"], lambda d, iid=it["id"]: next(i for i in d["items"] if i["id"] == iid)["dependsOn"].append("NO-SUCH-ITEM-999")))
    # M2 status against evidence state: a DONE item marked PLANNED
    for it in pick(rng, items, lambda i: i.get("status") == "DONE" and i.get("evidenceState") != "PLANNED", 3, "M2"):
        out.append(("M2", it["id"], "evidenceState", ["evidenceState", "PLANNED"], lambda d, iid=it["id"]: next(i for i in d["items"] if i["id"] == iid).__setitem__("evidenceState", "PLANNED")))
    # M3 score drift: a benefit factor out of scale (7), at zero (0), or a factor missing
    picks = pick(rng, items, lambda i: isinstance(i.get("benefit"), dict) and "B2" in i["benefit"], 3, "M3")
    out.append(("M3", picks[0]["id"], "benefit", ["benefit", "B2"], lambda d, iid=picks[0]["id"]: next(i for i in d["items"] if i["id"] == iid)["benefit"]["B2"].__setitem__(0, 7)))
    out.append(("M3", picks[1]["id"], "benefit", ["benefit", "B2"], lambda d, iid=picks[1]["id"]: next(i for i in d["items"] if i["id"] == iid)["benefit"]["B2"].__setitem__(0, 0)))
    out.append(("M3", picks[2]["id"], "benefit", ["benefit", "B2"], lambda d, iid=picks[2]["id"]: next(i for i in d["items"] if i["id"] == iid)["benefit"].pop("B2")))
    # M4 status change without an update entry: READY -> DONE, updates untouched
    for it in pick(rng, items, lambda i: i.get("status") in ("READY", "IN_PROGRESS") and i.get("evidenceState") in ("IMPLEMENTED", "CONTRACT_ADOPTED"), 3, "M4"):  # PREREG v4: open items with an evidence state consistent with DONE (exactly 3 qualify)
        out.append(("M4", it["id"], "status", ["updates", "update"], lambda d, iid=it["id"]: next(i for i in d["items"] if i["id"] == iid).__setitem__("status", "DONE")))
    # M5 stale reference: an unknown harness key, an unknown codebase id, a duplicated item id
    picks = pick(rng, items, lambda i: isinstance(i.get("harnesses"), dict) and i["harnesses"], 1, "M5")
    out.append(("M5", picks[0]["id"], "harnesses", ["harnesses", "H99"], lambda d, iid=picks[0]["id"]: next(i for i in d["items"] if i["id"] == iid)["harnesses"].__setitem__("H99", "NO-SUCH-HARNESS")))
    picks = pick(rng, items, lambda i: True, 1, "M5")
    out.append(("M5", picks[0]["id"], "codebases", ["codebases", "NO-SUCH-CODEBASE-999"], lambda d, iid=picks[0]["id"]: next(i for i in d["items"] if i["id"] == iid).__setitem__("codebases", ["NO-SUCH-CODEBASE-999"])))
    picks = pick(rng, items, lambda i: True, 1, "M5")
    out.append(("M5", picks[0]["id"], "id", ["duplicate", "duplicated", picks[0]["id"]], lambda d, iid=picks[0]["id"]: d["items"].append(dict(next(i for i in d["items"] if i["id"] == iid)))))
    # M6 stale snapshot digest (the register's class): a source digest malformed (63 hex); a paper's digest replaced
    # while its file in research/papers/ is unchanged; a secondary paper's digest replaced (no file in the bridge)
    res = data["research"]
    s = rng.choice([e for e in res["sources"] if re.fullmatch(r"[0-9a-f]{64}", e.get("sha256", ""))])
    QUALIFYING["M6"] = 12 + 8 + 29
    out.append(("M6", s["id"], "sha256", ["sha256", s["id"], str(s.get("file", ""))], lambda d, sid=s["id"]: next(e for e in d["research"]["sources"] if e["id"] == sid).__setitem__("sha256", next(e for e in d["research"]["sources"] if e["id"] == sid)["sha256"][:63])))
    pp = rng.choice([e for e in res["papers"] if re.fullmatch(r"[0-9a-f]{64}", e.get("sha256", ""))])
    out.append(("M6", pp["short"], "sha256", ["sha256", pp["short"], str(pp.get("file", ""))], lambda d, sh=pp["short"]: next(e for e in d["research"]["papers"] if e["short"] == sh).__setitem__("sha256", "0" * 63 + "1")))
    sp = rng.choice([e for e in res["secondaryPapers"] if re.fullmatch(r"[0-9a-f]{64}", e.get("sha256", ""))])
    out.append(("M6", sp["short"], "sha256", ["sha256", sp["short"]], lambda d, sh=sp["short"]: next(e for e in d["research"]["secondaryPapers"] if e["short"] == sh).__setitem__("sha256", "0" * 63 + "2")))
    # C controls, benign: a description edit, an added dated update entry, a title edit
    picks = pick(rng, items, lambda i: isinstance(i.get("description"), str), 3, "C")
    out.append(("C", picks[0]["id"], "description", ["description"], lambda d, iid=picks[0]["id"]: next(i for i in d["items"] if i["id"] == iid).__setitem__("description", next(i for i in d["items"] if i["id"] == iid)["description"] + " (RL-15 control edit.)")))
    out.append(("C", "updates", "updates", ["updates"], lambda d: d["updates"].append({"at": "2026-11-05", "note": "RL-15 control: a benign dated update entry."})))
    out.append(("C", picks[2]["id"], "title", ["title"], lambda d, iid=picks[2]["id"]: next(i for i in d["items"] if i["id"] == iid).__setitem__("title", next(i for i in d["items"] if i["id"] == iid)["title"] + " (RL-15)")))
    return out


def main(base, work, out_path):
    base, work = pathlib.Path(base), pathlib.Path(work)
    assert base.name != "roadmap" or "scratch" in str(base), "never the bridge's roadmap/"
    rng = random.Random(SEED)
    data = json.loads((base / "roadmap.json").read_text(encoding="utf-8"))
    manifest = {str(q.relative_to(base)): hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(base.rglob("*")) if q.is_file() and "__pycache__" not in q.parts}
    rec = {"seed": SEED, "interpreter": sys.version.split()[0], "baseManifestFiles": len(manifest), "baseManifestDigest": hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest(), "base": manifest, "runs": []}
    reset(base, work)
    rec["baseline"] = build(work)
    for klass, target, field, tokens, apply in mutations(data, rng):
        reset(base, work)
        d = json.loads((work / "roadmap.json").read_text(encoding="utf-8"))
        apply(d)
        (work / "roadmap.json").write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        res = build(work)
        res.update({"class": klass, "target": target, "field": field, "tokens": tokens,
                    "attributed": res["refused"] and any(tok and re.search(r"(?<![A-Za-z0-9_-])" + re.escape(tok) + r"(?![A-Za-z0-9_-])", res["message"]) for tok in tokens)})  # whole, field-specific tokens (PREREG v4)
        rec["runs"].append(res)
        print(klass, target, "refused" if res["refused"] else "built", res["exit"], res["wall_s"], "s")
    seeded = [r for r in rec["runs"] if r["class"] != "C"]
    controls = [r for r in rec["runs"] if r["class"] == "C"]
    rec["qualifying"] = dict(QUALIFYING)
    rec["counts"] = {"seeded": len(seeded), "seededRefused": sum(r["refused"] for r in seeded), "seededAttributed": sum(r["attributed"] for r in seeded), "seededCrashed": sum(r["crashed"] for r in seeded), "controls": len(controls), "controlsRefused": sum(r["refused"] for r in controls), "controlsNonZero": sum(1 for r in controls if r["exit"] != 0),
                     "perClass": {k: [sum(1 for r in seeded if r["class"] == k and r["attributed"]), sum(1 for r in seeded if r["class"] == k and r["refused"]), sum(1 for r in seeded if r["class"] == k)] for k in ("M1", "M2", "M3", "M4", "M5", "M6")}}
    json.dump(rec, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(rec["counts"]))


if __name__ == "__main__":
    main(*sys.argv[1:4])
