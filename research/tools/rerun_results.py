"""Evaluator re-derivation (LAB-REPO-001; widened by R13 issue 1, recommendation 2): rerun_table.json names every
experiment folder once with a level. LEDGER_REDERIVED entries run their evaluator argv over the committed inputs into
TMPDIR and must reproduce RESULTS.json byte for byte; RAW_REPRODUCED entries first regenerate committed inputs from a
raw source in the tree; INDEPENDENT_REPLICATION entries compare a second ledger's verdicts; RECORDED entries carry a
reason and externalInputs (source, commit, sha256, availability, retrieval), each sha256 among the ledger's evidence.
The PREREG argument is the file whose digest the ledger names. Counts only; writes under TMPDIR only. Standard library.

A PENDING folder (no RESULTS.json, and its OUTCOME.json's last attempt is PENDING: a frozen experiment whose ledger does not
exist yet; MON-292-RL-M101-RULE, Q-SYNC2-1 (a), the twin of prereg_check's PENDING rule) has nothing to re-derive: it needs no
table entry and an entry naming it is refused (PENDING_ENTRY). A folder without a ledger that is not PENDING still fails the
count. The OK line names the pending folders' count.

usage: python3 -I -B research/tools/rerun_results.py TABLE_JSON
       python3 -I -B research/tools/rerun_results.py --self-test     (four PENDING vectors in temporary trees)
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "planeon.research.rerun-table/v1"
LEVELS = ("LEDGER_REDERIVED", "RAW_REPRODUCED", "INDEPENDENT_REPLICATION", "RECORDED")
AVAILABILITY = ("IN_TREE", "OWNER_HELD", "UNPUBLISHED")
HEX64 = re.compile(r"^[0-9a-f]{64}(?![\s\S])")
HEX40 = re.compile(r"^[0-9a-f]{40}(?![\s\S])")
ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9_.~-])/(?:Users|home|private|root|tmp)/")
INPUT_KEYS = ("source", "commit", "sha256", "availability", "retrieval")
COMMON = ("folder", "level", "ledger")
BY_LEVEL = {"LEDGER_REDERIVED": ("argv", "evaluator", "evaluatorSha256", "preregSha256"),
            "RAW_REPRODUCED": ("argv", "evaluator", "evaluatorSha256", "preregSha256", "rawArgv", "regenerates"),
            "INDEPENDENT_REPLICATION": ("argv", "evaluator", "evaluatorSha256", "preregSha256", "replication"),
            "RECORDED": ("reason", "externalInputs")}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ledger_digests(doc) -> set:
    out = set()

    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "evidenceRefs" and isinstance(item, list):
                    out.update(str(x).split(":")[-1] for x in item)
                elif key in ("contentDigest", "scopeDigest") and isinstance(item, str):
                    out.add(item.split(":")[-1])
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(doc)
    return out


def safe_rel(value) -> bool:
    return isinstance(value, str) and value and not value.startswith("/") and ".." not in Path(value).parts


def run_argv(argv: list, root: Path, placeholder: str, target: Path) -> bool:
    cmd = [target.as_posix() if a == placeholder else a for a in argv]
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "TMPDIR": os.environ.get("TMPDIR", tempfile.gettempdir()),
           "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
    done = subprocess.run(cmd, cwd=root, env=env, capture_output=True)
    return done.returncode == 0


def check_rederive(entry: dict, root: Path, ledger: Path, refs: set, scratch: Path, problems: list) -> None:
    name = entry["folder"]
    argv = entry.get("argv")
    if not (isinstance(argv, list) and len(argv) >= 5 and all(isinstance(a, str) for a in argv)
            and argv[:3] == ["python3", "-I", "-B"] and argv.count("OUT") == 1 and argv[-1] == "OUT"):
        problems.append("ARGV_SHAPE:" + name)
        return
    evaluator = root / argv[3]
    if not (safe_rel(argv[3]) and argv[3] == entry.get("evaluator") and evaluator.is_file()
            and sha256(evaluator) == entry.get("evaluatorSha256") and entry["evaluatorSha256"] in refs):
        problems.append("EVALUATOR_MISMATCH:" + name)
        return
    preregs = [a for a in argv[4:-1] if Path(a).name.startswith("PREREG")]
    if not (len(preregs) == 1 and safe_rel(preregs[0]) and (root / preregs[0]).is_file()
            and sha256(root / preregs[0]) == entry.get("preregSha256") and entry["preregSha256"] in refs):
        problems.append("PREREG_MISMATCH:" + name)
        return
    for a in argv[4:-1]:
        if not (safe_rel(a) and (root / a).is_file()):
            problems.append("INPUT_MISSING:%s:%s" % (name, a))
            return
    out = scratch / (name + ".RESULTS.json")
    if not run_argv(argv, root, "OUT", out):
        problems.append("EVALUATOR_FAILED:" + name)
        return
    if not (out.is_file() and out.read_bytes() == ledger.read_bytes()):
        problems.append("LEDGER_DIFFERS:" + name)


def check_raw(entry: dict, root: Path, scratch: Path, problems: list) -> bool:
    name = entry["folder"]
    raw = entry.get("rawArgv")
    regen = entry.get("regenerates")
    if not (isinstance(raw, list) and len(raw) >= 4 and all(isinstance(a, str) for a in raw) and raw[:3] == ["python3", "-I", "-B"]
            and raw.count("OUT_DIR") == 1 and isinstance(regen, list) and regen
            and all(isinstance(r, dict) and set(r) == {"path", "produced"} and safe_rel(r["path"]) and safe_rel(r["produced"]) for r in regen)):
        problems.append("RAW_SHAPE:" + name)
        return False
    out_dir = scratch / (name + ".raw")
    out_dir.mkdir()
    if not run_argv(raw, root, "OUT_DIR", out_dir):
        problems.append("RAW_FAILED:" + name)
        return False
    for r in regen:
        produced = out_dir / r["produced"]
        if not (produced.is_file() and (root / r["path"]).is_file() and produced.read_bytes() == (root / r["path"]).read_bytes()):
            problems.append("RAW_DIFFERS:%s:%s" % (name, r["path"]))
            return False
    return True


def check_replication(entry: dict, root: Path, ledger: Path, problems: list) -> None:
    name = entry["folder"]
    rep = entry.get("replication")
    if not (isinstance(rep, dict) and set(rep) == {"ledger", "sha256"} and safe_rel(rep["ledger"])
            and isinstance(rep["sha256"], str) and HEX64.match(rep["sha256"])):
        problems.append("REPLICATION_SHAPE:" + name)
        return
    other = root / rep["ledger"]
    if not (other.is_file() and sha256(other) == rep["sha256"]):
        problems.append("REPLICATION_MISSING:" + name)
        return
    try:
        a = json.loads(ledger.read_text(encoding="utf-8")).get("claimVerdicts")
        b = json.loads(other.read_text(encoding="utf-8")).get("claimVerdicts")
    except (ValueError, UnicodeDecodeError):
        problems.append("REPLICATION_UNREADABLE:" + name)
        return
    if a is None or a != b:
        problems.append("REPLICATION_VERDICTS_DIFFER:" + name)


def check_recorded(entry: dict, root: Path, refs: set, problems: list) -> None:
    name = entry["folder"]
    reason = entry.get("reason")
    inputs = entry.get("externalInputs")
    if not (isinstance(reason, str) and reason.strip() and "\n" not in reason):
        problems.append("REASON_MISSING:" + name)
    if not (isinstance(inputs, list) and inputs):
        problems.append("EXTERNAL_INPUTS_MISSING:" + name)
        return
    for i, item in enumerate(inputs):
        ok = (isinstance(item, dict) and set(item) == set(INPUT_KEYS) and all(isinstance(item[k], str) for k in INPUT_KEYS)
              and (item["commit"] == "none" or HEX40.match(item["commit"])) and HEX64.match(item["sha256"])
              and item["availability"] in AVAILABILITY and item["source"].strip() and item["retrieval"].strip()
              and "\n" not in item["retrieval"] and not ABSOLUTE_PATH.search(item["retrieval"]))
        if not ok:
            problems.append("EXTERNAL_INPUT_SHAPE:%s:%d" % (name, i))
            continue
        if item["sha256"] not in refs:
            problems.append("EXTERNAL_INPUT_NOT_IN_LEDGER:%s:%d" % (name, i))
        if item["availability"] == "IN_TREE":
            path = root / item["source"]
            if not (safe_rel(item["source"]) and path.is_file() and sha256(path) == item["sha256"]):
                problems.append("IN_TREE_INPUT_MISSING:%s:%d" % (name, i))


def pending_folder(folder: Path) -> bool:
    """True for a folder with no RESULTS.json whose OUTCOME.json's last attempt is PENDING (charter step 1c)."""
    record = folder / "OUTCOME.json"
    if (folder / "RESULTS.json").exists() or not record.is_file():
        return False
    try:
        doc = json.loads(record.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError):
        return False
    attempts = doc.get("attempts") if isinstance(doc, dict) else None
    if not isinstance(attempts, list) or not attempts or not isinstance(attempts[-1], dict):
        return False
    return attempts[-1].get("outcome") == "PENDING"


