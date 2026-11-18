"""E1 joint-cause control (R13 issue 6, 2026-11-14): the 2x2 control over the declared edits versus the other changed
inputs that the isolation check E1 (research/reads/CONTRACT-286-QC2-LAB-READ.md section 2, superseded by the V2 read)
lacks. E1 restores the changed declared inputs and keeps the rest of the live tree ("other-only" cell) and credits the
event as explained when that cell returns the recorded outcome. A cause that needs a declared edit AND an undeclared
input together returns the recorded outcome in that cell, so E1 credits it although the undeclared input changes the
live outcome. The missing cell is "declared-only" (the declared edits applied, every other changed input at its base
bytes): credit needs other-only == recorded AND declared-only == live. Standard library only; no network; no run of
any suite.

usage:
  python3 -I -B e1_control.py selftest
      enumerates every outcome function of (declared edit D, other changed input U) over two outcome words, checks
      that the 2x2 rule credits exactly the functions where U has no effect, counts the functions E1 alone credits
      wrongly, and runs the known-answer cases K1-K7 (the issue's table is K1). Exit 0 on PASS, 1 on FAIL.
  python3 -I -B e1_control.py check CONTROL.json
      CONTROL.json: {"event": <free text>, "nodes": {<nodeId>: {"recorded": P, "declaredOnly": P, "otherOnly": P,
      "live": P}}} where P is a per-phase outcome map {"setup": w, "call": w, "teardown": w} and a cell or phase that
      was not run is null. Prints one line per node and the event verdict: explained (count), unexplained (class A,
      restart) or unresolved (no credit: a cell missing or not comparable), plus what E1 alone would have said.
      Exit 0 on a well-formed file, 2 on a malformed one.
"""
import json
import sys

CELLS = ("recorded", "declaredOnly", "otherOnly", "live")
WORDS = ("passed", "skipped")


def agrees(a, b):
    """True when both per-phase maps exist, name the same phases and every phase word is equal; None when either side is
    missing, has a null phase or the phase sets differ (not comparable); False otherwise. A cell not run never agrees."""
    if not isinstance(a, dict) or not isinstance(b, dict) or not a or set(a) != set(b):
        return None
    if any(not isinstance(a[k], str) or not isinstance(b[k], str) for k in a):
        return None
    return all(a[k] == b[k] for k in a)


def node_verdict(cells):
    """Returns (verdict, e1Verdict, reason). Verdicts: not-differing, unresolved, unexplained-other, unexplained-joint,
    explained. e1Verdict is what the one-cell check alone says: explained, unexplained or None (its cell missing)."""
    differing = agrees(cells.get("live"), cells.get("recorded"))
    other = agrees(cells.get("otherOnly"), cells.get("recorded"))
    decl = agrees(cells.get("declaredOnly"), cells.get("live"))
    e1 = None if other is None else ("explained" if other else "unexplained")
    if differing is None:
        return "unresolved", e1, "recorded or live cell missing or not comparable"
    if differing:
        return "not-differing", e1, "live outcome equals the record; E1 does not apply"
    if other is None:
        return "unresolved", e1, "other-only cell missing or not comparable"
    if decl is None:
        return "unresolved", e1, "declared-only cell missing or not comparable"
    if not other:
        return "unexplained-other", e1, "the other changed inputs alone change the outcome"
    if not decl:
        return "unexplained-joint", e1, "the declared edits alone do not reproduce the live outcome (a joint cause); E1 alone credits this"
    return "explained", e1, "declared edits alone reproduce the live outcome; the other changed inputs alone do not change it"


def event_verdict(nodes):
    rows = {n: node_verdict(c) for n, c in nodes.items()}
    live = {n: r for n, r in rows.items() if r[0] != "not-differing"}
    if not live:
        verdict = "no-change"
    elif any(r[0] == "unresolved" for r in live.values()):
        verdict = "unresolved"
    elif any(r[0].startswith("unexplained") for r in live.values()):
        verdict = "unexplained"
    else:
        verdict = "explained"
    e1s = [r[1] for r in live.values()]
    e1_would_credit = bool(live) and all(e == "explained" for e in e1s)
    return verdict, e1_would_credit, rows


def phases(word, call=None):
    return {"setup": "passed", "call": word if call is None else call, "teardown": "passed"}


