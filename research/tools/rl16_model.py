"""RL-16 (H-02, cost-model half): the attested share of argv 63 from R00's published cost split at 280, the equal-load
growth of verify time per slot on the K 6 era's verify runs (RL-01's datasets), the G1 projection at sample fractions
5, 10 and 20 percent with cadence 10, and the detection-delay model. Standard library; deterministic apart from the
seeded pairs bootstrap. usage: python3 -I -B rl16_model.py COST_SPLIT_TXT I1_ROWS_TSV I2_RUNS_TSV OUT.json"""
import csv
import json
import random
import re
import sys

SEED = 20261105
SLOT_LO, SLOT_HI = 253, 278  # the K 6 era rows RL-01 fitted (K 8 begins at 280)
FRACTIONS = (0.05, 0.10, 0.20)
CADENCE = 10


def cost_split(text):
    g = lambda pat: float(re.search(pat, text).group(1))
    out = {"serial_total_s": g(r"argv 63 serial.*?(\d+\.\d+) s in all"),
           "chain_files_s": g(r"chain-layer test files: \d+ \(of \d+ layers\), (\d+\.\d+) s"),
           "head_s": g(r"the head's (\d+\.\d+) s"), "older_s_reported": g(r"older layers (\d+\.\d+) s"),
           "bands": {m.group(1): float(m.group(2)) for m in re.finditer(r"slots (\d+-\d+): \d+ test files, (\d+\.\d+) s", text)},
           "argv63_wall_k8_s": g(r"argv 63 wall (\d+\.\d+) s"), "cli_s": g(r"chain-layer validator CLIs \d+, (\d+\.\d+) s"), "rest_s": g(r"the rest (\d+\.\d+) s")}
    older_bands = sum(v for k, v in out["bands"].items() if not k.startswith("280"))
    out["older_s_from_bands"] = round(older_bands, 1)
    out["attested_fraction"] = round(older_bands / out["serial_total_s"], 4)
    out["kept_fraction"] = {str(f): round((out["serial_total_s"] - older_bands) / out["serial_total_s"] + older_bands / out["serial_total_s"] * f, 4) for f in FRACTIONS}
    return out


def ols3(rows):
    # elapsed = a + g*slot + l*load ; normal equations, 3 x 3, Gaussian elimination
    X = [[1.0, r["slot"], r["load"]] for r in rows]; y = [r["elapsed"] for r in rows]
    n = 3
    A = [[sum(X[k][i] * X[k][j] for k in range(len(X))) for j in range(n)] for i in range(n)]
    b = [sum(X[k][i] * y[k] for k in range(len(X))) for i in range(n)]
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[p] = M[p], M[i]
        if abs(M[i][i]) < 1e-12:
            return None
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                M[r] = [M[r][c] - f * M[i][c] for c in range(n + 1)]
    beta = [M[i][n] / M[i][i] for i in range(n)]
    pred = [beta[0] + beta[1] * r["slot"] + beta[2] * r["load"] for r in rows]
    ss_res = sum((yy - pp) ** 2 for yy, pp in zip(y, pred)); ybar = sum(y) / len(y); ss_tot = sum((yy - ybar) ** 2 for yy in y)
    return {"a": beta[0], "g_per_slot": beta[1], "l_per_load": beta[2], "r2": 1 - ss_res / ss_tot if ss_tot else None}


def growth(i1_path, i2_path):
    slot_by_pr = {r["pr"]: int(r["slot"]) for r in csv.DictReader(open(i1_path, encoding="utf-8"), delimiter="\t") if r.get("slot", "").isdigit()}
    rows = []
    for r in csv.DictReader(open(i2_path, encoding="utf-8"), delimiter="\t"):
        s = slot_by_pr.get(r["pr"])
        if s is None or r.get("conclusion") != "success" or SLOT_LO > s or s > SLOT_HI:
            continue
        try:
            rows.append({"slot": s, "elapsed": float(r["elapsed_s"]), "load": float(r["load_run_mean"])})
        except ValueError:
            continue
    fit = ols3(rows)
    rng = random.Random(SEED); boots = []; undefined = 0
    for _ in range(1000):
        sample = [rows[rng.randrange(len(rows))] for _ in rows]
        f = ols3(sample)
        if f is None or len({r["slot"] for r in sample}) < 3:
            undefined += 1
        else:
            boots.append(f["g_per_slot"])
    boots.sort(); d = len(boots)
    ci = [boots[int(0.025 * d)], boots[int(0.975 * d) - 1]] if d >= 900 else None
    # descriptive: univariate slope on slot, and the median load
    xs = [r["slot"] for r in rows]; ys = [r["elapsed"] for r in rows]; xb = sum(xs) / len(xs); yb = sum(ys) / len(ys)
    uni = sum((x - xb) * (y - yb) for x, y in zip(xs, ys)) / sum((x - xb) ** 2 for x in xs)
    return {"n": len(rows), "slots": sorted({r["slot"] for r in rows}), "fit": fit, "g_ci95": ci, "defined_resamples": d, "undefined_resamples": undefined,
            "univariate_g_per_slot": uni, "median_load": sorted(r["load"] for r in rows)[len(rows) // 2], "elapsed_range": [min(ys), max(ys)]}


def projection(cs, g):
    out = {}
    for f in FRACTIONS:
        kept = cs["kept_fraction"][str(f)]
        argv63 = cs["argv63_wall_k8_s"] * kept
        total = cs["cli_s"] + cs["rest_s"] + argv63
        # detection delay for a checkpoint-run defect in an attested layer: sampled with probability f per verify, certain at the cadence rewrite
        p_within = {str(k): round(1 - (1 - f) ** k, 4) if k < CADENCE else 1.0 for k in (1, 3, 5, CADENCE)}
        expected = sum(k * f * (1 - f) ** (k - 1) for k in range(1, CADENCE)) + CADENCE * (1 - f) ** (CADENCE - 1)
        out[str(f)] = {"kept_fraction": kept, "argv63_wall_k8_s": round(argv63, 1), "saving_argv63_s": round(cs["argv63_wall_k8_s"] - argv63, 1),
                       "projected_dry_run_total_s": round(total, 1), "growth_bound_per_cadence_s": round(CADENCE * g, 1) if g is not None else None,
                       "detect_within_k_verifies": p_within, "expected_detection_delay_verifies": round(expected, 2), "max_delay_verifies": CADENCE}
    return out


def main(cost_txt, i1, i2, out_path):
    cs = cost_split(open(cost_txt, encoding="utf-8").read())
    gr = growth(i1, i2)
    g = gr["fit"]["g_per_slot"] if gr["fit"] else None
    rec = {"seed": SEED, "cadence": CADENCE, "fractions": list(FRACTIONS), "costSplit": cs, "growth": gr, "projection": projection(cs, g)}
    json.dump(rec, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("attested %.4f kept(0.10) %.4f bands %.1f vs reported %.1f | growth g %.2f s/slot ci %s n %d | load %.2f s per unit" % (
        cs["attested_fraction"], cs["kept_fraction"]["0.1"], cs["older_s_from_bands"], cs["older_s_reported"], g, gr["g_ci95"], gr["n"], gr["fit"]["l_per_load"]))


if __name__ == "__main__":
    main(*sys.argv[1:5])