def check_table(table: Path):
    """Returns (problems, counts, pending) for one table: the problem lines, the entries checked per level, the PENDING folders."""
    root = table.parent.parent.parent
    doc = json.loads(table.read_text(encoding="utf-8"))
    problems, counts = [], {level: 0 for level in LEVELS}
    if not (isinstance(doc, dict) and doc.get("schemaVersion") == SCHEMA and isinstance(doc.get("entries"), list)):
        return ["TABLE_SHAPE:" + table.relative_to(root).as_posix()], counts, 0
    experiments = root / "research" / "experiments"
    folders = sorted(p.name for p in experiments.glob("RL-*") if p.is_dir())
    pending = [name for name in folders if pending_folder(experiments / name)]
    names = [e.get("folder") for e in doc["entries"] if isinstance(e, dict)]
    for name in folders:
        if name in pending:
            if names.count(name):
                problems.append("PENDING_ENTRY:%s:%d" % (name, names.count(name)))
        elif names.count(name) != 1:
            problems.append("FOLDER_ENTRY_COUNT:%s:%d" % (name, names.count(name)))
    for name in names:
        if name not in folders:
            problems.append("FOLDER_UNKNOWN:%s" % name)
    with tempfile.TemporaryDirectory(prefix="rerun-") as tmp:
        scratch = Path(tmp)
        for entry in doc["entries"]:
            name = entry.get("folder") if isinstance(entry, dict) else None
            if name not in folders or name in pending or names.count(name) != 1:
                continue
            level = entry.get("level")
            if level not in LEVELS:
                problems.append("LEVEL_UNKNOWN:" + name)
                continue
            if set(entry) != set(COMMON) | set(BY_LEVEL[level]):
                problems.append("ENTRY_MEMBERS:" + name)
                continue
            ledger = root / str(entry["ledger"])
            expected = "research/experiments/%s/RESULTS.json" % name
            if entry["ledger"] != expected or not ledger.is_file():
                problems.append("LEDGER_PATH:" + name)
                continue
            try:
                refs = ledger_digests(json.loads(ledger.read_text(encoding="utf-8")))
            except (ValueError, UnicodeDecodeError):
                problems.append("LEDGER_UNREADABLE:" + name)
                continue
            counts[level] += 1
            if level == "RECORDED":
                check_recorded(entry, root, refs, problems)
                continue
            if level == "RAW_REPRODUCED" and not check_raw(entry, root, scratch, problems):
                continue
            check_rederive(entry, root, ledger, refs, scratch, problems)
            if level == "INDEPENDENT_REPLICATION":
                check_replication(entry, root, ledger, problems)
    return problems, counts, len(pending)


