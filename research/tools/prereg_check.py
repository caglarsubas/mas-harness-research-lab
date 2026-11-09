"""Preregistration and review-record check (LAB-REPO-001): every experiment folder holds a frozen PREREG, its ledger and
its report; every frozen digest the register names resolves to a PREREG file; from RL-14 the blind review names the
run version and reads PASS and the ledger names its evaluator; review records match planeon.review-record/v2.
Counts only on stdout; problem lines are CODE:path. Standard library.

usage: python3 -I -B research/tools/prereg_check.py REGISTER_MD EXPERIMENTS_DIR
"""
import hashlib
import json
import re
import sys
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


def main(argv: list) -> int:
    if len(argv) != 2:
        print("usage: prereg_check.py REGISTER_MD EXPERIMENTS_DIR")
        return 2
    register, exp_dir = Path(argv[0]).resolve(), Path(argv[1]).resolve()
    root = exp_dir.parent.parent
    tools_dir = root / "research" / "tools"
    tool_digests = {sha256(p) for p in sorted(tools_dir.glob("*.py"))} if tools_dir.is_dir() else set()
    rows = register_rows(register)
    problems, folders, reviewed = [], 0, 0
    for folder in sorted(p for p in exp_dir.glob("RL-*") if p.is_dir()):
        folders += 1
        name = folder.name
        rel = folder.relative_to(root).as_posix()
        preregs = {sha256(p): p for p in sorted(folder.glob("PREREG*.md")) if p.name != "PREREG-REVIEW.md"}
        if not preregs:
            problems.append("PREREG_MISSING:" + rel)
        ledger, report = folder / "RESULTS.json", folder / "REPORT.md"
        if not ledger.is_file():
            problems.append("LEDGER_MISSING:" + rel)
        if not report.is_file():
            problems.append("REPORT_MISSING:" + rel)
        if name not in rows:
            problems.append("REGISTER_ROW_MISSING:" + rel)
        else:
            prefixes = {d[:8] for d in preregs}
            for token in HEX8.findall(rows[name][4]):
                if token not in prefixes:
                    problems.append("FROZEN_DIGEST_MISSING:%s:%s" % (rel, token))
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
    if problems:
        for line in problems:
            print(line)
        print("PREREG FAIL: %d problems" % len(problems))
        return 1
    print("PREREG OK: %d folders, %d reviewed, %d records" % (folders, reviewed, records))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
