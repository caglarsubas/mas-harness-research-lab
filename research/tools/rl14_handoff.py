"""RL-14 (H-28, observational half): typed versus free-text resume blocks in the handoff files and the dated
rule lines that follow them. usage: python3 -I -B rl14_handoff.py HANDOFF_DIR OUT.json [--inventory]   (counts only;
no line of any handoff file is printed or copied; the lab's own lane file is excluded by name)."""
import datetime
import hashlib
import json
import pathlib
import re
import sys

HEAD = re.compile(r"^##+\s+(?:Resume here|HANDOVER\s+\d+|Resume prompts|RESUME)\b.*?(\d{4}-\d\d-\d\d)", re.I)
DIGEST = re.compile(r"\b[0-9a-f]{8}\b")
LINEPIN = re.compile(r"\blines?\s+\d+(?:\s*[-–]\s*\d+)?\b", re.I)
MONID = re.compile(r"\bMON-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")
DATE = re.compile(r"\b2026-\d\d-\d\d\b")
EXCLUDE = {"LANE-RESEARCH-LAB.md"}
INCLUDE = re.compile(r"^LANE-.*\.md$")  # the lanes' own files only (PREREG v2: the monitor's STATE.md is a different role)


def blocks_of(path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    # first dated appearance of each MON identifier in this file (PREREG v2: recaps and repeats count once, at their first date)
    first = {}
    for l in lines:
        if DATE.search(l):
            d = min(DATE.findall(l))
            for m in MONID.findall(l):
                if m not in first or d < first[m]:
                    first[m] = d
    dated = sorted((d, m) for m, d in first.items())
    heads = [(i, HEAD.match(l).group(1)) for i, l in enumerate(lines) if HEAD.match(l)]
    out = []
    for n, (i, date) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        body = lines[i:end]
        words = sum(len(l.split()) for l in body)
        digests = set(m for l in body for m in DIGEST.findall(l) if not m.isdigit())
        pins = sum(len(LINEPIN.findall(l)) for l in body)
        named = set(m for l in body for m in MONID.findall(l))
        out.append({"file": path.name, "date": date, "start": i, "words": words, "digests": len(digests), "linePins": pins, "monIdsNamed": len(named), "_named": sorted(named)})
    return out, dated


def main(handoff, out_path, inventory):
    files = sorted(p for p in pathlib.Path(handoff).glob("*.md") if p.name not in EXCLUDE and INCLUDE.match(p.name))
    rec = {"files": [], "blocks": []}
    dated_by_file = {}
    for p in files:
        b, dated = blocks_of(p)
        dated_by_file[p.name] = dated
        rec["files"].append({"file": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "blocks": len(b), "datedMonIds": len(dated)})
        rec["blocks"].extend(b)
    # windows: consecutive blocks within a file, ordered by block date; the window opened by block k ends at block k+1's date
    windows = []
    for name in sorted({b["file"] for b in rec["blocks"]}):
        bs = sorted((b for b in rec["blocks"] if b["file"] == name), key=lambda b: (b["date"], b["start"]))
        for k in range(len(bs) - 1):
            d0 = datetime.date.fromisoformat(bs[k]["date"]); d1 = datetime.date.fromisoformat(bs[k + 1]["date"])
            days = (d1 - d0).days
            opened, closed = bs[k]["date"], bs[k + 1]["date"]
            known = set(bs[k]["_named"])
            following = sum(1 for d, m in dated_by_file[name] if opened < d <= closed and m not in known)
            windows.append({"file": name, "opened": opened, "closed": closed, "days": days,
                            "typedness": round(100.0 * (bs[k]["digests"] + bs[k]["linePins"]) / max(1, bs[k]["words"]), 3),
                            "typednessDigestsOnly": round(100.0 * bs[k]["digests"] / max(1, bs[k]["words"]), 3),
                            "typed": bs[k]["digests"] + bs[k]["linePins"] > 0,
                            "newMonIds": following, "ratePerDay": round(following / days, 4) if days >= 1 else None})
    rec["windows"] = windows
    for b in rec["blocks"]:
        b.pop("_named", None)
    if inventory:
        print(json.dumps({"files": len(files), "blocks": len(rec["blocks"]), "blocksPerFile": {f["file"]: f["blocks"] for f in rec["files"]},
                          "windows": len(windows), "windowsWithDays": sum(1 for w in windows if w["days"] >= 1),
                          "typedBlocks": sum(1 for b in rec["blocks"] if b["digests"] + b["linePins"] > 0)}, indent=1))
        return
    json.dump(rec, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("blocks %d windows %d" % (len(rec["blocks"]), len(windows)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--inventory" in sys.argv)
