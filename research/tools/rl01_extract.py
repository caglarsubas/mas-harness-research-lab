"""RL-01 allowlist extractor: reads merge-decision records and prints only numeric / enum columns.
usage: python3 -I -B rl01_extract.py RECORD_DIR > rows.tsv
Never prints any string field other than the enum `conclusion`; repository, approver and paths are never read into
the output. Dates are kept as YYYY-MM-DD only."""
import json
import pathlib
import re
import sys

ENUM = re.compile(r"^[A-Za-z_]{1,24}$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
SLOT = re.compile(r"\b(2[0-9]{2}|3[0-9]{2})\b")


def num(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else ""


def enum(value):
    return value if isinstance(value, str) and ENUM.match(value) else ""


def date(value):
    match = DATE.match(value) if isinstance(value, str) else None
    return match.group(0) if match else ""


def slot_of(record):
    """The slot number: the record's `slot` when numeric, else the first 3-digit number 200-399 in the packet name."""
    if isinstance(record.get("slot"), int):
        return record["slot"]
    match = SLOT.search(record.get("packet", "")) if isinstance(record.get("packet"), str) else None
    return int(match.group(1)) if match else ""


def main(record_dir):
    print("\t".join(["file_date", "pr", "slot", "elapsed_s", "load_mean", "test_count", "conclusion", "decided_date"]))
    for path in sorted(pathlib.Path(record_dir).glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        verify = record.get("verify", {}) if isinstance(record.get("verify"), dict) else {}
        tests = verify.get("tests", verify.get("pytest"))
        test_count = num(tests) if not isinstance(tests, dict) else num(tests.get("count", tests.get("passed")))
        print("\t".join(str(x) for x in [
            date(path.name), num(record.get("pr")), slot_of(record), num(verify.get("elapsedSeconds")),
            num(verify.get("loadMean", verify.get("meanLoad"))), test_count, enum(verify.get("conclusion")),
            date(record.get("decidedAt")),
        ]))


if __name__ == "__main__":
    main(sys.argv[1])
