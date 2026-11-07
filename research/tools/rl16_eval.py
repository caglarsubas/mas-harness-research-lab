"""RL-16 evaluator (PREREG v1): gates on the model output and the verdict ledger.
usage: python3 -I -B rl16_eval.py MODEL_JSON PREREG_MD RUN_RECORD_MD OUT_RESULTS_JSON"""
import hashlib
import json
import pathlib
import sys

R00_ATTESTED, R00_KEPT_10 = 0.645, 0.4195  # DESIGN_CC2 rev 2, section 2 (as published)
REPORTED_G, G_LO, G_HI = 13.0, 8.0, 18.0     # the R&D report's "about 13 s per slot", with the lab's +-5 s band


def sha(path):
    return "sha256:" + hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def main(model_json, prereg, run_record, out_path):
    m = json.load(open(model_json, encoding="utf-8")); cs = m["costSplit"]; gr = m["growth"]
    # H-02a: re-derivation of the attested and kept fractions from the published bands
    bands_ok = abs(cs["older_s_from_bands"] - cs["older_s_reported"]) <= 0.01 * cs["older_s_reported"]
    att_ok = abs(cs["attested_fraction"] - R00_ATTESTED) <= 0.005
    kept_ok = abs(cs["kept_fraction"]["0.1"] - R00_KEPT_10) <= 0.005
    a_status = "PASS" if (bands_ok and att_ok and kept_ok) else "FAIL"
    a_value = "bands sum %.1f vs reported %.1f (within 1 percent: %s); attested %.4f vs 0.645 (within 0.005: %s); kept at 0.10 %.4f vs 0.4195 (within 0.005: %s)" % (
        cs["older_s_from_bands"], cs["older_s_reported"], bands_ok, cs["attested_fraction"], att_ok, cs["kept_fraction"]["0.1"], kept_ok)
    # H-02b: equal-load growth per slot against the report's figure
    g = gr["fit"]["g_per_slot"] if gr["fit"] else None; ci = gr["g_ci95"]
    WIDTH_CAP = 20.0  # PREREG v2: PASS needs an informative interval
    if gr["n"] < 15:  # precedence (PREREG v2): the UNRESOLVED triggers first, then FAIL, then PASS
        b_status, b_why = "UNRESOLVED", "fewer than 15 runs"
    elif g is None or ci is None:
        b_status, b_why = "UNRESOLVED", "no fit or fewer than 900 defined resamples"
    elif ci[1] < G_LO or ci[0] > G_HI:
        b_status, b_why = "FAIL", "the interval lies entirely outside [8, 18]"
    elif ci[0] <= REPORTED_G <= ci[1] and G_LO <= g <= G_HI and (ci[1] - ci[0]) <= WIDTH_CAP:
        b_status, b_why = "PASS", "the interval contains 13, the estimate lies in [8, 18] and the interval is at most 20 s wide"
    else:
        b_status, b_why = "UNRESOLVED", "the interval overlaps [8, 18] but PASS is not met (estimate outside the band, 13 outside the interval, or the interval wider than 20 s)"
    b_value = "g %.2f s per slot at equal load, 95 percent pairs bootstrap [%s, %s] (%d defined resamples), n %d runs over slots %d-%d, load coefficient %.1f s per unit, R2 %.3f; univariate slope %.2f" % (
        g if g is not None else float("nan"), "%.2f" % ci[0] if ci else "-", "%.2f" % ci[1] if ci else "-", gr["defined_resamples"], gr["n"], gr["slots"][0], gr["slots"][-1],
        gr["fit"]["l_per_load"] if gr["fit"] else float("nan"), gr["fit"]["r2"] if gr["fit"] and gr["fit"]["r2"] is not None else float("nan"), gr["univariate_g_per_slot"])
    status = "PASS" if (a_status == "PASS" and b_status == "PASS") else ("FAIL" if "FAIL" in (a_status, b_status) else "UNRESOLVED")
    proj = m["projection"]
    c_value = "; ".join("f %s: kept %.4f, argv 63 wall %.1f s (saving %.1f s), projected dry-run total %.1f s, growth bound per cadence %s s, P(detect within 1/3/5/10) %s, expected delay %.2f verifies (max %d)" % (
        f, p["kept_fraction"], p["argv63_wall_k8_s"], p["saving_argv63_s"], p["projected_dry_run_total_s"], p["growth_bound_per_cadence_s"], json.dumps(p["detect_within_k_verifies"]), p["expected_detection_delay_verifies"], p["max_delay_verifies"]) for f, p in sorted(proj.items()))
    self_digest = "sha256:" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
    led = {
        "schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-16-RESULTS-v1", "supersedes": None,
        "subject": {"scopeDigest": sha(prereg)}, "rollouts": ["run-001"],
        "contexts": [{"contextId": "lab", "role": "EVALUATOR", "inheritsFrom": []}],
        "evidence": [
            {"evidenceId": "E1", "kind": "ARTIFACT", "contentDigest": sha(model_json), "producedBy": "Research-Lab.rl16_model.run-001"},
            {"evidenceId": "E2", "kind": "ENVIRONMENT_STATE", "contentDigest": sha(run_record), "producedBy": "Research-Lab.run-record-001"},
            {"evidenceId": "E3", "kind": "ARTIFACT", "contentDigest": self_digest, "producedBy": "Research-Lab.rl16_eval"},
        ],
        "claims": [
            {"claimId": "H-02a", "requirement": "H-02a: the attested share of argv 63 and the kept fraction at a 10 percent sample re-derive from the published cost split to R00's figures", "delivered": a_value, "rolloutValues": [{"rollout": "run-001", "value": a_status}]},
            {"claimId": "H-02b", "requirement": "H-02b: the equal-load growth of verify time per slot in the K 6 era reproduces the report's about 13 s per slot within 5 s", "delivered": b_value, "rolloutValues": [{"rollout": "run-001", "value": b_status}]},
        ],
        "checks": [
            {"checkId": "C1", "claimId": "H-02a", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 1, "target": "DELIVERED", "establishedValue": a_value, "outcome": a_status, "evidence": ["E1", "E3"]},
            {"checkId": "C2", "claimId": "H-02b", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 2, "target": "DELIVERED", "establishedValue": b_value + "; gate: " + b_why, "outcome": b_status, "evidence": ["E1", "E3"]},
            {"checkId": "C3", "claimId": "H-02b", "contextId": "lab", "kind": "DETERMINISTIC_TEST", "sequence": 3, "target": "INTERMEDIATE", "establishedValue": "projection and detection-delay model, descriptive, never gated: " + c_value, "outcome": "PASS", "evidence": ["E1"]},
        ],
        "claimVerdicts": [
            {"claimId": "H-02a", "checks": ["C1"], "verdict": {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(a_status, "UNRESOLVED"), "value": a_value},
            {"claimId": "H-02b", "checks": ["C2", "C3"], "verdict": {"PASS": "SUPPORTED", "FAIL": "CONTRADICTED"}.get(b_status, "UNRESOLVED"), "value": b_value},
        ],
        "verdict": {"status": status, "producedBy": "lab", "unresolvedChecks": ["C2"] if b_status == "UNRESOLVED" else [], "policyViolations": [],
                    "scores": {"attested_permille": int(round(cs["attested_fraction"] * 1000)), "kept_10_permille": int(round(cs["kept_fraction"]["0.1"] * 1000)), "g_per_slot_ds": int(round(g * 10)) if g is not None else None,
                               "g_ci_lo_ds": int(round(ci[0] * 10)) if ci else None, "g_ci_hi_ds": int(round(ci[1] * 10)) if ci else None, "n_runs": gr["n"], "defined_resamples": gr["defined_resamples"]},
                    "evidenceRefs": [sha(model_json), sha(run_record), sha(prereg), self_digest]},
    }
    json.dump(led, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(status, "| H-02a", a_status, "| H-02b", b_status, b_why)


if __name__ == "__main__":
    main(*sys.argv[1:5])
