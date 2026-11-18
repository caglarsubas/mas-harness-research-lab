"""Preregistration and review-record check (LAB-REPO-001): every experiment folder holds a frozen PREREG, its ledger and
its report; every frozen digest the register names resolves to a PREREG file; from RL-14 the blind review names the
run version and reads PASS and the ledger names its evaluator; review records match planeon.review-record/v2.
A folder whose OUTCOME.json last attempt is PENDING (a frozen PREREG awaiting its review or run; MON-LAB-FACTORY-3,
2026-11-12) is accepted only when PREREG.md's sha256 equals the outcome record's digest and its prefix is the register
row's pin, the folder holds no RESULT, LEDGER or REPORT file at all, and its PREREG-REVIEW.md, when the file exists, already
holds a passing review of that digest, read exactly as for a finished experiment: the file names the digest; with review
headers the last header naming it reads PASS; without any header the last VERDICT line reads PASS. A version that still
awaits its review has no review file, or none that passes: then the folder is refused until the review is recorded (packet
reviews LS2-R1-1, LS2-R2-1 and LS2-R3-1, 2026-11-18: no reading of the file is left that only a PENDING folder gets).
Counts only on stdout; problem lines are CODE:path. Standard library.

usage: python3 -I -B research/tools/prereg_check.py REGISTER_MD EXPERIMENTS_DIR
       python3 -I -B research/tools/prereg_check.py --self-test     (twenty-two PENDING vectors in temporary trees)
"""
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

HEX8 = re.compile(r"\b[0-9a-f]{8}\b")
HEADER = re.compile(r"^## Review (\d+),? of PREREG v(\S+) \(([0-9a-f]{8})\),? (\d{4}-\d{2}-\d{2}): (PASS|FAIL)", re.M)
PLAIN = re.compile(r"^(?:VERDICT|Verdict):? (PASS|FAIL)\b", re.M)
REVIEW_FROM = 14
END = r"(?![\s\S])"
HEX64 = re.compile(r"^[0-9a-f]{64}" + END)
HEX40 = re.compile(r"^[0-9a-f]{40}" + END)
SERIES = re.compile(r"^[A-Z][A-Z0-9-]{1,63}/[a-z][a-z0-9-]{0,31}" + END)
DATE = re.compile(r"^(?!0000)[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])" + END)
REPOSITORY = re.compile(r"^[A-Za-z0-9._-]{1,100}" + END)
FILE_PATH = re.compile(r"^(?!/)(?!(?:.*/)?\.\.?(?:/|" + END + r"))(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+" + END)
REQUIRED = ("briefSha256", "checked", "disclosures", "findings", "kind", "reviewDate", "reviewer", "round",
            "rulesSha256", "schemaVersion", "series", "subject", "verdict", "wrapperSha256")
OPTIONAL = ("base", "bindingRules", "dispositions", "notChecked", "questions")
SEVERITY = ("MAJOR", "MINOR", "NOTE")
DISPOSITION = ("ADDRESSED", "PARTLY_ADDRESSED", "NOT_ADDRESSED", "WITHDRAWN", "DISPUTED")


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


def register_rows(path: Path) -> dict:
    rows, started = {}, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            started = line.startswith("## Experiments started")
        if started and line.startswith("| RL-"):
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            if len(cells) >= 5:
                rows[cells[0]] = cells
    return rows


def numeric_id(name: str) -> int:
    m = re.match(r"RL-(\d+)", name)
    return int(m.group(1)) if m else 0


def nonempty_string(value, limit: int = 4000) -> bool:
    return isinstance(value, str) and 1 <= len(value) <= limit