def known_answers():
    p, s = "passed", "skipped"
    one = lambda rec, dec, oth, liv: {"n": {"recorded": phases(rec), "declaredOnly": phases(dec), "otherOnly": phases(oth), "live": phases(liv)}}
    cases = [
        ("K1-issue-table-joint-cause", one(p, p, p, s), "unexplained", True, "unexplained-joint"),
        ("K2-declared-only-positive-control", one(p, s, p, s), "explained", True, "explained"),
        ("K3-undeclared-only-cause", one(p, p, s, s), "unexplained", False, "unexplained-other"),
        ("K4-missing-declared-only-cell", {"n": {"recorded": phases(p), "declaredOnly": None, "otherOnly": phases(p), "live": phases(s)}}, "unresolved", True, "unresolved"),
        ("K5-joint-cause-other-polarity", one(s, s, s, p), "unexplained", True, "unexplained-joint"),
        ("K6-phase-sets-differ", {"n": {"recorded": phases(p), "declaredOnly": phases(p), "otherOnly": {"setup": "passed", "call": "passed"}, "live": phases(s)}}, "unresolved", None, "unresolved"),
        ("K7-not-differing", one(p, p, p, p), "no-change", True, "not-differing"),  # E1's own cell agrees, but the node is not an outcome change, so no event credit
    ]
    return cases


def enumerate_functions():
    """Every function f(D, U) -> word over two words; D = the declared edit applied, U = the other changed input live."""
    keys = [(0, 0), (0, 1), (1, 0), (1, 1)]
    out = []
    for i in range(16):
        f = {k: WORDS[(i >> j) & 1] for j, k in enumerate(keys)}
        live_changed = f[(1, 1)] != f[(0, 0)]
        e1_credits = f[(0, 1)] == f[(0, 0)]
        control_credits = e1_credits and f[(1, 0)] == f[(1, 1)]
        u_effect = f[(0, 0)] != f[(0, 1)] or f[(1, 0)] != f[(1, 1)]
        out.append({"f": f, "liveChanged": live_changed, "e1Credits": e1_credits, "controlCredits": control_credits, "uEffect": u_effect})
    return out


def selftest():
    fails = []
    fs = enumerate_functions()
    for r in fs:
        if r["controlCredits"] != (not r["uEffect"]):
            fails.append("enumeration: control credit must equal 'U has no effect' for %s" % r["f"])
    changed = [r for r in fs if r["liveChanged"]]
    e1_wrong = [r for r in changed if r["e1Credits"] and r["uEffect"]]
    e1_right = [r for r in changed if r["e1Credits"] and not r["uEffect"]]
    ctrl_wrong = [r for r in changed if r["controlCredits"] and r["uEffect"]]
    if len(changed) != 8 or len(e1_wrong) != 2 or len(e1_right) != 2 or ctrl_wrong:
        fails.append("enumeration counts: changed %d (8), E1 wrong %d (2), E1 right %d (2), control wrong %d (0)" % (len(changed), len(e1_wrong), len(e1_right), len(ctrl_wrong)))
    issue = {(0, 0): "passed", (0, 1): "passed", (1, 0): "passed", (1, 1): "skipped"}
    if issue not in [r["f"] for r in e1_wrong]:
        fails.append("the issue's table is not among the functions E1 credits wrongly")
    for name, nodes, want, want_e1, want_node in known_answers():
        verdict, e1_credit, rows = event_verdict(nodes)
        got_node = rows["n"][0]
        got_e1 = rows["n"][1] == "explained" if rows["n"][1] is not None else None
        ok = verdict == want and got_node == want_node and got_e1 == want_e1
        print("%-36s event %-11s node %-18s e1WouldCredit %-5s %s" % (name, verdict, got_node, e1_credit, "ok" if ok else "FAIL"))
        if not ok:
            fails.append("%s: got event %s node %s e1 %s, wanted %s %s %s" % (name, verdict, got_node, got_e1, want, want_node, want_e1))
    print("enumeration: 16 functions, 8 with a live outcome change; E1 credits 4 of them, 2 wrongly (a joint cause in either polarity); the 2x2 control credits 2, 0 wrongly")
    print("SELFTEST", "FAIL" if fails else "PASS", len(known_answers()), "known-answer cases")
    for f in fails:
        print("  ", f)
    return 1 if fails else 0


def check(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
        nodes = d["nodes"]
        assert isinstance(nodes, dict) and nodes, "nodes must be a non-empty object"
        for n, c in nodes.items():
            assert isinstance(c, dict) and set(c) == set(CELLS), "node %s must carry exactly the cells %s" % (n, list(CELLS))
    except Exception as e:  # malformed input
        print("MALFORMED", type(e).__name__, str(e)[:200])
        return 2
    verdict, e1_credit, rows = event_verdict(nodes)
    for n, (v, e1, why) in rows.items():
        print("node %s: %s (E1 alone: %s) - %s" % (n, v, e1 or "no cell", why))
    print("EVENT", verdict, "| countEffect", {"explained": "count", "unexplained": "class A, restart", "unresolved": "pending (no credit)", "no-change": "not an outcome change"}[verdict], "| E1 alone would credit:", e1_credit)
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "selftest":
        sys.exit(selftest())
    if len(sys.argv) == 3 and sys.argv[1] == "check":
        sys.exit(check(sys.argv[2]))
    print(__doc__)
    sys.exit(2)
