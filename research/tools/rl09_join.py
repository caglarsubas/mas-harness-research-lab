"""RL-09 (PREREG v1): the documentary allowlist join over the host-interface counterexamples 18-28.
usage: python3 -I -B rl09_join.py EXPORT_ARCH OUT.json   (stdlib; prints per-path coverage; no spec text printed)"""
import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"\b(?:[PASCEI]\d{1,2}|I0\d|v\d|T0\d)\b")
TICK = re.compile(r"`([^`]{2,40})`")
GENERIC = {"W01"}


def counterexamples(spec_lines):
    """Paths 18-28: their line ranges and the token set of their 'Required:' sentences."""
    paths, current = {}, None
    for i, line in enumerate(spec_lines, 1):
        m = re.match(r"^(\d{1,2})\. ", line)
        if m and 18 <= int(m.group(1)) <= 28:
            current = int(m.group(1)); paths[current] = {"start": i, "end": i, "text": line}
        elif current and (line.startswith("    ") or line.startswith("   ")):
            paths[current]["end"] = i; paths[current]["text"] += " " + line.strip()
        elif current and line.strip() == "":
            current = None
        elif current and re.match(r"^(##|\d{1,2}\. )", line):
            current = None
    for n, p in paths.items():
        req = p["text"].split("Required:", 1)[1] if "Required:" in p["text"] else ""
        toks = set(TOKEN.findall(req)) | set(TICK.findall(req))
        p["tokens"] = sorted(t for t in toks if t not in GENERIC); p["has_required"] = "Required:" in p["text"]
        del p["text"]
    return paths


def main(arch, out_path):
    arch = Path(arch)
    spec = (arch / "host-interface-inputs/resolved/HOST_INTERFACE_SPEC.md").read_text(encoding="utf-8").splitlines()
    hs53 = (arch / "host-interface-amendment-hs53/HOST_INTERFACE_SPEC.md").read_text(encoding="utf-8").splitlines()
    paths = counterexamples(spec)
    same = {n: " ".join(spec[p["start"] - 1:p["end"]]) in "\n".join(hs53).replace("\n", " ") or any(spec[p["start"] - 1] == l for l in hs53) for n, p in paths.items()}
    seccomp = json.loads((arch / "seccomp-allowlists-v5/allowlists.json").read_text())
    matrix = json.loads((arch / "selinux-matrix-v4/matrix.json").read_text())
    amend = {k: json.loads((arch / ("host-interface-amendment-%s/amendment.json" % k)).read_text()) for k in ("hs53", "he5")}
    residual_text = " ".join(json.dumps(a["residuals"]) for a in amend.values())
    sec63 = [i for i, l in enumerate(spec, 1) if l.startswith("### 6.3")]; sec8 = [i for i, l in enumerate(spec, 1) if l.startswith("## 8.")]
    for start in sec63 + sec8:
        residual_text += " " + " ".join(spec[start:start + 20])
    duties = [(role, i, d) for role, r in seccomp["roles"].items() for i, d in enumerate(r["duties"])]
    out = {"paths": {}, "families": {"S_seccomp_duties": len(duties), "M_selinux_assertions": len(matrix["assertions"]),
                                      "D_amendment_items_obligations": sum(len(a["items"]) + len(a["obligations"]) for a in amend.values()),
                                      "T04_rows": sum(1 for a in amend.values() for x in a["items"] + a["obligations"] if "T04" in json.dumps(x))},
           "residual_entries": [x["id"] for a in amend.values() for x in a["residuals"]], "base_counterexamples_not_enumerated": 17}
    for n, p in sorted(paths.items()):
        toks = p["tokens"]
        def hit(text):
            return any(re.search(r"\b" + re.escape(t) + r"\b", text) for t in toks)
        s_rows = [role + "#" + str(i) for role, i, d in duties if (re.search(r":(\d+)$", str(d.get("source", ""))) and p["start"] <= int(re.search(r":(\d+)$", str(d["source"])).group(1)) <= p["end"]) or hit(str(d.get("row", "")) + " " + str(d.get("source", "")))]
        m_rows = [a["id"] for a in matrix["assertions"] if hit(str(a.get("ref", "")) + " " + str(a.get("statement", "")))]
        d_rows = [k + ":" + x["id"] for k, a in amend.items() for x in a["items"] + a["obligations"] if hit(json.dumps(x))]
        t_rows = [r for r in d_rows if "T04" in r or any("T04" in json.dumps(x) and k + ":" + x["id"] == r for k, a in amend.items() for x in a["items"] + a["obligations"])]
        residual = hit(residual_text) or ("counterexample %d" % n) in residual_text
        status = "UNRESOLVED" if not toks else ("COVERED" if (s_rows or m_rows or d_rows) else ("RESIDUAL" if residual else "UNCOVERED"))
        out["paths"][n] = {"lines": [p["start"], p["end"]], "has_required": p["has_required"], "tokens": toks, "same_in_hs53": same[n],
                           "S": s_rows[:12], "M": m_rows[:12], "D": d_rows[:12], "T04": t_rows[:8], "residual": residual, "status": status,
                           "counts": {"S": len(s_rows), "M": len(m_rows), "D": len(d_rows), "T04": len(t_rows)}}
    st = [v["status"] for v in out["paths"].values()]
    out["gate"] = {"paths": len(st), "covered": st.count("COVERED"), "residual": st.count("RESIDUAL"), "uncovered": st.count("UNCOVERED"), "unresolved": st.count("UNRESOLVED"),
                   "outcome": "FAIL" if "UNCOVERED" in st else ("INCONCLUSIVE" if "UNRESOLVED" in st else "PASS")}
    Path(out_path).write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    for n, v in sorted(out["paths"].items()): print(n, v["status"], "tokens", v["tokens"], "counts", v["counts"], "residual", v["residual"], "same", v["same_in_hs53"])
    print("gate", out["gate"], "families", out["families"], "residual entries", out["residual_entries"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
