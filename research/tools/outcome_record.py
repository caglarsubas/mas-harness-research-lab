"""Experiment outcome records (R13 issue 4, 2026-11-09; charter step 1c): one OUTCOME.json per experiment folder, form
planeon.research.experiment-outcome/v1, one entry per attempt (a PREREG version taken to review or to a run), so that a
pre-run stop, a completed run and a pending one are distinguishable by the collector without parsing prose.

usage:
  python3 -I -B outcome_record.py backfill EXPERIMENTS_DIR
      writes OUTCOME.json for every RL-* folder from its records: PREREG.md digest, PREREG-REVIEW.md rounds, RESULTS.json
      presence; the two recorded pre-run stops (RL-15 under v3, RL-21 under v1) are declared in STOPS below with their
      evidence anchors. Existing files are rewritten only when their content changes.
  python3 -I -B outcome_record.py add EXPERIMENT_DIR --version vN --sha256 HEX --stage STAGE --outcome OUTCOME
      [--stop-stage S --cause TEXT --detector D --class C] [--evidence PATH]
      appends one attempt for a new experiment (from RL-23 on), written at every stop and at the gated run's start.
  python3 -I -B outcome_record.py check FILE...     validates the form (enums, required fields); exit 1 on any defect.
Standard library only."""
import datetime
import hashlib
import json
import pathlib
import re
import sys

SCHEMA = "planeon.research.experiment-outcome/v1"
STAGES = ("PREREG", "REVIEW", "PREFLIGHT", "GATED_RUN", "RESULTS")
OUTCOMES = ("COMPLETED_NO_STOP", "STOPPED", "PENDING")
DETECTORS = ("REVIEW", "LAB_PREFLIGHT", "LAB_RUN", "AUDIT")
CLASSES = ("CAUGHT_BY_PREFLIGHT", "ESCAPED_TO_GATED_RUN", "ESCAPED_TO_AUDIT", "FALSE_BLOCK", "NONE")
HEAD = re.compile(r"^## Review (\d+), of PREREG (v\d+) \(([0-9a-f]{8})\), (\d{4}-\d{2}-\d{2}): (PASS|FAIL)", re.M)
REVIEW_ADOPTED = "2026-11-05"
# The two pre-run stops the records hold (meta-review 001's STOP findings), declared here with their evidence anchors.
STOPS = {
    "RL-15": {"afterReview": 3, "version": "v3", "prefix": "cda3e838", "stage": "GATED_RUN", "detector": "LAB_RUN",
              "class": "ESCAPED_TO_GATED_RUN",
              "cause": "the mutation tool stopped while drawing M4's targets: no READY item carried an evidence state the class needs; "
                       "the baseline had built, no seeded build ran (review 3's note 2 made real); v4 redrew M4 and went to review 4",
              "anchor": "## Instrument stop before any seeded build, under v3"},
    "RL-21": {"afterReview": 1, "version": "v1", "prefix": "73c96e89", "stage": "PREFLIGHT", "detector": "LAB_PREFLIGHT",
              "class": "CAUGHT_BY_PREFLIGHT",
              "cause": "before any run the lab's own inventory showed the meta authorities' metaBaseline is a commit id, not a packet id, "
                       "so H-26c's chain rule was not computable from the export; v2 made H-26c descriptive and went to review 2",
              "anchor": "the lab's own inventory showed"},
}


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def rounds_of(review_path, exp):
    text = review_path.read_text(encoding="utf-8")
    if exp == "RL-15b":  # single-round layout: "VERDICT: PASS" and no numbered heading
        return [{"round": 1, "version": "v1", "prefix": None, "date": re.search(r"(\d{4}-\d{2}-\d{2})", text).group(1),
                 "verdict": "PASS" if "VERDICT: PASS" in text else "FAIL"}]
    return [{"round": int(m.group(1)), "version": m.group(2), "prefix": m.group(3), "date": m.group(4), "verdict": m.group(5)}
            for m in HEAD.finditer(text)]


def version_key(path):
    return tuple(int(x) for x in re.findall(r"\d+", path.name.split("PREREG.", 1)[1]))


