"""RL-11 (PREREG v1): the widened documentary join (families S, M, D, T, G, R) over counterexamples 18-28.
usage: python3 -I -B rl11_join.py EXPORT_ARCH OUT.json   (stdlib; prints per-path coverage; no spec text printed)"""
import json
import re
import sys
from pathlib import Path

CLAUSE = re.compile(r"\b(?:[PASCEI]\d{1,2}|I0\d|v\d|T0\d)\b")
TICK = re.compile(r"`([^`]{2,40})`")
OPS = re.compile(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b|\b(?:CREATE|DELETE|GET|ARM|HELD|CSR|RBAC|WRITE|READ)\b")
GENERIC = {"W01"}
CITED = {18: ["T28", "T31", "T30", "T90", "T27"], 21: ["T25"], 22: ["T05", "T13", "T39", "T43", "T06", "T04", "T02", "T03"]}
R10_RESIDUAL = {22: "C4 stamp-equality branch declared unreachable (closed by C2's flush at ARM(B); vectored as T02/T03 only)", 28: "no native-profile v4 T04 proof names A17, A18 or A38; T04-LABELS is a precondition only"}
G_FILES = ["i05-gate-channel/vectors.json", "i05-gate-channel-v2/vectors.json", "i05-gate-channel-v3/vectors.json", "i05-gate-channel-v4/vectors.json",
           "admission-semantics-v2/vectors.json", "admission-semantics-v3/vectors.json", "admission-semantics-v4/vectors.json",
           "i07-policy-write/vectors.json", "i07-policy-write-v2/vectors.json", "i07-policy-write-v3/vectors.json"]
G_TEXT = ["i05-gate-channel-v4/README.md", "admission-semantics-v4/README.md", "i07-policy-write-v3/README.md", "i05-gate-channel-authority.json", "i05-gate-channel-v2-authority.json",
          "i05-gate-channel-v4-authority.json", "admission-semantics-v2-authority.json", "admission-channel-v3-authority.json", "artifact-edges/operator-harness-engineering-v12.json",
          "edge-record-v9-authority.json", "edge-record-v12-authority.json"]


def paths_of(spec):
    paths, cur = {}, None
    for i, line in enumerate(spec, 1):
        m = re.match(r"^(\d{1,2})\. ", line)
        if m and 18 <= int(m.group(1)) <= 28:
            cur = int(m.group(1)); paths[cur] = {"start": i, "end": i, "text": line}
        elif cur and line.startswith("   "):
            paths[cur]["end"] = i; paths[cur]["text"] += " " + line.strip()
        else:
            cur = None
    for n, p in paths.items():
        t = p["text"]
        toks = set(CLAUSE.findall(t)) | set(TICK.findall(t)) | set(OPS.findall(t))
        p["tokens"] = sorted(x for x in toks if x not in GENERIC and len(x) >= 2); del p["text"]
    return paths


def hit(toks, text):
    return any(re.search(r"(?<![A-Za-z0-9_])" + re.escape(t) + r"(?![A-Za-z0-9_])", text) for t in toks)


def main(arch, out_path):
    arch = Path(arch)
    spec = (arch / "host-interface-inputs/resolved/HOST_INTERFACE_SPEC.md").read_text(encoding="utf-8").splitlines()
    paths = paths_of(spec)
    seccomp = json.loads((arch / "seccomp-allowlists-v5/allowlists.json").read_text())
    matrix = json.loads((arch / "selinux-matrix-v4/matrix.json").read_text())
    amend = {k: json.loads((arch / ("host-interface-amendment-%s/amendment.json" % k)).read_text()) for k in ("hs53", "he5")}
    residual_text = " ".join(json.dumps(a["residuals"]) for a in amend.values())
    for start in [i for i, l in enumerate(spec, 1) if l.startswith("### 6.3") or l.startswith("## 8.")]:
        residual_text += " " + " ".join(spec[start:start + 20])
    duties = [(role, i, d) for role, r in seccomp["roles"].items() for i, d in enumerate(r["duties"])]
    g_rows = []
    for f in G_FILES:
        v = json.loads((arch / f).read_text())
        for sec, items in v.items():
            if isinstance(items, list):
                for c in items:
                    if isinstance(c, dict) and "id" in c:
                        g_rows.append((f.split("/")[0] + ":" + sec + ":" + str(c["id"]), str(c["id"]), json.dumps({k: c[k] for k in c if k in ("id", "intent", "expect", "refusal", "kind", "override", "verb", "outcome")})))
    g_text = [(f, "", (arch / f).read_text(encoding="utf-8", errors="replace")) for f in G_TEXT]
    out = {"paths": {}, "families": {"S": len(duties), "M": len(matrix["assertions"]), "D": sum(len(a["items"]) + len(a["obligations"]) for a in amend.values()), "G_vectors": len(g_rows), "G_text": len(g_text)}}
    for n, p in sorted(paths.items()):
        toks = p["tokens"]
        S = [role + "#" + str(i) for role, i, d in duties if (re.search(r":(\d+)$", str(d.get("source", ""))) and p["start"] <= int(re.search(r":(\d+)$", str(d["source"])).group(1)) <= p["end"]) or hit(toks, str(d.get("row", "")) + " " + str(d.get("source", "")))]
        M = [a["id"] for a in matrix["assertions"] if hit(toks, str(a.get("ref", "")) + " " + str(a.get("statement", "")))]
        D = [k + ":" + x["id"] for k, a in amend.items() for x in a["items"] + a["obligations"] if hit(toks, json.dumps(x))]
        T = [r for r in D if "T04" in r]
        cited = set(CITED.get(n, []))
        G = [rid for rid, cid, text in g_rows if hit(toks, text)]
        R = [rid for rid, cid, text in g_rows if cid in cited and rid.startswith("i05-gate-channel-v3:transcripts:")]
        Gt = [f for f, _, text in g_text if hit(toks, text)]
        residual = hit(toks, residual_text) or n in R10_RESIDUAL
        covered = bool(S or M or D or G or R or Gt)
        status = "UNRESOLVED" if not toks else ("COVERED" if covered else ("RESIDUAL" if residual else "UNCOVERED"))
        out["paths"][n] = {"tokens": toks, "counts": {"S": len(S), "M": len(M), "D": len(D), "T04": len(T), "G": len(G), "G_text": len(Gt), "R": len(R)}, "S": S[:8], "M": M[:8], "D": D[:8], "G": G[:12], "G_text": Gt, "R": R, "residual": residual, "r10_residual": R10_RESIDUAL.get(n), "status": status,
                           "covering_families": [k for k, v in (("S", S), ("M", M), ("D", D), ("G", G), ("G_text", Gt), ("R", R)) if v]}
    st = [v["status"] for v in out["paths"].values()]
    out["gate"] = {"paths": len(st), "covered": st.count("COVERED"), "residual": st.count("RESIDUAL"), "uncovered": st.count("UNCOVERED"), "unresolved": st.count("UNRESOLVED"), "outcome": "FAIL" if "UNCOVERED" in st else ("INCONCLUSIVE" if "UNRESOLVED" in st else "PASS")}
    Path(out_path).write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    for n, v in sorted(out["paths"].items()): print(n, v["status"], "families", v["covering_families"], "counts", v["counts"], "tokens", v["tokens"][:8])
    print("gate", out["gate"], "families", out["families"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
