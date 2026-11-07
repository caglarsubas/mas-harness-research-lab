"""RL-01 confirmatory analysis (PREREG v1 section 3): OLS of T and log T on L, C, K with PR-clustered percentile
bootstrap intervals. usage: python3 -I -B rl01_fit.py I2.tsv I1_rows.tsv OUT.json   (stdlib only; prints the summary)"""
import csv
import json
import math
import random
import sys

SEED, RESAMPLES = 20261104, 1000


def fnum(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def ols(xs, ys):
    """Least squares with an intercept by normal equations (Gaussian elimination); xs rows are predictor lists."""
    p = len(xs[0]) + 1
    a = [[0.0] * p for _ in range(p)]
    b = [0.0] * p
    for row, y in zip(xs, ys):
        v = [1.0] + list(row)
        for i in range(p):
            b[i] += v[i] * y
            for j in range(p):
                a[i][j] += v[i] * v[j]
    for i in range(p):
        pivot = max(range(i, p), key=lambda r: abs(a[r][i]))
        a[i], a[pivot], b[i], b[pivot] = a[pivot], a[i], b[pivot], b[i]
        for r in range(p):
            if r != i and a[i][i]:
                f = a[r][i] / a[i][i]
                a[r] = [x - f * y for x, y in zip(a[r], a[i])]
                b[r] -= f * b[i]
    return [b[i] / a[i][i] for i in range(p)]


def zscore(cols):
    out = []
    for col in cols:
        m = sum(col) / len(col)
        s = math.sqrt(sum((x - m) ** 2 for x in col) / (len(col) - 1))
        out.append([(x - m) / s for x in col])
    return out


def fit_with_bootstrap(rows, target):
    xs = [[r["L"], r["C"], r["K"]] for r in rows]
    cols = zscore(list(zip(*xs)))
    xs = [list(t) for t in zip(*cols)]
    ys = [target(r) for r in rows]
    point = ols(xs, ys)
    clusters = {}
    for i, r in enumerate(rows):
        clusters.setdefault(r["pr"], []).append(i)
    keys = sorted(clusters)
    rng = random.Random(SEED)
    draws = []
    for _ in range(RESAMPLES):
        idx = [i for k in rng.choices(keys, k=len(keys)) for i in clusters[k]]
        try:
            draws.append(ols([xs[i] for i in idx], [ys[i] for i in idx]))
        except ZeroDivisionError:
            continue
    names = ["intercept", "bL", "bC", "bK"]
    result = {}
    for j, name in enumerate(names):
        vals = sorted(d[j] for d in draws)
        lo, hi = vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]
        result[name] = {"estimate": round(point[j], 4), "ci95": [round(lo, 4), round(hi, 4)],
                        "excludes_zero": lo > 0 or hi < 0}
    resid = [y - (point[0] + sum(c * x for c, x in zip(point[1:], row))) for row, y in zip(xs, ys)]
    ss_res = sum(e * e for e in resid)
    mean = sum(ys) / len(ys)
    ss_tot = sum((y - mean) ** 2 for y in ys)
    result["r2"] = round(1 - ss_res / ss_tot, 4)
    result["n"] = len(rows)
    result["clusters"] = len(keys)
    result["bootstrap_draws"] = len(draws)
    return result


def main(i2_path, i1_path, out_path):
    slot_by_pr = {}
    for r in csv.DictReader(open(i1_path, encoding="utf-8"), delimiter="\t"):
        if r["slot"] and r["pr"]:
            slot_by_pr[int(float(r["pr"]))] = int(float(r["slot"]))
    rows, dropped = [], {"no_tests_passed": 0, "no_slot": 0}
    for r in csv.DictReader(open(i2_path, encoding="utf-8"), delimiter="\t"):
        pr = int(r["pr"])
        L, C, T = fnum(r["load_run_mean"]), fnum(r["tests_passed"]), fnum(r["elapsed_s"])
        if C is None:
            dropped["no_tests_passed"] += 1
            continue
        if pr not in slot_by_pr:
            dropped["no_slot"] += 1
            continue
        rows.append({"pr": pr, "L": L, "C": C, "K": float(slot_by_pr[pr]), "T": T})
    out = {"seed": SEED, "resamples": RESAMPLES, "rows_used": len(rows), "dropped": dropped,
           "fit1_T": fit_with_bootstrap(rows, lambda r: r["T"]),
           "fit2_logT": fit_with_bootstrap(rows, lambda r: math.log(r["T"]))}
    # descriptive context
    ts = sorted(r["T"] for r in rows)
    out["T_summary"] = {"min": ts[0], "median": ts[len(ts) // 2], "max": ts[-1]}
    out["K_range"] = [min(r["K"] for r in rows), max(r["K"] for r in rows)]
    out["pairwise_r"] = {}
    for a, b in [("L", "C"), ("L", "K"), ("C", "K"), ("K", "T"), ("C", "T"), ("L", "T")]:
        xa, xb = zscore([[r[a] for r in rows], [r[b] for r in rows]])
        out["pairwise_r"][a + b] = round(sum(x * y for x, y in zip(xa, xb)) / (len(xa) - 1), 3)
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main(*sys.argv[1:4])