def self_test() -> int:
    """Four PENDING vectors (MON-292-RL-M101-RULE), each in its own temporary tree with an otherwise empty table: a PENDING
    folder without an entry, accepted; a folder without a ledger that is not PENDING, still refused; a PENDING folder with an
    entry, refused; a PENDING record beside a RESULTS.json, not pending, so the missing entry is refused."""
    vectors = [("RL-90", "PENDING", False, False, [], 1),
               ("RL-91", "STOPPED", False, False, ["FOLDER_ENTRY_COUNT:RL-91:0"], 0),
               ("RL-92", "PENDING", False, True, ["PENDING_ENTRY:RL-92:1"], 1),
               ("RL-93", "PENDING", True, False, ["FOLDER_ENTRY_COUNT:RL-93:0"], 0)]
    failures = 0
    for name, outcome, ledger, entry, expected, expected_pending in vectors:
        with tempfile.TemporaryDirectory(prefix="rerun-selftest-") as tmp:
            root = Path(tmp)
            folder = root / "research" / "experiments" / name
            folder.mkdir(parents=True)
            (folder / "OUTCOME.json").write_text(json.dumps({"experiment": name, "attempts": [{"attempt": 1, "outcome": outcome}]}), encoding="utf-8")
            if ledger:
                (folder / "RESULTS.json").write_text("{}", encoding="utf-8")
            table = root / "research" / "tools" / "rerun_table.json"
            table.parent.mkdir(parents=True)
            entries = [{"folder": name, "level": "RECORDED"}] if entry else []
            table.write_text(json.dumps({"schemaVersion": SCHEMA, "entries": entries}), encoding="utf-8")
            problems, _, pending = check_table(table)
            if sorted(problems) != sorted(expected) or pending != expected_pending:
                failures += 1
                print("SELFTEST VECTOR %s: got %s pending %d, expected %s pending %d" % (name, sorted(problems), pending, sorted(expected), expected_pending))
    if failures:
        print("SELFTEST FAIL: %d of %d vectors" % (failures, len(vectors)))
        return 1
    print("SELFTEST OK: %d vectors" % len(vectors))
    return 0


def main(argv: list) -> int:
    if argv == ["--self-test"]:
        return self_test()
    if len(argv) != 1:
        print("usage: rerun_results.py TABLE_JSON | --self-test")
        return 2
    problems, counts, pending = check_table(Path(argv[0]).resolve())
    if problems:
        for line in problems:
            print(line)
        print("RERUN FAIL: %d problems" % len(problems))
        return 1
    print("RERUN OK: %d entries (%d pending); %s" % (sum(counts.values()), pending, ", ".join("%s %d" % (k, counts[k]) for k in LEVELS)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
