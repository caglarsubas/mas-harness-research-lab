#!/usr/bin/env python3
"""Check research/hypotheses/CLAIMS.json against the verdict ledgers, and render CLAIMS.md from it.

Usage:
  python3 -I -B research/tools/claims_check.py research/hypotheses/CLAIMS.json            # check only
  python3 -I -B research/tools/claims_check.py research/hypotheses/CLAIMS.json --render   # check, then write CLAIMS.md

The claims table is a read-only companion of the ledgers (R13 issue 1, recommendation 1): every row names one
claim of one RESULTS.json and copies its verdict; the table never changes a ledger. The check fails when a row's
verdict or status differs from the ledger, when a ledger claim has no row or a row names no ledger claim, when an
enumeration value is unknown, or when a required field is empty. Standard library only; reads the tree, writes
only CLAIMS.md under --render.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA = "planeon.research.claims/v1"
VERDICTS = {"SUPPORTED", "CONTRADICTED", "UNRESOLVED", "NEW_VALUE_ESTABLISHED"}
STATUSES = {"PASS", "FAIL", "UNRESOLVED"}
EVIDENCE_TYPES = {"simulation", "documentary", "empirical", "formal"}
REPLICATION = {"RECORDED", "LEDGER_REDERIVED", "RAW_REPRODUCED", "INDEPENDENT_REPLICATION"}
INSTRUMENT = {"VALID", "VALID_WITH_LIMITS", "UNDERPOWERED", "INVALID", "NONE", "DESCRIPTIVE"}
REQUIRED = ("experiment", "claimId", "hypothesis", "ledgerId", "ledgerStatus", "claimVerdict", "testedClause",
            "measured", "checks", "unresolvedChecks", "operationalDefinition", "instrumentValidity",
            "instrumentNote", "supportedScope", "unresolvedClauses", "evidenceType", "evidenceMethod",
            "replicationState", "invalidCases", "decision")


def ledgers(root: Path) -> dict[tuple[str, str], dict]:
    out = {}
    for folder in sorted((root / "research" / "experiments").glob("RL-*")):
        path = folder / "RESULTS.json"
        if not path.is_file():
            continue
        j = json.loads(path.read_text(encoding="utf-8"))
        for cv in j["claimVerdicts"]:
            out[(folder.name, cv["claimId"])] = {"ledgerId": j["ledgerId"], "status": j["verdict"]["status"],
                                                "verdict": cv["verdict"], "checks": list(cv["checks"]),
                                                "unresolved": list(j["verdict"].get("unresolvedChecks", []))}
    return out


def check(doc: dict, led: dict) -> list[str]:
    problems = []
    if doc.get("schemaVersion") != SCHEMA:
        problems.append("SCHEMA: %r" % doc.get("schemaVersion"))
    rows = doc.get("claims")
    if not isinstance(rows, list) or not rows:
        return problems + ["CLAIMS: missing or empty"]
    seen = set()
    for i, r in enumerate(rows):
        key = (r.get("experiment"), r.get("claimId"))
        tag = "%s/%s" % key
        for f in REQUIRED:
            v = r.get(f)
            if v is None or v == "" or (isinstance(v, list) and f in ("checks",) and not v):
                problems.append("EMPTY: %s %s" % (tag, f))
        if key in seen:
            problems.append("DUPLICATE: %s" % tag)
        seen.add(key)
        L = led.get(key)
        if L is None:
            problems.append("NO_LEDGER_CLAIM: %s" % tag)
            continue
        if r.get("claimVerdict") != L["verdict"]:
            problems.append("VERDICT: %s row %s ledger %s" % (tag, r.get("claimVerdict"), L["verdict"]))
        if r.get("ledgerStatus") != L["status"]:
            problems.append("STATUS: %s row %s ledger %s" % (tag, r.get("ledgerStatus"), L["status"]))
        if r.get("ledgerId") != L["ledgerId"]:
            problems.append("LEDGER_ID: %s" % tag)
        if sorted(r.get("checks") or []) != sorted(L["checks"]):
            problems.append("CHECKS: %s" % tag)
        if sorted(r.get("unresolvedChecks") or []) != sorted(c for c in L["unresolved"] if c in L["checks"]):
            problems.append("UNRESOLVED_CHECKS: %s row %s ledger %s" % (tag, r.get("unresolvedChecks"), L["unresolved"]))
        if r.get("claimVerdict") not in VERDICTS:
            problems.append("ENUM verdict: %s" % tag)
        if r.get("evidenceType") not in EVIDENCE_TYPES:
            problems.append("ENUM evidenceType: %s %r" % (tag, r.get("evidenceType")))
        if r.get("replicationState") not in REPLICATION:
            problems.append("ENUM replicationState: %s %r" % (tag, r.get("replicationState")))
        if r.get("instrumentValidity") not in INSTRUMENT:
            problems.append("ENUM instrumentValidity: %s %r" % (tag, r.get("instrumentValidity")))
        if not isinstance(r.get("invalidCases"), list):
            problems.append("SHAPE invalidCases: %s" % tag)
    for key in led:
        if key not in seen:
            problems.append("NO_ROW: %s/%s" % key)
    return problems


def render(doc: dict) -> str:
    rows = doc["claims"]
    out = ["# Claims table (generated from CLAIMS.json by research/tools/claims_check.py --render; do not edit by hand)",
           "",
           doc.get("preamble", "").strip(),
           "",
           "Columns: the ledger's claim and verdict (copied, never changed); what was operationally measured; whether the",
           "instrument could answer the clause (VALID, VALID_WITH_LIMITS, UNDERPOWERED, INVALID, NONE, DESCRIPTIVE); the",
           "scope the verdict supports; the clauses it leaves open; evidence type (simulation, documentary, empirical,",
           "formal) and method; replication state (RECORDED, LEDGER_REDERIVED, RAW_REPRODUCED, INDEPENDENT_REPLICATION);",
           "invalid cases recorded beside the verdict; the decision the verdict justifies.",
           ""]
    by_exp: dict[str, list[dict]] = {}
    for r in rows:
        by_exp.setdefault(r["experiment"], []).append(r)
    counts = {}
    for r in rows:
        counts[r["claimVerdict"]] = counts.get(r["claimVerdict"], 0) + 1
    out.append("Rows: %d claims over %d experiments; verdicts %s; replication %s." % (
        len(rows), len(by_exp), ", ".join("%s %d" % kv for kv in sorted(counts.items())),
        ", ".join("%s %d" % (k, sum(1 for r in rows if r["replicationState"] == k)) for k in sorted({r["replicationState"] for r in rows}))))
    out.append("")
    for exp in sorted(by_exp):
        rs = by_exp[exp]
        out.append("## %s (%s, ledger status %s, %s)" % (exp, rs[0]["ledgerId"], rs[0]["ledgerStatus"], rs[0]["hypothesis"]))
        out.append("")
        for r in rs:
            out.append("### %s: %s" % (r["claimId"], r["claimVerdict"]))
            out.append("")
            out.append("- Tested clause: %s" % r["testedClause"])
            out.append("- Measured: %s" % r["measured"])
            out.append("- Operational definition: %s" % r["operationalDefinition"])
            out.append("- Instrument: %s. %s" % (r["instrumentValidity"], r["instrumentNote"]))
            out.append("- Supported scope: %s" % r["supportedScope"])
            out.append("- Unresolved clauses: %s (ledger checks %s)" % (r["unresolvedClauses"], ", ".join(r["unresolvedChecks"]) or "none"))
            out.append("- Evidence: %s; %s" % (r["evidenceType"], r["evidenceMethod"]))
            out.append("- Replication: %s" % r["replicationState"])
            if r["invalidCases"]:
                out.append("- Invalid cases: " + "; ".join("%s: %s" % (c["id"], c["note"]) for c in r["invalidCases"]))
            out.append("- Decision justified: %s" % r["decision"])
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 2
    path = Path(argv[1])
    root = path.resolve().parents[2]
    doc = json.loads(path.read_text(encoding="utf-8"))
    problems = check(doc, ledgers(root))
    for p in problems:
        print(p)
    if problems:
        print("CLAIMS FAIL: %d problem(s)" % len(problems))
        return 1
    print("CLAIMS OK: %d claims over %d experiments" % (len(doc["claims"]), len({r["experiment"] for r in doc["claims"]})))
    if "--render" in argv[2:]:
        out = path.with_name("CLAIMS.md")
        out.write_text(render(doc), encoding="utf-8")
        print("CLAIMS.md written: %s" % out.resolve().relative_to(root))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
