"""RL-10 (PREREG v1): the evidence algebra checks over the ledger and native-profile v4 records and vectors.
usage: python3 -I -B rl10_algebra.py EXPORT_ARCH OUT.json"""
import json
import re
import sys
from pathlib import Path

LEVEL = {"ESTABLISHING": 5, "PROOF_BOUND": 4, "CONSISTENCY_ONLY": 3, "NOT_CONFIRMATION": 2, "NOT_EVIDENCE": 1, "OUT_OF_SCOPE": 0}
LEDGER = {k: "ESTABLISHING" for k in ("TEST_RESULT", "REPRODUCER", "SCHEMA_RESULT", "POLICY_RESULT", "ARTIFACT", "TRACE", "DIFF", "ENVIRONMENT_STATE", "DOCUMENT_EXTRACT")}
LEDGER.update({"RESOLVER_REPORT": "PROOF_BOUND", "CHALLENGER_REPORT": "PROOF_BOUND", "VERIFIER_REPORT": "PROOF_BOUND", "REGRESSION_RUN": "CONSISTENCY_ONLY",
               "ROLLOUT_AGREEMENT": "NOT_CONFIRMATION", "POOL_RECOMPUTATION": "NOT_CONFIRMATION", "MODEL_CONFIDENCE": "NOT_EVIDENCE", "SELF_REPORTED_STATUS": "NOT_EVIDENCE"})
NATIVE = {"OBSERVED": "ESTABLISHING", "LABEL_BOUND": "PROOF_BOUND", "ENTRY_BOUND": "PROOF_BOUND", "DECLARED_T04": "PROOF_BOUND", "CONSISTENCY_ONLY": "CONSISTENCY_ONLY", "OUT_OF_SCOPE_HOST": "OUT_OF_SCOPE"}
CODE_LEVEL = {"CONSISTENCY_ONLY": 3, "CONSENSUS_ONLY": 2, "NOT_EVIDENCE": 1}


def main(arch, out_path):
    arch = Path(arch)
    ck = json.loads((arch / "verdict-ledger/check-kinds.json").read_text())
    lv = json.loads((arch / "verdict-ledger/vectors.json").read_text())
    sch = json.loads((arch / "native-profile-v4/qualification.schema.json").read_text())
    nv = json.loads((arch / "native-profile-v4/vectors.json").read_text())
    # C1 totality
    ledger_vocab = set(ck["evidenceKinds"]) | set(ck["notEvidence"])
    native_vocab = set(sch["$defs"]["evidenceClasses"]["const"]["classes"])
    c1 = {"ledger_unmapped": sorted(ledger_vocab - set(LEDGER)), "ledger_extra_in_map": sorted(set(LEDGER) - ledger_vocab), "native_unmapped": sorted(native_vocab - set(NATIVE)), "native_extra_in_map": sorted(set(NATIVE) - native_vocab),
          "consistencyOnly_list": ck["consistencyOnly"], "notConfirmation_list": ck["notConfirmation"], "notEvidence_list": ck["notEvidence"],
          "lists_agree": set(ck["consistencyOnly"]) == {k for k, v in LEDGER.items() if v == "CONSISTENCY_ONLY"} and set(ck["notConfirmation"]) == {k for k, v in LEDGER.items() if v == "NOT_CONFIRMATION"} and set(ck["notEvidence"]) == {k for k, v in LEDGER.items() if v == "NOT_EVIDENCE"}}
    c1["ok"] = not (c1["ledger_unmapped"] or c1["ledger_extra_in_map"] or c1["native_unmapped"] or c1["native_extra_in_map"]) and c1["lists_agree"]
    # C2 ledger agreement
    rows = []
    for x in lv["ledgers"]:
        code = x.get("expect")
        if code not in CODE_LEVEL:
            continue
        led = x["ledger"]; kinds = [e.get("kind") for e in led.get("evidence", []) if isinstance(e, dict)]
        levels = [LEVEL.get(LEDGER.get(k, ""), None) for k in kinds]
        has_level = CODE_LEVEL[code] in levels
        ev_by_id = {e.get("evidenceId"): e.get("kind") for e in led.get("evidence", []) if isinstance(e, dict)}
        deciding = [c for c in led.get("checks", []) if isinstance(c, dict) and str(c.get("kind", "")).startswith("DETERMINISTIC") and c.get("target") == "DELIVERED" and c.get("outcome") == "PASS"
                    and all(LEDGER.get(ev_by_id.get(r, ""), "") == "ESTABLISHING" for r in c.get("evidence", [])) and c.get("evidence")]
        rows.append({"id": x["id"], "code": code, "kinds": sorted(set(k for k in kinds if k)), "has_code_level_kind": has_level, "establishing_deciding_checks": len(deciding)})
    c2 = {"vectors": len(rows), "violations": [r for r in rows if not r["has_code_level_kind"]], "with_establishing_deciding_check": [r["id"] for r in rows if r["establishing_deciding_checks"]], "rows": rows}
    c2["ok"] = not c2["violations"]
    # C3 native agreement
    pat = re.compile(r"LABEL_BOUND capture where OBSERVED is required|OBSERVED field missing from the capture|field forbidden in a LABEL_BOUND capture")
    nrows = []
    for x in nv["negative"]:
        ref = str(x.get("refusal", ""))
        if not pat.search(ref):
            continue
        if "where OBSERVED is required" in ref:
            offered, required = "LABEL_BOUND", "OBSERVED"
        elif "OBSERVED field missing" in ref:
            offered, required = None, "OBSERVED"
        else:
            offered, required = "OBSERVED", "LABEL_BOUND"  # an OBSERVED-only field offered in a LABEL_BOUND role's capture: above the role's ceiling
        lo, lr = (LEVEL[NATIVE[offered]] if offered else None), LEVEL[NATIVE[required]]
        consistent = (lo is None) or (lo < lr) or (lo > lr and "forbidden" in ref)
        nrows.append({"id": x["id"], "refusal": ref, "offered": offered, "required": required, "offered_level": lo, "required_level": lr, "consistent": consistent, "kind": "ceiling" if (lo is not None and lo > lr) else "strictly_below" if lo is not None else "missing_required"})
    c3 = {"vectors": len(nrows), "violations": [r["id"] for r in nrows if not r["consistent"]], "by_kind": {k: sum(1 for r in nrows if r["kind"] == k) for k in ("strictly_below", "missing_required", "ceiling")}, "rows": nrows}
    c3["ok"] = not c3["violations"] and len(nrows) > 0
    out = {"C1": c1, "C2": c2, "C3": c3, "asymmetries": {"OUT_OF_SCOPE_ledger_counterpart": None, "PROOF_BOUND_native_classes": [k for k, v in NATIVE.items() if v == "PROOF_BOUND"], "NOT_CONFIRMATION_native_counterpart": None},
           "ledger_vectors": len(lv["ledgers"]), "native_negatives": len(nv["negative"]), "gate": "PASS" if (c1["ok"] and c2["ok"] and c3["ok"]) else "FAIL"}
    Path(out_path).write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print("C1", {k: v for k, v in c1.items()}); print("C2", {k: v for k, v in c2.items() if k != "rows"}); print("C3", {k: v for k, v in c3.items() if k != "rows"}); print("gate", out["gate"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