def prereg_file(folder, version=None):
    """PREREG.md when present (the frozen current version), else the highest PREREG.v*.md; with a version, that
    version's file (PREREG.vN.md keeps a superseded version) when it exists."""
    if version and (folder / ("PREREG.%s.md" % version)).exists():
        return folder / ("PREREG.%s.md" % version)
    if (folder / "PREREG.md").exists():
        return folder / "PREREG.md"
    versions = sorted(folder.glob("PREREG.v*.md"), key=version_key)
    return versions[-1] if versions else None


def backfill_folder(folder):
    exp = folder.name
    prereg = prereg_file(folder)
    assert prereg is not None, "%s has no PREREG file" % exp
    review = folder / "PREREG-REVIEW.md"
    results = folder / "RESULTS.json"
    rounds = rounds_of(review, exp) if review.exists() else []
    attempts = []
    stop = STOPS.get(exp)
    if stop:
        before = [r for r in rounds if r["round"] <= stop["afterReview"]]
        vfile = prereg_file(folder, stop["version"])
        vsha = sha(vfile) if vfile and vfile.name != "PREREG.md" else None
        assert vsha is None or vsha.startswith(stop["prefix"]), "%s: the kept %s file does not match the review heading's prefix" % (exp, stop["version"])
        attempts.append({"attempt": 1, "preregVersion": stop["version"],
                         "preregDigest": {"sha256": vsha, "prefix": stop["prefix"],
                                          "source": ("experiments/%s/%s (the superseded version, kept)" % (exp, vfile.name)) if vsha else "PREREG-REVIEW.md heading; the version file is not kept"},
                         "reviewRounds": len(before), "reviewVerdict": before[-1]["verdict"] if before else None,
                         "stageReached": stop["stage"], "outcome": "STOPPED",
                         "stop": {"stage": stop["stage"], "cause": stop["cause"], "detector": stop["detector"]}, "class": stop["class"],
                         "evidence": {"path": "experiments/%s/PREREG-REVIEW.md" % exp, "sha256": sha(review), "anchor": stop["anchor"]}})
        later = [r for r in rounds if r["round"] > stop["afterReview"]]
    else:
        later = rounds
    final_version = later[-1]["version"] if later else ("v1" if rounds == [] else rounds[-1]["version"])
    digest = sha(prereg)
    if later and later[-1]["prefix"] and not digest.startswith(later[-1]["prefix"]):
        note_digest = "PREREG.md's current digest does not start with the last reviewed prefix; both recorded"
    else:
        note_digest = None
    completed = results.exists()
    attempts.append({"attempt": len(attempts) + 1, "preregVersion": final_version,
                     "preregDigest": {"sha256": digest, "prefix": later[-1]["prefix"] if later else None, "source": "experiments/%s/%s as it stands" % (exp, prereg.name),
                                      **({"note": note_digest} if note_digest else {})},
                     "reviewRounds": len(later), "reviewVerdict": later[-1]["verdict"] if later else None,
                     "stageReached": "RESULTS" if completed else "PREREG", "outcome": "COMPLETED_NO_STOP" if completed else "PENDING",
                     "stop": None, "class": "NONE",
                     "evidence": {"path": "experiments/%s/RESULTS.json" % exp, "sha256": sha(results), "anchor": None} if completed else None})
    notes = []
    if not review.exists():
        notes.append("predates the blind review (adopted %s); reviewRounds 0" % REVIEW_ADOPTED)
    if exp == "RL-15":
        notes.append("run-002 (the corrected record) is a second run under the same version, not a new attempt")
    return {"schemaVersion": SCHEMA, "experiment": exp, "attempts": attempts, "notes": notes,
            "recordedBy": {"tool": "research/tools/outcome_record.py", "sha256": sha(__file__), "mode": "backfill", "date": now()}}


def write_if_changed(path, doc):
    new = json.dumps(doc, indent=1, sort_keys=True) + "\n"
    if path.exists():
        old = json.loads(path.read_text(encoding="utf-8"))
        old.pop("recordedBy", None)
        cmp = dict(doc)
        cmp.pop("recordedBy", None)
        if old == cmp:
            return False
    path.write_text(new, encoding="utf-8")
    return True


