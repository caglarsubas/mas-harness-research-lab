"""RL-23 evaluator (PREREG v4, sha256 prefix 2bbd9728): the factory-trials observational study, hypotheses H-37 to H-44.
Reads the monitor's aggregate deliveries (form planeon.research.factory-aggregates/v1), applies the ordered gate of
PREREG section 7 with the constants pinned in sections 2 to 4, and writes a verdict ledger (planeon.internal.verdict-ledger/v1).
Every constant below is copied from the frozen PREREG; the digest check refuses any other PREREG. Standard library only.

usage:
  python3 -I -B rl23_factory.py check DELIVERY...                                  acceptance boundary only; REJECT codes
  python3 -I -B rl23_factory.py preflight PREREG_MD FIXTURE_DIR OUT_JSON            builds the known-answer fixtures, evaluates each
  python3 -I -B rl23_factory.py evaluate PREREG_MD PREFLIGHT_JSON OUT_LEDGER DELIVERY...   STOP unless the preflight reads PASS
Counts and verdicts on stdout; no delivery content is printed.
Missing evidence (bridge issue 6, 2026-11-13): a post unit whose fidelity, confounder evidence (account-switch count, slot
scopeDate), guard observation or primary measure is absent is excluded with a named reason and counted; evidence absent
from every post unit reads UNRESOLVED U2 (PREREG section 6: a missing field is a missing measure, never a zero). Absence
is never read as exposure, as "unconfounded" or as zero incidents.
"""
import datetime
import hashlib
import json
import re
import statistics
import sys
from fractions import Fraction
from pathlib import Path

PREREG_PREFIX = "2bbd9728"
SCHEMA = "planeon.research.factory-aggregates/v1"
PINS = {"meterSha256": "44d6f454ce86fd53", "extractSha256": "ec0b1d9d27d11759"}
MONITOR = "Lane-Monitor"
PRE_DAYS, POST_DAYS, EXCLUDED_DAY = ("2026-11-05", "2026-11-11"), ("2026-11-13", "2026-11-19"), "2026-11-12"
LOAD_PRE, LOAD_POST_FROM, STOP_DATE = ("2026-11-05T00:00", "2026-11-12T11:05"), "2026-11-12T12:00", "2026-11-26"
H40_PRE, POST_SLOTS = (285, 287), (289, 292)
KINDS = ("verify-start", "push", "worktree")
T = {"h37": Fraction(3, 4), "h38_watch": 50, "h39": Fraction(7, 10), "h40_rounds": 2, "h41_c2": 3, "h42_rulings": 10,
     "h42_hours": Fraction(6), "h43_major": 4, "h44_ctx": 365000, "h44_min": Fraction("16.07"), "h44_slips": 0,
     "overshoot": 95, "fanout": 60}
MIN = {"days": 3, "load": 8, "load_verify": 3, "h40_pre": 2, "post_slots": 3, "guard_pre": 2, "h43_post": 3}
HYPOTHESES = ("H-37", "H-38", "H-39", "H-40", "H-41", "H-42", "H-43", "H-44")
CLASSES = {"days": ("date", "session"), "windows": ("windowEnd",), "loadEvents": ("at", "kind"), "slots": ("slot",), "changes": ("date", "kind")}
NUM = (int, float)
DATE_RE, TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$"), re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_num(v) -> bool:
    return isinstance(v, NUM) and not isinstance(v, bool)


class Reject(Exception):
    pass


def typed(item: dict, field: str, kind, cls: str, required: bool = False):
    """Returns the field's value, None when absent (a missing measure), Reject on a wrong type."""
    if field not in item or item[field] is None:
        if required:
            raise Reject("MISSING_FIELD:%s:%s" % (cls, field))
        return None
    v = item[field]
    ok = (is_num(v) if kind == "num" else isinstance(v, bool) if kind == "bool" else isinstance(v, str) if kind == "str"
          else isinstance(v, int) and not isinstance(v, bool) if kind == "int" else isinstance(v, dict) if kind == "dict"
          else isinstance(v, list))
    if not ok:
        raise Reject("TYPE:%s:%s" % (cls, field))
    return v


def iso(value, cls: str, field: str, with_time: bool = False) -> None:
    """Dates are compared as text, so every date is ISO: YYYY-MM-DD, or YYYY-MM-DDTHH:MM[:SS] for a time; else TYPE."""
    ok = isinstance(value, str) and (TIME_RE if with_time else DATE_RE).match(value) is not None
    if ok:
        try:
            datetime.date.fromisoformat(value[:10])
        except ValueError:
            ok = False
    if not ok:
        raise Reject("TYPE:%s:%s" % (cls, field))