def check_record(path: Path, root: Path, problems: list) -> None:
    rel = path.relative_to(root).as_posix()
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError):
        problems.append("RECORD_UNREADABLE:" + rel)
        return
    if not isinstance(doc, dict):
        problems.append("RECORD_SHAPE:" + rel)
        return
    unknown = [k for k in doc if k not in REQUIRED and k not in OPTIONAL]
    missing = [k for k in REQUIRED if k not in doc]
    if unknown or missing:
        problems.append("RECORD_MEMBERS:" + rel)
        return
    ok = doc["schemaVersion"] == "planeon.review-record/v2" and isinstance(doc["kind"], str) and len(doc["kind"]) <= 4000
    ok = ok and isinstance(doc["series"], str) and SERIES.match(doc["series"]) is not None
    ok = ok and type(doc["round"]) is int and doc["round"] >= 1
    ok = ok and isinstance(doc["reviewDate"], str) and DATE.match(doc["reviewDate"]) is not None
    ok = ok and isinstance(doc["briefSha256"], str) and HEX64.match(doc["briefSha256"]) is not None
    for key in ("rulesSha256", "wrapperSha256"):
        ok = ok and (doc[key] is None or (isinstance(doc[key], str) and HEX64.match(doc[key]) is not None))
    subj = doc["subject"]
    ok = ok and isinstance(subj, dict) and (
        (set(subj) == {"repository", "commit", "tree"} and REPOSITORY.match(str(subj["repository"])) is not None
         and HEX40.match(str(subj["commit"])) is not None and HEX40.match(str(subj["tree"])) is not None)
        or (set(subj) == {"path", "sha256"} and FILE_PATH.match(str(subj["path"])) is not None
            and HEX64.match(str(subj["sha256"])) is not None))
    rv = doc["reviewer"]
    ok = ok and isinstance(rv, dict) and set(rv) == {"model", "role"} and all(nonempty_string(v) for v in rv.values())
    ok = ok and nonempty_string(doc["verdict"])
    ok = ok and isinstance(doc["findings"], list) and all(
        isinstance(f, dict) and set(f) == {"blocks", "finding", "id", "location", "requiredChange", "severity"}
        and type(f["blocks"]) is bool and f["severity"] in SEVERITY
        and all(nonempty_string(f[k]) for k in ("finding", "id", "location", "requiredChange")) for f in doc["findings"])
    ok = ok and isinstance(doc["checked"], list) and len(doc["checked"]) >= 1 and all(
        nonempty_string(c) or (isinstance(c, dict) and set(c) == {"check", "result"} and nonempty_string(c["check"])
                               and nonempty_string(c["result"])) for c in doc["checked"])
    ok = ok and isinstance(doc["disclosures"], list) and all(nonempty_string(d) for d in doc["disclosures"])
    for key in ("bindingRules", "dispositions", "notChecked", "questions"):
        if key in doc:
            ok = ok and isinstance(doc[key], list)
    if "dispositions" in doc and ok:
        ok = all(isinstance(d, dict) and {"id", "status"} <= set(d) and d["status"] in DISPOSITION for d in doc["dispositions"])
    if not ok:
        problems.append("RECORD_SHAPE:" + rel)
        return
    brief = root / doc["kind"]
    if not (FILE_PATH.match(doc["kind"]) and brief.is_file() and sha256(brief) == doc["briefSha256"]):
        problems.append("RECORD_BRIEF_MISMATCH:" + rel)


STRAY = ("RESULT", "LEDGER", "REPORT")


