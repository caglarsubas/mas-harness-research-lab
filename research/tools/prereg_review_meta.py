#!/usr/bin/env python3
"""Meta-review of the lab's blind PREREG reviews (charter step 1a).

Parses every experiments/RL-*/PREREG-REVIEW.md into review rounds (version, digest prefix, date, verdict, R1-R7
outcomes, note count) and finding keys (one per criterion FAIL, one per numbered note, one per declared pre-run
stop), then checks a curated data file against that parse and renders summary tables.

  python3 -I -B prereg_review_meta.py --init OUT.json      write the parsed skeleton (themes and dispositions empty)
  python3 -I -B prereg_review_meta.py --check DATA.json    re-parse and compare; exit 1 on any difference
  python3 -I -B prereg_review_meta.py --render DATA.json OUT.md   check, then write the tables

The tool reads the review files only; it prints ids, counts, digest prefixes and dates, never review prose.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments"

HEAD = re.compile(r"^## Review (\d+), of PREREG v(\d+) \(([0-9a-f]{8})\), (\d{4}-\d{2}-\d{2}): (PASS|FAIL)", re.MULTILINE)
HEAD_B = re.compile(r"Review (\d+) of PREREG v(\d+) \(([0-9a-f]{8})\)")
TITLE_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")
CRIT = re.compile(r"\bR([1-7]):?\s+(PASS|FAIL)")
ALLPASS = re.compile(r"\bR1-R7 PASS")
NOTE_MARK = re.compile(r"\((\d+)\)")
NOTE_LINE = re.compile(r"^(\d+)\. ")

THEMES = {
    "T1": "GATE: regions overlap, precedence unstated, a statistic or region undefined for some outcome",
    "T2": "SCOPE: the unit measured differs from the register's clause without a declared narrowing or proxy",
    "T3": "PIN: an input, instrument, constant or source without a full digest, a commit or a stated origin",
    "T4": "INSTRUMENT: detection or attribution validity, crash classes, boundary and edge cases, targets that do not exist or quantities that cannot be computed",
    "T5": "ANALYSIS: interval width, clustering, ties, resamples, sensitivity, k, the expected outcome class",
    "T6": "DESIGN VALIDITY: researcher degrees of freedom, prior knowledge of the data or comparator, shared authorship, foregone verdicts, confounds",
    "T7": "REPORT: what the report or run record must say (sub-case, counts, proxies, operationalisation, limits)",
    "T8": "PROCESS: status and procedure consistency (frozen before review, GO wording, register entries)",
}
SEVERITIES = ("BLOCKING", "NOTE", "STOP")
DISPOSITIONS = (
    "ANSWERED_NEXT_VERSION",      # a new PREREG version answered it before the run
    "ANSWERED_IN_REPORT",         # answered in the run record or the report under the frozen PREREG
    "ANSWERED_IN_REGISTER",       # answered by the register row's wording
    "DONE_AFTER_REVIEW",          # an artefact added after the review without a version (preflight addendum, a non-gating run)
    "ADOPTED_WITHOUT_VERSION",    # a rule applied to the run without a new version (a protocol slip, recorded as such)
    "DEFERRED_NEXT_PREREG",       # carried to the next PREREG that reuses the form
)
DETECTORS = ("REVIEW", "LAB")


def parse_file(path):
    text = path.read_text(encoding="utf-8")
    exp = path.parent.name
    rounds = []
    if exp == "RL-15b":
        m = HEAD_B.search(text)
        date = TITLE_DATE.search(text.splitlines()[0]).group(1)
        verdict = "PASS" if "VERDICT: PASS" in text else "FAIL"
        body = text.split("## The lab's handling")[0]
        notes = [int(x.group(1)) for x in (NOTE_LINE.match(l) for l in body.split("NOTES:")[1].splitlines()) if x]
        outcomes = {f"R{k}": v for k, v in CRIT.findall(body)}
        rounds.append(_round(exp, m, date, verdict, outcomes, notes, body, True))
        return rounds, _stops(exp, text)
    heads = list(HEAD.finditer(text))
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[h.start():end]
        core = body.split("Lab's disposition")[0]
        outcomes = {}
        if ALLPASS.search(core):
            outcomes = {f"R{k}": "PASS" for k in range(1, 8)}
        for k, v in CRIT.findall(core):
            outcomes.setdefault(f"R{k}", v)
        notes_text = core.split("NOTES:")[1] if "NOTES:" in core else ""
        marks = [int(x) for x in NOTE_MARK.findall(notes_text)]
        notes = []
        for x in marks:
            if x == len(notes) + 1:
                notes.append(x)
        rounds.append(_round(exp, h, h.group(4), h.group(5), outcomes, notes, body, "Lab's disposition" in body))
    return rounds, _stops(exp, text)


def _round(exp, m, date, verdict, outcomes, notes, body, has_disposition):
    missing = [f"R{k}" for k in range(1, 8) if f"R{k}" not in outcomes]
    if missing:
        raise SystemExit(f"{exp} review {m.group(1)}: criteria without an outcome: {missing}")
    return {
        "experiment": exp,
        "round": int(m.group(1)),
        "version": int(m.group(2)),
        "digest": m.group(3),
        "date": date,
        "verdict": verdict,
        "outcomes": {f"R{k}": outcomes[f"R{k}"] for k in range(1, 8)},
        "noteCount": len(notes),
        "hasDisposition": bool(has_disposition),
    }


STOP_ANCHORS = {
    "RL-15": "## Instrument stop before any seeded build",
    "RL-21": "the lab's own inventory showed",
}


def _stops(exp, text):
    a = STOP_ANCHORS.get(exp)
    return [{"experiment": exp, "anchor": a}] if a and a in text else []


def parse_all():
    rounds, stops = [], []
    for p in sorted(EXP.glob("RL-*/PREREG-REVIEW.md"), key=lambda q: (len(q.parent.name), q.parent.name)):
        r, s = parse_file(p)
        rounds += r
        stops += s
    return rounds, stops


def finding_keys(rounds, stops):
    keys = []
    for r in rounds:
        base = f"{r['experiment']}/r{r['round']}"
        for k in range(1, 8):
            if r["outcomes"][f"R{k}"] == "FAIL":
                keys.append((f"{base}/R{k}", "BLOCKING", r["round"]))
        for n in range(1, r["noteCount"] + 1):
            keys.append((f"{base}/N{n}", "NOTE", r["round"]))
    for s in stops:
        keys.append((f"{s['experiment']}/stop", "STOP", None))
    return keys


def skeleton():
    rounds, stops = parse_all()
    findings = []
    for key, sev, rnd in finding_keys(rounds, stops):
        findings.append({"findingId": key, "experiment": key.split("/")[0], "round": rnd, "severity": sev,
                         "blocks": sev != "NOTE", "criterion": key.split("/")[-1] if sev == "BLOCKING" else None,
                         "theme": "", "detector": "REVIEW" if sev != "STOP" else "LAB", "disposition": "",
                         "gist": ""})
    return {"schema": "planeon.research.prereg-review-meta/v1", "themes": THEMES, "rounds": rounds,
            "stops": stops, "findings": findings}


def check(doc):
    problems = []
    rounds, stops = parse_all()
    if doc.get("rounds") != rounds:
        problems.append("ROUNDS differ from the parse")
    if doc.get("stops") != stops:
        problems.append("STOPS differ from the parse")
    want = {k for k, _, _ in finding_keys(rounds, stops)}
    have = [f["findingId"] for f in doc.get("findings", [])]
    if len(have) != len(set(have)):
        problems.append("DUPLICATE finding ids")
    if set(have) != want:
        problems.append(f"FINDING KEYS differ: missing {sorted(want - set(have))}, extra {sorted(set(have) - want)}")
    sev_by_key = {k: s for k, s, _ in finding_keys(rounds, stops)}
    for f in doc.get("findings", []):
        if f.get("theme") not in THEMES:
            problems.append(f"{f['findingId']}: THEME {f.get('theme')!r}")
        if f.get("disposition") not in DISPOSITIONS:
            problems.append(f"{f['findingId']}: DISPOSITION {f.get('disposition')!r}")
        if f.get("severity") != sev_by_key.get(f["findingId"]):
            problems.append(f"{f['findingId']}: SEVERITY")
        if f.get("detector") not in DETECTORS:
            problems.append(f"{f['findingId']}: DETECTOR")
        if not f.get("gist"):
            problems.append(f"{f['findingId']}: EMPTY gist")
        if f.get("blocks") != (f.get("severity") != "NOTE"):
            problems.append(f"{f['findingId']}: BLOCKS")
    return problems


def tables(doc):
    rounds, findings = doc["rounds"], doc["findings"]
    exps = []
    for r in rounds:
        if r["experiment"] not in exps:
            exps.append(r["experiment"])
    out = ["# PREREG review meta-review 001: tables (generated by `tools/prereg_review_meta.py --render`)", ""]
    out.append(f"Rounds {len(rounds)} over {len(exps)} reviewed experiments; FAIL rounds "
               f"{sum(r['verdict'] == 'FAIL' for r in rounds)}; findings {len(findings)} "
               f"(blocking {sum(f['severity'] == 'BLOCKING' for f in findings)}, notes "
               f"{sum(f['severity'] == 'NOTE' for f in findings)}, pre-run stops {sum(f['severity'] == 'STOP' for f in findings)}).")
    out += ["", "## Rounds per experiment", "", "| experiment | date(s) | rounds | verdicts in order | first-round verdict | blocking findings | notes | pre-run stop |",
            "|---|---|---|---|---|---|---|---|"]
    for e in exps:
        rs = [r for r in rounds if r["experiment"] == e]
        fs = [f for f in findings if f["experiment"] == e]
        dates = sorted({r["date"] for r in rs})
        out.append(f"| {e} | {', '.join(dates)} | {len(rs)} | {' '.join(r['verdict'] for r in rs)} | {rs[0]['verdict']} | "
                   f"{sum(f['severity'] == 'BLOCKING' for f in fs)} | {sum(f['severity'] == 'NOTE' for f in fs)} | "
                   f"{'yes' if any(f['severity'] == 'STOP' for f in fs) else 'no'} |")
    out += ["", "## Blocking findings by criterion", "", "| criterion | FAIL count | rounds |", "|---|---|---|"]
    for k in range(1, 8):
        rs = [f"{r['experiment']} r{r['round']}" for r in rounds if r["outcomes"][f"R{k}"] == "FAIL"]
        out.append(f"| R{k} | {len(rs)} | {', '.join(rs) if rs else '-'} |")
    out += ["", "## Notes per round", "", "| notes returned | rounds |", "|---|---|"]
    for n in sorted({r["noteCount"] for r in rounds}):
        out.append(f"| {n} | {sum(r['noteCount'] == n for r in rounds)} |")
    out += ["", "## Findings by theme", "", "| theme | blocking | notes | stops | total | experiments | first seen |", "|---|---|---|---|---|---|---|"]
    for t, name in doc["themes"].items():
        fs = [f for f in findings if f["theme"] == t]
        first = min((f for f in fs), key=lambda f: (exps.index(f["experiment"]), f["round"] or 99), default=None)
        out.append(f"| {t} {name.split(':')[0]} | {sum(f['severity'] == 'BLOCKING' for f in fs)} | {sum(f['severity'] == 'NOTE' for f in fs)} | "
                   f"{sum(f['severity'] == 'STOP' for f in fs)} | {len(fs)} | {len({f['experiment'] for f in fs})} | "
                   f"{first['findingId'] if first else '-'} |")
    out += ["", "## Dispositions", "", "| disposition | blocking | notes | stops |", "|---|---|---|---|"]
    for d in DISPOSITIONS:
        fs = [f for f in findings if f["disposition"] == d]
        out.append(f"| {d} | {sum(f['severity'] == 'BLOCKING' for f in fs)} | {sum(f['severity'] == 'NOTE' for f in fs)} | {sum(f['severity'] == 'STOP' for f in fs)} |")
    out += ["", "## Every finding", "", "| findingId | severity | theme | detector | disposition | gist |", "|---|---|---|---|---|---|"]
    for f in findings:
        out.append(f"| {f['findingId']} | {f['severity']} | {f['theme']} | {f['detector']} | {f['disposition']} | {f['gist']} |")
    return "\n".join(out) + "\n"


def main(argv):
    if len(argv) >= 2 and argv[0] == "--init":
        Path(argv[1]).write_text(json.dumps(skeleton(), indent=2) + "\n", encoding="utf-8")
        print(f"skeleton written: {len(skeleton()['findings'])} findings")
        return 0
    if len(argv) >= 2 and argv[0] in ("--check", "--render"):
        doc = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        problems = check(doc)
        for p in problems:
            print("PROBLEM:", p)
        if problems:
            return 1
        if argv[0] == "--render":
            Path(argv[2]).write_text(tables(doc), encoding="utf-8")
            print(f"tables written: {argv[2]}")
        print(f"META-REVIEW OK: {len(doc['rounds'])} rounds, {len(doc['findings'])} findings")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