def load_deliveries(paths):
    """The acceptance boundary: form, producer pins, every class present, typed fields, no duplicate unit."""
    merged = {k: [] for k in CLASSES}
    seen = {k: set() for k in CLASSES}
    for p in paths:
        doc = json.loads(Path(p).read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or doc.get("schemaVersion") != SCHEMA:
            raise Reject("SCHEMA:" + Path(p).name)
        producer = doc.get("producer")
        if not isinstance(producer, dict):
            raise Reject("PRODUCER_MISSING:" + Path(p).name)
        for key, prefix in PINS.items():
            if not (isinstance(producer.get(key), str) and producer[key].startswith(prefix)):
                raise Reject("PRODUCER_PIN:%s:%s" % (Path(p).name, key))
        for cls, keys in CLASSES.items():
            if not isinstance(doc.get(cls), list):
                raise Reject("MISSING_CLASS:%s:%s" % (Path(p).name, cls))
            for item in doc[cls]:
                if not isinstance(item, dict):
                    raise Reject("ITEM_SHAPE:" + cls)
                ident = tuple(typed(item, k, "int" if k == "slot" else "str", cls, required=True) for k in keys)
                if ident in seen[cls]:
                    raise Reject("DUPLICATE:%s:%s" % (cls, ",".join(str(x) for x in ident)))
                seen[cls].add(ident)
                validate(cls, item)
                merged[cls].append(item)
    return merged


def validate(cls: str, item: dict) -> None:
    if cls == "days":
        iso(item["date"], cls, "date")
        for f in ("calls", "messagesHandled", "meanContextTokens", "weightedMtok", "watchFirings", "watchCalls", "accountSwitches", "fanOuts3Plus"):
            typed(item, f, "num", cls)
        fid = typed(item, "fidelity", "dict", cls)
        if fid is not None and not all(v is None or isinstance(v, bool) for v in fid.values()):
            raise Reject("TYPE:days:fidelity")
    elif cls == "windows":
        iso(item["windowEnd"], cls, "windowEnd", with_time=True)
        typed(item, "usageAtStop", "num", cls, required=True)
        typed(item, "fanOut3PlusStartUsage", "num", cls)
    elif cls == "loadEvents":
        iso(item["at"], cls, "at", with_time=True)
        if item["kind"] not in KINDS:
            raise Reject("ENUM:loadEvents:kind")
        typed(item, "load1", "num", cls, required=True)
        typed(item, "otherAppLoad", "bool", cls, required=True)
    elif cls == "changes":
        iso(item["date"], cls, "date")
    elif cls == "slots":
        if typed(item, "scopeDate", "str", cls) is not None:
            iso(item["scopeDate"], cls, "scopeDate")
        if typed(item, "kind", "str", cls, required=True) not in ("product", "machinery"):
            raise Reject("ENUM:slots:kind")
        for f in ("c2Builds", "dryC2Runs", "rulingsWaited", "scopeToPacketR1Hours", "machineryRepairs", "machineryMajor",
                  "r00Calls", "r00MeanContextTokens", "stepMinutesMean", "lostDetailSlips", "accountSwitches", "fanOuts3Plus", "ownerWindowShare"):
            typed(item, f, "num", cls)
        series = typed(item, "series", "list", cls)
        if series is not None and not all(isinstance(s, dict) and isinstance(s.get("name"), str) and isinstance(s.get("rounds"), int)
                                          and not isinstance(s.get("rounds"), bool) for s in series):
            raise Reject("TYPE:slots:series")
        defects = typed(item, "laterDefects", "dict", cls)
        if defects is not None and not all(v is None or is_num(v) for v in defects.values()):
            raise Reject("TYPE:slots:laterDefects")
        fid = typed(item, "fidelity", "dict", cls)
        if fid is not None and not all(v is None or isinstance(v, bool) for v in fid.values()):
            raise Reject("TYPE:slots:fidelity")


def fidelity(item: dict, key: str):
    """True or False from the unit's fidelity map; None when the map, the key or its value is absent (a missing measure,
    never exposure)."""
    fid = item.get("fidelity")
    if not isinstance(fid, dict):
        return None
    return fid.get(key)


def median(values):
    return statistics.median(values) if values else None


def ratio_ok(post, pre, bound: Fraction):
    """post median / pre median <= bound on the raw values; None when the pre median is zero."""
    if pre == 0:
        return None
    return Fraction(str(post)) / Fraction(str(pre)) <= bound


def le(value, bound) -> bool:
    return Fraction(str(value)) <= Fraction(str(bound))


def defects(slot: dict):
    d = slot.get("laterDefects")
    if not isinstance(d, dict):
        return None
    parts = [d.get(k) for k in ("oracleFailures", "packetMajor", "postMergeIssues7d")]
    return None if any(v is None for v in parts) else sum(parts)


def day_flag(day: dict, changes):
    """Section 5's confounder flag for a day: True after a change or with an account switch, False otherwise, None when
    the account-switch count is missing (the flag is not computable; missing is not zero)."""
    if any(POST_DAYS[0] <= c["date"] <= day["date"] for c in changes):
        return True
    sw = day.get("accountSwitches")
    return None if sw is None else sw > 0


def slot_flag(slot: dict, changes):
    """Section 5's confounder flag for a slot: True with an account switch or a scopeDate on or after a change, False
    otherwise, None when the account-switch count or the scopeDate is missing (not computable)."""
    sw, date = slot.get("accountSwitches"), slot.get("scopeDate")
    if sw is not None and sw > 0:
        return True
    if sw is None or date is None:
        return None
    return any(POST_DAYS[0] <= c["date"] <= date for c in changes)


def gate(hid: str, pre_units, post_units, measure, n_pre_min: int, n_post_min: int, flags, fid_key=None, needs=(),
         guard=None, primary=None, tags=(), extra=None):
    """The ordered gate of PREREG section 7, regions 2 to 7, for one hypothesis.
    pre_units, post_units: the delivered units of the hypothesis's class and periods. measure(unit) -> value or None.
    flags(unit) -> True (confounder flag), False, or None when the confounder evidence is missing. fid_key: the unit's
    fidelity key (None for H-39). needs: (name, fn) pairs of further evidence a post unit must carry, fn(unit) -> value
    or None. guard(included) -> breached (bool) or None when not computable. primary(pre_values, post_values, included)
    -> bool or None. extra: a dict, or a function of the included post units, merged into the result.
    Evidence rule (issue 6): evidence absent from every post unit reads U2; a post unit missing any piece is excluded
    with the reason and counted in `excluded`; the rest face the minimum (U1). A missing fidelity is never exposure, a
    missing confounder count or date is never "unflagged", a missing guard observation is never zero."""
    out = {"id": hid, "tags": list(tags), "nPre": len(pre_units), "postUnits": len(post_units), "excluded": {}}
    reqs = ([("fidelity", lambda u: fidelity(u, fid_key))] if fid_key else []) + [("confounder evidence", flags)]
    reqs += list(needs) + [("primary measure", measure)]
    for name, fn in reqs:
        if post_units and all(fn(u) is None for u in post_units):
            out.update(verdict="UNRESOLVED", region=3, subCase="U2", nPost=0, note="the %s is missing from every post unit" % name)
            return out
    included = []
    for u in post_units:
        reason = None
        for name, fn in reqs:
            v = fn(u)
            if v is None:
                reason = name + " missing"
                break
            if name == "fidelity" and v is False:
                reason = "no intervention"
                break
        if reason:
            out["excluded"][reason] = out["excluded"].get(reason, 0) + 1
        else:
            included.append(u)
    out["nPost"] = len(included)
    pre_have = [v for v in (measure(u) for u in pre_units) if v is not None]
    post_have = [measure(u) for u in included]
    out["preValues"], out["postValues"] = pre_have, post_have
    if extra:
        out.update(extra(included) if callable(extra) else extra)
    if len(pre_have) < n_pre_min or len(post_have) < n_post_min:
        out.update(verdict="UNRESOLVED", region=2, subCase="U1", note="units below the minimum")
        return out
    if included and all(flags(u) for u in included):
        out.update(verdict="UNRESOLVED", region=4, subCase="U3", note="every post unit carries a confounder flag")
        return out
    if guard is not None:
        g = guard(included)
        if g is None:
            out.update(verdict="UNRESOLVED", region=3, subCase="U2", note="the guard measure is not computable")
            return out
        if g:
            out.update(verdict="NOT SUPPORTED", region=5, note="guard breached")
            return out
    ok = primary(pre_have, post_have, included)
    if ok is None:
        out.update(verdict="UNRESOLVED", region=3, subCase="U2", note="the primary is not computable (a secondary measure below its minimum, or a pre median of zero)")
        return out
    out.update(verdict="SUPPORTED" if ok else "NOT SUPPORTED", region=6 if ok else 7)
    return out


def evaluate(d: dict) -> dict:
    changes = d["changes"]
    mon_days = [x for x in d["days"] if x["session"] == MONITOR]
    pre_days = [x for x in mon_days if PRE_DAYS[0] <= x["date"] <= PRE_DAYS[1]]
    post_days = [x for x in mon_days if POST_DAYS[0] <= x["date"] <= POST_DAYS[1]]
    dflag = lambda u: day_flag(u, changes)
    sflag = lambda u: slot_flag(u, changes)
    results = {}
    # H-37 (fidelity excludes post units only: a pre unit carries no intervention by definition, preflight note)
    cpm = lambda u: (None if u.get("calls") is None or not u.get("messagesHandled") else u["calls"] / u["messagesHandled"])
    ctx = lambda u: u.get("meanContextTokens")

    def h37_primary(pre, post, included):
        a = ratio_ok(median(post), median(pre), T["h37"])
        pre_c = [ctx(u) for u in pre_days if ctx(u) is not None]
        post_c = [ctx(u) for u in included if ctx(u) is not None]
        if len(pre_c) < MIN["days"] or len(post_c) < MIN["days"]:
            return None
        b = ratio_ok(median(post_c), median(pre_c), T["h37"])
        return None if a is None or b is None else (a and b)
    results["H-37"] = gate("H-37", pre_days, post_days, cpm, MIN["days"], MIN["days"], dflag, fid_key="h1", primary=h37_primary, tags=("bundle H1-H3", "no guard"))
    # H-38: the guard's observations are the post windows; a post day without a window ending on it carries no overshoot evidence
    post_windows = [w for w in d["windows"] if POST_DAYS[0] <= w["windowEnd"][:10] <= POST_DAYS[1]]
    window_days = {w["windowEnd"][:10] for w in post_windows}
    overshoots = [w for w in post_windows if w["usageAtStop"] > T["overshoot"]]
    unconfounded = [w for w in overshoots if not (w.get("fanOut3PlusStartUsage") is not None and w["fanOut3PlusStartUsage"] >= T["fanout"])]
    pre_overshoots = [w for w in d["windows"] if PRE_DAYS[0] <= w["windowEnd"][:10] <= PRE_DAYS[1] and w["usageAtStop"] > T["overshoot"]]
    results["H-38"] = gate("H-38", pre_days, post_days, lambda u: u.get("watchCalls"), 0, MIN["days"], dflag, fid_key="h2",
                           needs=(("overshoot evidence (a 5-hour window ending on the day)", lambda u: True if u["date"] in window_days else None),),
                           guard=lambda included: len(unconfounded) > 0, primary=lambda pre, post, included: all(le(v, T["h38_watch"]) for v in post),
                           tags=("bundle H1-H3", "manipulation check"),
                           extra={"overshootsPost": len(overshoots), "confoundedPost": len(overshoots) - len(unconfounded), "overshootsPre": len(pre_overshoots), "postWindows": len(post_windows)})
    # H-39
    ev = [e for e in d["loadEvents"] if not e["otherAppLoad"]]
    pre_ev = [e for e in ev if LOAD_PRE[0] <= e["at"] < LOAD_PRE[1]]
    post_ev = [e for e in ev if LOAD_POST_FROM <= e["at"] <= STOP_DATE + "T24:00"]
    enough = (len(pre_ev) >= MIN["load"] and len(post_ev) >= MIN["load"]
              and sum(e["kind"] == "verify-start" for e in pre_ev) >= MIN["load_verify"] and sum(e["kind"] == "verify-start" for e in post_ev) >= MIN["load_verify"])
    per_kind = {k: {"pre": median([e["load1"] for e in pre_ev if e["kind"] == k]), "post": median([e["load1"] for e in post_ev if e["kind"] == k])} for k in KINDS}
    results["H-39"] = gate("H-39", pre_ev if enough else [], post_ev if enough else [], lambda e: e["load1"], MIN["load"], MIN["load"], lambda e: False,
                           primary=lambda pre, post, included: ratio_ok(median(post), median(pre), T["h39"]), tags=("bundle H1-H3", "no guard"), extra={"perKind": per_kind})
    # slots
    slots = {s["slot"]: s for s in d["slots"]}
    pre40 = [slots[n] for n in range(H40_PRE[0], H40_PRE[1] + 1) if n in slots]
    post_slots = [slots[n] for n in range(POST_SLOTS[0], POST_SLOTS[1] + 1) if n in slots]
    pre_def = [defects(s) for s in pre40 if defects(s) is not None]
    post_def_all = [defects(s) for s in post_slots]

    def defect_guard(post_set):
        post_d = [defects(s) for s in post_set if defects(s) is not None]
        if len(pre_def) < MIN["guard_pre"] or len(post_d) < MIN["post_slots"]:
            return None
        return not le(median(post_d), median(pre_def))
    rounds_max = lambda s: (None if s.get("series") is None else max([x["rounds"] for x in s["series"]] or [0]))
    baseline = [slots[288]] if 288 in slots else []
    results["H-40"] = gate("H-40", pre40, post_slots, rounds_max, MIN["h40_pre"], MIN["post_slots"], sflag, fid_key="h4",
                           guard=defect_guard, primary=lambda pre, post, included: all(v <= T["h40_rounds"] for v in post), tags=("manipulation check",))
    results["H-41"] = gate("H-41", baseline, post_slots, lambda s: s.get("c2Builds"), 0, MIN["post_slots"], sflag, fid_key="h5",
                           guard=defect_guard, primary=lambda pre, post, included: le(median(post), T["h41_c2"]),
                           tags=("single baseline", "baseline partly treated", "bundle H5-H8"))
    hours = lambda s: s.get("scopeToPacketR1Hours")

    def h42_primary(pre, post, included):
        h = [hours(s) for s in included if hours(s) is not None]
        if len(h) < MIN["post_slots"]:
            return None
        return le(median(post), T["h42_rulings"]) and le(median(h), T["h42_hours"])
    results["H-42"] = gate("H-42", baseline, post_slots, lambda s: s.get("rulingsWaited"), 0, MIN["post_slots"], sflag, fid_key="h6",
                           guard=defect_guard, primary=h42_primary, tags=("single baseline", "baseline partly treated", "bundle H5-H8"))
    major = lambda included: [s["machineryMajor"] for s in included if s.get("machineryMajor") is not None]
    results["H-43"] = gate("H-43", [], [s for s in post_slots if s["kind"] == "product"], lambda s: s.get("machineryRepairs"), 0, MIN["h43_post"], sflag, fid_key="h7",
                           guard=lambda included: (None if len(major(included)) < MIN["h43_post"] else not le(median(major(included)), T["h43_major"])),
                           primary=lambda pre, post, included: all(v == 0 for v in post), tags=("single baseline", "baseline partly treated", "bundle H5-H8"))
    slips = lambda included: [s["lostDetailSlips"] for s in included if s.get("lostDetailSlips") is not None]
    mins = lambda s: s.get("stepMinutesMean")

    def h44_primary(pre, post, included):
        m = [mins(s) for s in included if mins(s) is not None]
        if len(m) < MIN["post_slots"]:
            return None
        return le(median(post), T["h44_ctx"]) and le(median(m), T["h44_min"])
    results["H-44"] = gate("H-44", baseline, post_slots, lambda s: s.get("r00MeanContextTokens"), 0, MIN["post_slots"], sflag, fid_key="h8",
                           guard=lambda included: (None if len(slips(included)) < MIN["post_slots"] else not le(median(slips(included)), T["h44_slips"])),
                           primary=h44_primary, tags=("single baseline", "baseline partly treated", "bundle H5-H8", "manipulation check"),
                           extra=lambda included: {"slipsTotalPost": sum(slips(included))})
    results["descriptive"] = {"postDefectsPerSlot": post_def_all, "excludedDay": EXCLUDED_DAY, "changes": len(changes)}
    return results


# ---------------------------------------------------------------- preflight fixtures (known answers)
def base_delivery():
    days, windows, events, slots = [], [], [], []
    for i in range(7):
        pre = "2026-11-%02d" % (5 + i)
        post = "2026-11-%02d" % (13 + i)
        days.append({"date": pre, "session": MONITOR, "calls": 1000, "messagesHandled": 100, "meanContextTokens": 400000, "watchFirings": 72,
                     "watchCalls": 144, "accountSwitches": 0, "fanOuts3Plus": 0, "fidelity": {"h1": False, "h2": False, "h3": False}})
        days.append({"date": post, "session": MONITOR, "calls": 700, "messagesHandled": 100, "meanContextTokens": 280000, "watchFirings": 24,
                     "watchCalls": 40, "accountSwitches": 0, "fanOuts3Plus": 0, "fidelity": {"h1": True, "h2": True, "h3": True}})
        windows.append({"windowEnd": post + "T05:00", "usageAtStop": 90, "fanOut3PlusStartUsage": None})
        windows.append({"windowEnd": pre + "T05:00", "usageAtStop": 97, "fanOut3PlusStartUsage": None})
    windows.append({"windowEnd": "2026-11-14T22:00", "usageAtStop": 100, "fanOut3PlusStartUsage": 81})
    for i in range(10):
        kind = KINDS[i % 3]
        events.append({"at": "2026-11-%02dT10:%02d" % (6 + i // 3, 10 * (i % 3)), "kind": kind, "load1": 12.0, "load5": 11.0, "load15": 10.0, "otherAppLoad": False})
        events.append({"at": "2026-11-%02dT10:%02d" % (13 + i // 3, 10 * (i % 3)), "kind": kind, "load1": 8.0, "load5": 8.0, "load15": 8.0, "otherAppLoad": False})
    events.append({"at": "2026-11-15T12:00", "kind": "push", "load1": 30.0, "load5": 20.0, "load15": 15.0, "otherAppLoad": True})
    for n in range(285, 293):
        post = n >= 289
        slots.append({"slot": n, "scopeDate": "2026-11-%02d" % (6 + n - 285) if not post else "2026-11-%02d" % (13 + n - 289), "kind": "product", "shape": {"k": 1, "parts": 2, "machinery": False},
                      "fidelity": {k: post for k in ("h4", "h5", "h6", "h7", "h8")},
                      "c2Builds": 3 if post else 5, "dryC2Runs": 1 if post else 0,
                      "series": [{"name": "contract", "rounds": 2 if post else 3}, {"name": "source", "rounds": 2 if post else 3}, {"name": "PACKET", "rounds": 1}],
                      "rulingsWaited": 8 if post else 16, "scopeToPacketR1Hours": 5.0 if post else 8.5,
                      "laterDefects": {"oracleFailures": 1 if post else 1, "packetMajor": 0 if post else 1, "postMergeIssues7d": 0},
                      "machineryRepairs": 0 if post else 1, "machineryMajor": 3 if post else 4,
                      "r00Calls": 500, "r00MeanContextTokens": 300000 if post else 487000, "stepMinutesMean": 15.0 if post else 18.9,
                      "lostDetailSlips": 0, "accountSwitches": 0, "fanOuts3Plus": 0, "ownerWindowShare": 0.5})
    return {"schemaVersion": SCHEMA, "producedAt": "2026-11-20", "period": {"from": "2026-11-05", "to": "2026-11-19"}, "clock": "host-local",
            "producer": {"meterSha256": PINS["meterSha256"] + "0" * 48, "extractSha256": PINS["extractSha256"] + "0" * 48},
            "days": days, "windows": windows, "loadEvents": events, "slots": slots, "changes": []}


def set_post(doc, cls, field, value, where=lambda item: True):
    for item in doc[cls]:
        if where(item):
            item[field] = value


def is_post_day(x):
    return x["session"] == MONITOR and POST_DAYS[0] <= x["date"] <= POST_DAYS[1]


def is_post_slot(s):
    return POST_SLOTS[0] <= s["slot"] <= POST_SLOTS[1]


def fixtures():
    ALL = dict.fromkeys(HYPOTHESES, "SUPPORTED")
    out = []
    f = base_delivery(); out.append(("F1-positive-control", f, dict(ALL)))
    f = base_delivery()
    set_post(f, "days", "calls", 900, is_post_day)
    for s in f["slots"]:
        if is_post_slot(s):
            s["laterDefects"] = {"oracleFailures": 3, "packetMajor": 2, "postMergeIssues7d": 0}; s["machineryMajor"] = 6; s["lostDetailSlips"] = 1
    for e in f["loadEvents"]:
        if e["at"] >= LOAD_POST_FROM:
            e["load1"] = 10.8
    f["windows"].append({"windowEnd": "2026-11-16T22:00", "usageAtStop": 100, "fanOut3PlusStartUsage": None})
    out.append(("F2-negative-control", f, dict.fromkeys(HYPOTHESES, "NOT SUPPORTED")))
    f = base_delivery()
    set_post(f, "days", "calls", 750, is_post_day); set_post(f, "days", "meanContextTokens", 300000, is_post_day); set_post(f, "days", "watchCalls", 50, is_post_day)
    for e in f["loadEvents"]:
        if e["at"] >= LOAD_POST_FROM:
            e["load1"] = 8.4
    for s in f["slots"]:
        if is_post_slot(s):
            s.update(c2Builds=3, rulingsWaited=10, scopeToPacketR1Hours=6.0, machineryMajor=4, r00MeanContextTokens=365000, stepMinutesMean=16.07,
                     laterDefects={"oracleFailures": 2, "packetMajor": 0, "postMergeIssues7d": 0})
    out.append(("F3-boundary-at", f, dict(ALL)))
    f = base_delivery()
    set_post(f, "days", "calls", 751, is_post_day); set_post(f, "days", "watchCalls", 51, is_post_day)
    for e in f["loadEvents"]:
        if e["at"] >= LOAD_POST_FROM:
            e["load1"] = 8.41
    for s in f["slots"]:
        if is_post_slot(s):
            s.update(c2Builds=4, rulingsWaited=11, scopeToPacketR1Hours=6.01, r00MeanContextTokens=365001, stepMinutesMean=16.08)
            s["series"][0]["rounds"] = 3; s["machineryRepairs"] = 1
    out.append(("F4-boundary-above", f, dict.fromkeys(HYPOTHESES, "NOT SUPPORTED")))
    f = base_delivery()
    f["days"] = [x for x in f["days"] if not (is_post_day(x) and x["date"] > "2026-11-14")]
    f["slots"] = [s for s in f["slots"] if s["slot"] <= 290]
    f["loadEvents"] = [e for e in f["loadEvents"] if not (e["at"] >= LOAD_POST_FROM and e["at"] > "2026-11-15")]
    out.append(("F5-below-minimum-n", f, dict.fromkeys(HYPOTHESES, "UNRESOLVED U1")))
    f = base_delivery()
    for x in f["days"]:
        if is_post_day(x):
            del x["messagesHandled"]
    for s in f["slots"]:
        if is_post_slot(s):
            for k in ("c2Builds", "rulingsWaited", "r00MeanContextTokens"):
                del s[k]
    exp = dict(ALL); exp.update({"H-37": "UNRESOLVED U2", "H-41": "UNRESOLVED U2", "H-42": "UNRESOLVED U2", "H-44": "UNRESOLVED U2"})
    out.append(("F6-missing-measure", f, exp))
    f = base_delivery()
    set_post(f, "days", "accountSwitches", 1, is_post_day); set_post(f, "slots", "accountSwitches", 1, is_post_slot)
    exp = dict.fromkeys(HYPOTHESES, "UNRESOLVED U3"); exp["H-39"] = "SUPPORTED"
    out.append(("F7-all-flagged", f, exp))
    f = base_delivery()
    f["changes"].append({"date": "2026-11-13", "kind": "monitor restart"})
    exp = dict.fromkeys(HYPOTHESES, "UNRESOLVED U3"); exp["H-39"] = "SUPPORTED"
    out.append(("F8-change-flags-days-and-slots", f, exp))
    f = base_delivery()
    f["days"].append({"date": EXCLUDED_DAY, "session": MONITOR, "calls": 99999, "messagesHandled": 1, "meanContextTokens": 999999, "watchCalls": 999, "fidelity": {"h1": True}})
    for s in f["slots"]:
        if s["slot"] == 288:
            s["series"] = [{"name": "contract", "rounds": 9}]
        if s["slot"] in (291, 292):
            s["fidelity"]["h5"] = False
    exp = dict(ALL); exp["H-41"] = "UNRESOLVED U1"
    out.append(("F9-excluded-and-fidelity", f, exp, {"H-41": {"no intervention": 2}}))
    # issue 6 (2026-11-13): missing evidence never reads as exposure, as "unconfounded" or as zero incidents
    f = base_delivery()
    for x in f["days"]:
        if is_post_day(x):
            del x["fidelity"]
    for s in f["slots"]:
        if is_post_slot(s):
            s["fidelity"] = {}
    exp = dict.fromkeys(HYPOTHESES, "UNRESOLVED U2"); exp["H-39"] = "SUPPORTED"
    out.append(("F10-missing-fidelity", f, exp))
    f = base_delivery()
    f["changes"].append({"date": "2026-11-13", "kind": "monitor restart"})
    for s in f["slots"]:
        if is_post_slot(s):
            del s["scopeDate"]
    exp = dict.fromkeys(HYPOTHESES, "UNRESOLVED U2"); exp.update({"H-37": "UNRESOLVED U3", "H-38": "UNRESOLVED U3", "H-39": "SUPPORTED"})
    out.append(("F11-missing-scopeDate", f, exp))
    f = base_delivery()
    f["windows"] = []
    exp = dict(ALL); exp["H-38"] = "UNRESOLVED U2"
    out.append(("F12-guard-no-observations", f, exp))
    f = base_delivery()
    for x in f["days"]:
        if x["date"] == "2026-11-13":
            del x["accountSwitches"]
    for s in f["slots"]:
        if s["slot"] == 289:
            s["fidelity"] = {"h4": None, "h5": None, "h6": None, "h7": None, "h8": None}
        if s["slot"] == 290:
            del s["scopeDate"]
    exp = dict(ALL); exp.update(dict.fromkeys(("H-40", "H-41", "H-42", "H-43", "H-44"), "UNRESOLVED U1"))
    out.append(("F13-partial-evidence", f, exp, {"H-37": {"confounder evidence missing": 1}, "H-38": {"confounder evidence missing": 1},
                                                 "H-40": {"fidelity missing": 1, "confounder evidence missing": 1}, "H-43": {"fidelity missing": 1, "confounder evidence missing": 1}}))
    f = base_delivery()
    f["windows"] = [w for w in f["windows"] if not (POST_DAYS[0] <= w["windowEnd"][:10] <= POST_DAYS[1]) or w["windowEnd"][:10] in ("2026-11-13", "2026-11-14")]
    exp = dict(ALL); exp["H-38"] = "UNRESOLVED U1"
    out.append(("F14-partial-window-coverage", f, exp, {"H-38": {"overshoot evidence (a 5-hour window ending on the day) missing": 5}}))
    return out


def reject_fixtures():
    out = []
    f = base_delivery(); del f["slots"]; out.append(("R1-missing-class", f, "MISSING_CLASS"))
    f = base_delivery(); f["slots"].append(dict(f["slots"][0])); out.append(("R2-duplicate-unit", f, "DUPLICATE"))
    f = base_delivery(); f["producer"]["meterSha256"] = "0" * 64; out.append(("R3-producer-pin", f, "PRODUCER_PIN"))
    f = base_delivery(); f["slots"][5]["c2Builds"] = "3"; out.append(("R4-type", f, "TYPE"))
    f = base_delivery(); f["loadEvents"][0]["kind"] = "deploy"; out.append(("R5-enum", f, "ENUM"))
    f = base_delivery(); f["slots"][5]["scopeDate"] = "13/11/2026"; out.append(("R6-invalid-date", f, "TYPE"))
    return out


def verdict_word(r: dict) -> str:
    return r["verdict"] + (" " + r["subCase"] if r.get("subCase") else "")


def preflight(prereg: Path, fixture_dir: Path, out_json: Path) -> int:
    assert sha256(prereg).startswith(PREREG_PREFIX), "PREREG digest"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    rows, failures = [], 0
    for row in fixtures():
        name, doc, expected = row[:3]
        excluded_expected = row[3] if len(row) > 3 else None
        path = fixture_dir / (name + ".json")
        path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        results = evaluate(load_deliveries([path]))
        got = {h: verdict_word(r) for h, r in results.items() if h in HYPOTHESES}
        ok = got == expected
        record = {"fixture": name, "sha256": sha256(path), "expected": expected, "got": got}
        if excluded_expected is not None:
            got_excluded = {h: results[h]["excluded"] for h in excluded_expected}
            ok = ok and got_excluded == excluded_expected
            record.update(expectedExcluded=excluded_expected, gotExcluded=got_excluded)
        failures += int(not ok)
        record["ok"] = ok
        rows.append(record)
    for name, doc, code in reject_fixtures():
        path = fixture_dir / (name + ".json")
        path.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        try:
            load_deliveries([path]); got = "ACCEPTED"
        except Reject as e:
            got = str(e).split(":")[0]
        ok = got == code
        failures += int(not ok)
        rows.append({"fixture": name, "sha256": sha256(path), "expected": code, "got": got, "ok": ok})
    record = {"schemaVersion": "planeon.research.preflight/v1", "experiment": "RL-23", "preregSha256": sha256(prereg),
              "evaluatorSha256": sha256(Path(__file__)), "date": datetime.date.today().isoformat(), "fixtures": rows,
              "status": "PASS" if failures == 0 else "FAIL"}
    out_json.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("PREFLIGHT %s: %d fixtures, %d failed" % (record["status"], len(rows), failures))
    for r in rows:
        if not r["ok"]:
            print("  " + r["fixture"], "expected", r["expected"], "got", r["got"], r.get("expectedExcluded", ""), r.get("gotExcluded", ""))
    return 0 if failures == 0 else 1


def ledger(prereg: Path, preflight_json: Path, deliveries, results: dict) -> dict:
    me = sha256(Path(__file__))
    evidence = [{"evidenceId": "E0", "kind": "PREREG", "contentDigest": "sha256:" + sha256(prereg), "producedBy": "Research-Lab.RL-23.PREREG"},
                {"evidenceId": "E1", "kind": "EVALUATOR", "contentDigest": "sha256:" + me, "producedBy": "Research-Lab.rl23_factory"},
                {"evidenceId": "E2", "kind": "PREFLIGHT", "contentDigest": "sha256:" + sha256(preflight_json), "producedBy": "Research-Lab.rl23_factory.preflight"}]
    for i, p in enumerate(deliveries):
        evidence.append({"evidenceId": "D%d" % (i + 1), "kind": "DELIVERY", "contentDigest": "sha256:" + sha256(Path(p)), "producedBy": "Lane-Monitor.aggregates"})
    claims, checks, verdicts = [], [], []
    for n, h in enumerate(HYPOTHESES):
        r = results[h]
        word = verdict_word(r)
        v = {"SUPPORTED": "PASS", "NOT SUPPORTED": "FAIL"}.get(r["verdict"], "UNRESOLVED")
        value = json.dumps({k: r[k] for k in r if k not in ("id",)}, sort_keys=True)
        claims.append({"claimId": h, "requirement": "PREREG v4 section 2, " + h, "delivered": word, "rolloutValues": {"run-001": value}})
        checks.append({"checkId": "C%d" % (n + 1), "claimId": h, "contextId": "lab", "kind": "GATE", "target": "PREREG section 7 region", "establishedValue": value,
                       "outcome": v, "sequence": n + 1, "evidence": [e["evidenceId"] for e in evidence]})
        verdicts.append({"claimId": h, "verdict": v, "value": word, "checks": ["C%d" % (n + 1)]})
    status = "FAIL" if any(x["verdict"] == "FAIL" for x in verdicts) else "UNRESOLVED" if any(x["verdict"] == "UNRESOLVED" for x in verdicts) else "PASS"
    return {"schemaVersion": "planeon.internal.verdict-ledger/v1", "ledgerId": "RL-23-RESULTS-v1", "subject": {"scopeDigest": "sha256:" + sha256(prereg)},
            "supersedes": None, "rollouts": ["run-001"], "contexts": [{"contextId": "lab", "inheritsFrom": [], "role": "EVALUATOR"}],
            "evidence": evidence, "claims": claims, "checks": checks, "claimVerdicts": verdicts,
            "verdict": {"status": status, "scores": {x["claimId"]: x["value"] for x in verdicts}, "evidenceRefs": [e["contentDigest"] for e in evidence],
                        "unresolvedChecks": [x["checks"][0] for x in verdicts if x["verdict"] == "UNRESOLVED"], "policyViolations": [],
                        "producedBy": "Research-Lab.rl23_factory " + me[:8]},
            "descriptive": results["descriptive"]}


def coverage(d: dict) -> str:
    """Counts of post units whose evidence is absent (issue 6), printed at acceptance so a gap is visible at delivery,
    not at the stop date; no values."""
    days = [x for x in d["days"] if x["session"] == MONITOR and POST_DAYS[0] <= x["date"] <= POST_DAYS[1]]
    slots = [s for s in d["slots"] if POST_SLOTS[0] <= s["slot"] <= POST_SLOTS[1]]
    window_days = {w["windowEnd"][:10] for w in d["windows"]}
    miss = lambda units, f: sum(u.get(f) is None for u in units)
    fid_miss = lambda units, keys: sum(any(fidelity(u, k) is None for k in keys) for u in units)
    return ("COVERAGE: post days %d (fidelity missing %d, accountSwitches missing %d, no window %d); post slots %d (fidelity missing %d, "
            "scopeDate missing %d, accountSwitches missing %d); changes %d"
            % (len(days), fid_miss(days, ("h1", "h2", "h3")), miss(days, "accountSwitches"), sum(x["date"] not in window_days for x in days),
               len(slots), fid_miss(slots, ("h4", "h5", "h6", "h7", "h8")), miss(slots, "scopeDate"), miss(slots, "accountSwitches"), len(d["changes"])))


def main(argv) -> int:
    if len(argv) >= 2 and argv[0] == "check":
        try:
            d = load_deliveries(argv[1:])
        except Reject as e:
            print("REJECT " + str(e)); return 1
        print("ACCEPTED: " + ", ".join("%s %d" % (k, len(v)) for k, v in d.items()))
        print(coverage(d)); return 0
    if len(argv) == 4 and argv[0] == "preflight":
        return preflight(Path(argv[1]), Path(argv[2]), Path(argv[3]))
    if len(argv) >= 5 and argv[0] == "evaluate":
        prereg, pf, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
        if not sha256(prereg).startswith(PREREG_PREFIX):
            print("STOP: PREREG digest is not " + PREREG_PREFIX); return 2
        record = json.loads(pf.read_text(encoding="utf-8"))
        if record.get("status") != "PASS" or record.get("evaluatorSha256") != sha256(Path(__file__)):
            print("STOP: preflight not PASS for this evaluator"); return 2
        try:
            d = load_deliveries(argv[4:])
        except Reject as e:
            print("REJECT " + str(e)); return 1
        results = evaluate(d)
        out.write_text(json.dumps(ledger(prereg, pf, argv[4:], results), indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print("LEDGER written: " + "; ".join("%s %s" % (h, verdict_word(results[h])) for h in HYPOTHESES)); return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