def backfill(exp_dir):
    exp_dir = pathlib.Path(exp_dir)
    written = total = 0
    for folder in sorted(p for p in exp_dir.glob("RL-*") if p.is_dir()):
        doc = backfill_folder(folder)
        problems = validate(doc)
        assert not problems, (folder.name, problems)
        total += 1
        written += write_if_changed(folder / "OUTCOME.json", doc)
    print("outcome records: %d folders, %d written or changed" % (total, written))


def validate(doc):
    p = []
    if doc.get("schemaVersion") != SCHEMA:
        p.append("schemaVersion")
    if not re.fullmatch(r"RL-\d{2}[a-z]?", str(doc.get("experiment", ""))):
        p.append("experiment")
    atts = doc.get("attempts")
    if not isinstance(atts, list) or not atts:
        return p + ["attempts empty"]
    for i, a in enumerate(atts, 1):
        if a.get("attempt") != i:
            p.append("attempt %d numbering" % i)
        if a.get("stageReached") not in STAGES:
            p.append("attempt %d stageReached" % i)
        if a.get("outcome") not in OUTCOMES:
            p.append("attempt %d outcome" % i)
        if a.get("class") not in CLASSES:
            p.append("attempt %d class" % i)
        if a.get("outcome") == "STOPPED":
            s = a.get("stop") or {}
            if s.get("stage") not in STAGES or s.get("detector") not in DETECTORS or not s.get("cause"):
                p.append("attempt %d stop fields" % i)
            if a.get("class") == "NONE":
                p.append("attempt %d stopped with class NONE" % i)
        else:
            if a.get("stop") is not None:
                p.append("attempt %d stop on a non-stopped attempt" % i)
        if a.get("outcome") != "PENDING" and not (a.get("evidence") or {}).get("sha256"):
            p.append("attempt %d evidence" % i)
        d = a.get("preregDigest") or {}
        if not (d.get("sha256") or d.get("prefix")):
            p.append("attempt %d preregDigest" % i)
    return p


def add(folder, args):
    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default
    folder = pathlib.Path(folder)
    path = folder / "OUTCOME.json"
    doc = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schemaVersion": SCHEMA, "experiment": folder.name, "attempts": [], "notes": []}
    outcome = opt("--outcome")
    ev = opt("--evidence")
    att = {"attempt": len(doc["attempts"]) + 1, "preregVersion": opt("--version"),
           "preregDigest": {"sha256": opt("--sha256"), "prefix": (opt("--sha256") or "")[:8] or None, "source": "the frozen PREREG at this attempt"},
           "reviewRounds": int(opt("--rounds", "0")), "reviewVerdict": opt("--review-verdict"),
           "stageReached": opt("--stage"), "outcome": outcome,
           "stop": {"stage": opt("--stop-stage"), "cause": opt("--cause"), "detector": opt("--detector")} if outcome == "STOPPED" else None,
           "class": opt("--class", "NONE"),
           "evidence": {"path": ev, "sha256": sha(ev), "anchor": opt("--anchor")} if ev else None}
    doc["attempts"].append(att)
    doc["recordedBy"] = {"tool": "research/tools/outcome_record.py", "sha256": sha(__file__), "mode": "add", "date": now()}
    problems = validate(doc)
    if problems:
        print("REFUSED:", "; ".join(problems))
        return 1
    path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("attempt %d recorded for %s" % (att["attempt"], folder.name))
    return 0


def check(files):
    bad = 0
    for f in files:
        problems = validate(json.loads(pathlib.Path(f).read_text(encoding="utf-8")))
        if problems:
            bad += 1
            print(pathlib.Path(f).parent.name, "DEFECT:", "; ".join(problems))
    print("OUTCOME check: %d files, %d defective" % (len(files), bad))
    return 1 if bad else 0


def main(argv):
    if argv[:1] == ["backfill"] and len(argv) == 2:
        backfill(argv[1])
        return 0
    if argv[:1] == ["add"] and len(argv) >= 2:
        return add(argv[1], argv[2:])
    if argv[:1] == ["check"] and len(argv) >= 2:
        return check(argv[1:])
    print(__doc__)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
