"""RL-07 replay (PREREG v1): the chain vectors through the pinned evaluators, section by section.
usage: python3 -I -B rl07_replay.py EXPORT_ARCH SCRIPTS_DIR OUT.json SECTION [SECTION ...]
Sections: counts bindings allowedPaths pin steps products classForms inheritance. Modules are imported by path from
SCRIPTS_DIR (v2 must be named chain_identity_v2.py for v3's pin). Outputs: per vector id the expected and observed
outcome and clause, mismatches, counts. No vector body is printed."""
import ast
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


def load(scripts, name):
    path = Path(scripts) / (name + ".py")
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def outcome(fn, *args, **kw):
    """OK, or refuse with the clause the evaluator raised (clause = the text before the first ': ' of the message,
    or the exception's `clause` attribute when it has one)."""
    try:
        fn(*args, **kw)
        return "OK", ""
    except Exception as exc:  # the evaluators refuse by raising
        clause = getattr(exc, "clause", None) or str(exc).split(":", 1)[0].strip()
        if clause.startswith("identity "):  # the evaluators raise ValueError("identity <clause>: <detail>")
            clause = clause[len("identity "):]
        return "refuse", clause


def main(arch, scripts, out_path, sections):
    arch = Path(arch)
    v2, v3, v1 = load(scripts, "chain_identity_v2"), load(scripts, "chain_identity_v3"), load(scripts, "chain_identity")
    safe_load = None
    reader = load(scripts, "safe_yaml")
    if reader is not None:
        safe_load = getattr(reader, "safe_load", None)
    pv = json.loads((arch / "chain-product-packets/vectors.json").read_text())
    iv = json.loads((arch / "chain-inheritance/vectors.json").read_text())
    ext = json.loads((arch / "chain-product-packets/rule.json").read_text())
    ext3 = json.loads((arch / "chain-inheritance/rule.json").read_text())
    idr = json.loads((arch / "chain-compaction/identity-rule.json").read_text())
    v2_raw = (Path(scripts) / "chain_identity_v2.py").read_bytes()
    out = {"sections": {}, "extends_digests_ok": {
        "inheritance_extends_product_rule": hashlib.sha256((arch / "chain-product-packets/rule.json").read_bytes()).hexdigest() == ext3["extends"]["sha256"],
        "product_rule_extends_identity_rule": hashlib.sha256((arch / "chain-compaction/identity-rule.json").read_bytes()).hexdigest() == ext["extends"]["sha256"]}}
    pinned = None
    try:
        pinned = v3.pin_v2(v2, v2_raw)
    except Exception as exc:
        out["pin_v2_error"] = str(exc)[:120]

    def record(name, rows):
        mism = [r for r in rows if r["observed"] != r["expect"] or (r["expect"] == "refuse" and r["expected_clause"] and r["clause"] != r["expected_clause"])]
        out["sections"][name] = {"n": len(rows), "matches": len(rows) - len(mism), "mismatches": [{k: r[k] for k in ("id", "expect", "observed", "expected_clause", "clause")} for r in mism],
                                 "expected_refuse": sum(r["expect"] == "refuse" for r in rows), "rows": rows}

    def row(case, obs):
        return {"id": case["id"], "expect": case["expect"], "expected_clause": case.get("clause", ""), "observed": obs[0], "clause": obs[1]}

    if "counts" in sections:
        record("counts", [row(c, outcome(v2.check_counts, c["slot"], c["catalog"], c["products"])) for c in pv["counts"]])
    if "bindings" in sections:
        record("bindings", [row(c, outcome(lambda s: v2.layer_products(ast.parse(s)), c["source"])) for c in pv["bindings"]])
    if "allowedPaths" in sections:
        record("allowedPaths", [row(c, outcome(v2.check_allowed_paths, c["allowed"], c["changed"], c["new"], c["authority"], c["validator"], c["ownYaml"], c["products"])) for c in pv["allowedPaths"]])
    if "pin" in sections:
        pin = iv["pin"]
        out["sections"]["pin"] = {"n": 1, "matches": int(hashlib.sha256(v2_raw).hexdigest() == pin["sha256"] and pinned is not None), "mismatches": [], "expected_refuse": 0,
                                  "detail": {"id": pin["id"], "path": pin["path"], "digest_equal": hashlib.sha256(v2_raw).hexdigest() == pin["sha256"], "pin_v2_ok": pinned is not None}}
    if "steps" in sections and v1 is not None:
        record("steps", [row(c, outcome(v2.check_step_vector, c, v1)) for c in pv["steps"]])
    if "classForms" in sections and v1 is not None:
        bases = pv["classForms"]["bases"]
        rows2 = [row(c, outcome(v2.check_class_vector, c, bases, idr, v1)) for c in pv["classForms"]["cases"]]
        rows3 = [row(c, outcome(v3.check_class_vector, c, bases, idr, v1, pinned)) for c in iv["classForms"]["cases"]] if pinned is not None else []
        record("classForms_v2", rows2); record("classForms_v3", rows3)
    if "products" in sections and safe_load is not None:
        def run_products(c):
            files = {"task-packets/%s.yaml" % k: v.encode("utf-8") for k, v in c["files"].items()}
            listed = {int(k): list(v) for k, v in c["listed"].items()}
            return outcome(v2.check_products, ext, listed, files.__getitem__, safe_load, tuple(c.get("chainPackets", ())))
        record("products", [row(c, run_products(c)) for c in pv["products"]])
    if "inheritance" in sections and safe_load is not None and pinned is not None:
        record("inheritance", [row(c, outcome(v3.check_inheritance_vector, c, ext3, safe_load, pinned)) for c in iv["inheritance"]])
    out["modules"] = {"v1": v1 is not None, "v2": v2 is not None, "v3": v3 is not None, "safe_load": safe_load is not None}
    Path(out_path).write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in out["sections"].items()}, indent=1, sort_keys=True))
    print("extends", out["extends_digests_ok"], "modules", out["modules"], out.get("pin_v2_error", ""))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