def pending_attempt(folder: Path):
    """The OUTCOME.json's last attempt when its outcome is PENDING (charter step 1c), else None."""
    record = folder / "OUTCOME.json"
    if not record.is_file():
        return None
    try:
        doc = json.loads(record.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    attempts = doc.get("attempts") if isinstance(doc, dict) else None
    if not isinstance(attempts, list) or not attempts or not isinstance(attempts[-1], dict):
        return None
    return attempts[-1] if attempts[-1].get("outcome") == "PENDING" else None


def check_pending(folder: Path, root: Path, attempt: dict, row, problems: list) -> None:
    """A frozen PREREG awaiting its review or run: the three conditions of MON-LAB-FACTORY-3 (2026-11-12), plus its
    review, when one exists, reading PASS; a review file that names the pinned digest is read fail-closed."""
    rel = folder.relative_to(root).as_posix()
    prereg = folder / "PREREG.md"
    if not prereg.is_file():
        problems.append("PENDING_PREREG_MISSING:" + rel)
        return
    digest = sha256(prereg)
    recorded = attempt.get("preregDigest")
    recorded = recorded.get("sha256") if isinstance(recorded, dict) else None
    if digest != recorded:
        problems.append("PENDING_DIGEST_MISMATCH:" + rel)
    if row is None or digest[:8] not in HEX8.findall(row[4]):
        problems.append("PENDING_PIN_MISMATCH:" + rel)
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        if any(token in path.name.upper() for token in STRAY):
            problems.append("PENDING_STRAY_FILE:" + path.relative_to(root).as_posix())
    review = folder / "PREREG-REVIEW.md"
    if review.is_file():
        # the finished-experiment review reading of check_tree, applied to the pinned digest: the file names it; with review
        # headers the last header naming it reads PASS; without any header the last VERDICT line reads PASS. Anything else,
        # an unreadable file included, is a refusal: a PENDING folder gets no reading of its own (LS2-R3-1)
        try:
            text = review.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = ""
        headers = HEADER.findall(text)
        verdicts = [h[4] for h in headers if h[2] == digest[:8]] if headers else PLAIN.findall(text)
        if digest[:8] not in text or not verdicts or verdicts[-1] != "PASS":
            problems.append("PENDING_REVIEW_NOT_PASS:" + rel)

def check_tree(register: Path, exp_dir: Path):
    """Returns (problems, folders, pending, reviewed, records) for one register and experiments directory."""
    root = exp_dir.parent.parent
    tools_dir = root / "research" / "tools"
    tool_digests = {sha256(p) for p in sorted(tools_dir.glob("*.py"))} if tools_dir.is_dir() else set()
    rows = register_rows(register)
    problems, folders, pending, reviewed = [], 0, 0, 0
    for folder in sorted(p for p in exp_dir.glob("RL-*") if p.is_dir()):
        folders += 1
        name = folder.name
        rel = folder.relative_to(root).as_posix()
        preregs = {sha256(p): p for p in sorted(folder.glob("PREREG*.md")) if p.name != "PREREG-REVIEW.md"}
        if not preregs:
            problems.append("PREREG_MISSING:" + rel)
        if name not in rows:
            problems.append("REGISTER_ROW_MISSING:" + rel)
        else:
            prefixes = {d[:8] for d in preregs}
            for token in HEX8.findall(rows[name][4]):
                if token not in prefixes:
                    problems.append("FROZEN_DIGEST_MISSING:%s:%s" % (rel, token))
        attempt = pending_attempt(folder)
        if attempt is not None:
            pending += 1
            check_pending(folder, root, attempt, rows.get(name), problems)
            continue
        ledger, report = folder / "RESULTS.json", folder / "REPORT.md"
        if not ledger.is_file():
            problems.append("LEDGER_MISSING:" + rel)
        if not report.is_file():
            problems.append("REPORT_MISSING:" + rel)
        refs = set()
        if ledger.is_file():
            try:
                refs = ledger_digests(json.loads(ledger.read_text(encoding="utf-8")))
            except (ValueError, UnicodeDecodeError):
                problems.append("LEDGER_UNREADABLE:" + rel)
        run_versions = [preregs[d] for d in refs if d in preregs]
        if ledger.is_file() and refs and len(run_versions) != 1:
            problems.append("LEDGER_PREREG_MISSING:" + rel)
        if numeric_id(name) >= REVIEW_FROM:
            review = folder / "PREREG-REVIEW.md"
            if not review.is_file():
                problems.append("REVIEW_MISSING:" + rel)
            elif len(run_versions) == 1:
                run8 = sha256(run_versions[0])[:8]
                text = review.read_text(encoding="utf-8")
                headers = HEADER.findall(text)
                if run8 not in text:
                    problems.append("REVIEW_DIGEST_MISSING:" + rel)
                elif headers:
                    verdicts = [h[4] for h in headers if h[2] == run8]
                    if not verdicts or verdicts[-1] != "PASS":
                        problems.append("REVIEW_NOT_PASS:" + rel)
                    else:
                        reviewed += 1
                else:
                    plain = PLAIN.findall(text)
                    if not plain or plain[-1] != "PASS":
                        problems.append("REVIEW_NOT_PASS:" + rel)
                    else:
                        reviewed += 1
            if ledger.is_file() and not (refs & tool_digests):
                problems.append("LEDGER_EVALUATOR_MISSING:" + rel)
    records = 0
    reviews_dir = root / "research" / "reviews"
    if reviews_dir.is_dir():
        for path in sorted(reviews_dir.glob("*.json")):
            records += 1
            check_record(path, root, problems)
    return problems, folders, pending, reviewed, records


def self_test() -> int:
    """Twenty-two PENDING vectors, each in its own temporary tree ({D} stands for the PREREG's digest prefix). Conditions of
    MON-LAB-FACTORY-3: no review file, accepted; PREREG digest not the register's pin, refused; a stray RESULT file,
    refused; an outcome record naming another digest, refused. Review file present, read as for a finished experiment:
    accepted only for a header naming the digest that reads PASS last (also beside a body line or another digest's later
    header) or, without any header, a file naming the digest whose last VERDICT line is PASS; refused for a FAIL in either
    form, a bold, lower-case or unknown verdict word, an off-pattern header, no verdict, another digest's header beside a
    plain verdict (FAIL or PASS), and for every file that does not name the digest, whatever it says."""
    body = "# PREREG v1\n\nfrozen text\n"
    not_pass = lambda n: ["PENDING_REVIEW_NOT_PASS:research/experiments/" + n]
    other = "## Review 1 of PREREG v0 (0badc0de) 2026-11-18: FAIL\n\n"
    vectors = [("RL-90", None, None, None, []),
               ("RL-91", "deadbeef", None, None, ["FROZEN_DIGEST_MISSING:research/experiments/RL-91:deadbeef",
                                                 "PENDING_PIN_MISMATCH:research/experiments/RL-91"]),
               ("RL-92", None, "RESULTS.json", None, ["PENDING_STRAY_FILE:research/experiments/RL-92/RESULTS.json"]),
               ("RL-93", None, None, "# Review of {D}\n\nVERDICT: FAIL\n", not_pass("RL-93")),
               ("RL-94", None, None, "# Review of {D}\n\nVERDICT: FAIL\n\nSecond pass.\n\nVERDICT: PASS\n", []),
               ("RL-95", None, None, "## Review 1 of PREREG v1 ({D}) 2026-11-18: FAIL\n\ntext\n", not_pass("RL-95")),
               ("RL-96", None, None, other + "VERDICT: FAIL\n", not_pass("RL-96")),
               ("RL-97", None, None, "# Review of {D}\n\n**VERDICT: FAIL**\n", not_pass("RL-97")),
               ("RL-98", None, None, "# Review of {D}\n\nverdict: FAIL\n", not_pass("RL-98")),
               ("RL-99", None, None, "# Review of {D}\n\nverdict: CHANGES_REQUIRED\n", not_pass("RL-99")),
               ("RL-100", None, None, "## Review 1 of PREREG v1 ({D}) 2026-11-18 FAIL\n\ntext\n", not_pass("RL-100")),
               ("RL-101", None, None, "# Notes on {D}\n\nno verdict yet\n", not_pass("RL-101")),
               ("RL-102", None, None, other + "Review of {D}\n\nVERDICT: FAIL\n", not_pass("RL-102")),
               ("RL-103", None, None, "## Review 1 of PREREG v1 ({D}) 2026-11-18: PASS\n\nVERDICT: FAIL\n", []),
               ("RL-104", None, None, "# Review\n\nVERDICT: FAIL\n\nVERDICT: PASS\n", not_pass("RL-104")),
               ("RL-105", None, None, "# Review\n\nVERDICT: PASS\n\nVERDICT: FAIL\n", not_pass("RL-105")),
               ("RL-106", None, None, None, ["PENDING_DIGEST_MISMATCH:research/experiments/RL-106"]),
               ("RL-107", None, None, "## Review 1 of PREREG v1 ({D}) 2026-11-18: PASS\n\n" + other, []),
               ("RL-108", None, None, other + "Review of {D}\n\nVERDICT: PASS\n", not_pass("RL-108")),
               ("RL-109", None, None, "# Review\n\nverdict: CHANGES_REQUIRED\n", not_pass("RL-109")),
               ("RL-110", None, None, other, not_pass("RL-110")),
               ("RL-111", None, None, "# Review of {D}\n\nVERDICT: PASS\n", [])]
    assert len(vectors) == 22 and len({v[0] for v in vectors}) == 22
    failures = 0
    for name, pin, stray, review, expected in vectors:
        with tempfile.TemporaryDirectory(prefix="prereg-selftest-") as tmp:
            root = Path(tmp)
            folder = root / "research" / "experiments" / name
            folder.mkdir(parents=True)
            (folder / "PREREG.md").write_text(body, encoding="utf-8")
            digest = sha256(folder / "PREREG.md")
            recorded = digest if name != "RL-106" else "0" * 64  # RL-106: the outcome record names another digest
            outcome = {"schemaVersion": "planeon.research.experiment-outcome/v1", "experiment": name,
                       "attempts": [{"attempt": 1, "outcome": "PENDING", "stageReached": "REVIEW",
                                     "preregDigest": {"sha256": recorded, "prefix": recorded[:8]}}]}
            (folder / "OUTCOME.json").write_text(json.dumps(outcome, indent=1, sort_keys=True), encoding="utf-8")
            if stray:
                (folder / stray).write_text("{}", encoding="utf-8")
            if review:
                (folder / "PREREG-REVIEW.md").write_text(review.replace("{D}", digest[:8]), encoding="utf-8")
            register = root / "research" / "hypotheses" / "REGISTER.md"
            register.parent.mkdir(parents=True)
            register.write_text("# register\n\n## Experiments started\n\n| id | h | folder | state | sha256 (frozen) | effort | notes |\n"
                                "|---|---|---|---|---|---|---|\n| %s | H-00 | `experiments/%s/` | FROZEN | v1 %s | n/r | none |\n"
                                % (name, name, pin or digest[:8]), encoding="utf-8")
            problems = check_tree(register, folder.parent)[0]
            if sorted(problems) != sorted(expected):
                failures += 1
                print("SELFTEST VECTOR %s: got %s, expected %s" % (name, sorted(problems), sorted(expected)))
    if failures:
        print("SELFTEST FAIL: %d of %d vectors" % (failures, len(vectors)))
        return 1
    print("SELFTEST OK: %d vectors" % len(vectors))
    return 0


def main(argv: list) -> int:
    if argv == ["--self-test"]:
        return self_test()
    if len(argv) != 2:
        print("usage: prereg_check.py REGISTER_MD EXPERIMENTS_DIR | --self-test")
        return 2
    register, exp_dir = Path(argv[0]).resolve(), Path(argv[1]).resolve()
    problems, folders, pending, reviewed, records = check_tree(register, exp_dir)
    if problems:
        for line in problems:
            print(line)
        print("PREREG FAIL: %d problems" % len(problems))
        return 1
    print("PREREG OK: %d folders (%d pending), %d reviewed, %d records" % (folders, pending, reviewed, records))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
