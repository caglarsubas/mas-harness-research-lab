#!/usr/bin/env python3
"""Render the living Research-Lab page.

usage: python3 -I -B research/build_research.py [--force-snapshot] [--page-only] [--check]   (run from the bridge root)

--page-only renders research.html from the existing research.json and history.json (the data files stay byte-equal);
--check renders the same way in memory and prints SAME or DIFFER against research.html (exit 1 on DIFFER).

Reads research/README.md (the charter), research/hypotheses/REGISTER.md (the two tables), every
research/experiments/RL-nn/ folder (PREREG.md, RESULTS.json, REPORT.md, MAPPING.md, runs/*.md, data/*), the lab's
tools, research/reads/*.md (design reads and asks), the register's milestone rows, and handoff/LANE-RESEARCH-LAB.md's "Resume here" block; writes research/research.json (the data record with a
sha256 prefix per source file), appends a snapshot to research/history.json when the counts or verdicts changed, and
writes the self-contained research/research.html, which wears the shared sheet design/tokens/pages.css inlined unchanged
(Design-UX's; the build fails closed without it or without design/pages/glossary-families.md). Standard library only; no
local path and no handle enters the page: every link is relative to research/. The monitor's checkpoint carries the three
files with research/**.

Rule I (owner, SC-D2; in force 2026-11-17): a full build also writes research/progress/README.md and the S files from the data
record and the hand-kept scope map research/progress/scopes.json (every experiment in exactly one scope, or the build stops), so
the owner's reading view cannot fall behind the records; --check compares them too. The lane file keeps its resume block and the
last ten entries; older ones live in research/resume-log-archive.md, which the resume log page reads beside the lane file.
"""
from __future__ import annotations

import datetime
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "research"
LANE = ROOT / "handoff" / "LANE-RESEARCH-LAB.md"
ARCHIVE = RES / "resume-log-archive.md"
SCOPES = RES / "progress" / "scopes.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split(" | ")]


# ------------------------------------------------------------------------------------------------- markdown (small) --

def inline(text: str) -> str:
    text = esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    # a fingerprint in prose (8 to 64 hex characters with a digit and a letter) is set as code, small and monospace, never as running text (S3)
    text = re.sub(r"(?<![\w<>/])(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{8,64}\b(?![^<]*</code>)", lambda m: "<code>%s</code>" % m.group(0), text)
    return text


def md_to_html(md: str, base: str = "") -> str:
    """Paragraphs, headings, bullet lists, pipe tables, bold and code spans; nothing else."""
    out, para, table, items = [], [], [], []

    def flush_para():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para))); para.clear()

    def flush_table():
        if table:
            rows = [cells(r) for r in table if not re.match(r"^\s*\|?\s*-{2,}", r)]
            if rows:
                head = "".join("<th>%s</th>" % inline(c) for c in rows[0])
                body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in rows[1:])
                out.append("<table class=\"md\"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (head, body))
            table.clear()

    def flush_items():
        if items:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(i) for i in items)); items.clear()

    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("|"):
            flush_para(); flush_items(); table.append(line); continue
        flush_table()
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_para(); flush_items(); level = min(len(m.group(1)) + 2, 5)
            out.append("<h%d>%s</h%d>" % (level, inline(m.group(2)), level)); continue
        if re.match(r"^\s*[-*]\s+", line):
            flush_para(); items.append(re.sub(r"^\s*[-*]\s+", "", line)); continue
        if re.match(r"^\s+\S", line) and items:
            items[-1] += " " + line.strip(); continue
        if not line.strip():
            flush_para(); flush_items(); continue
        flush_items(); para.append(line.strip())
    flush_para(); flush_table(); flush_items()
    return "\n".join(out)


# ----------------------------------------------------------------------------------------------------- the sources --

def register() -> dict:
    path = RES / "hypotheses" / "REGISTER.md"
    text = path.read_text(encoding="utf-8")
    hyps, exps, milestones = [], [], []
    for line in text.splitlines():
        if line.startswith("| H-"):
            c = cells(line)
            if len(c) >= 7:
                hyps.append({"id": c[0], "hypothesis": c[1], "kind": c[2], "section": c[3], "inputs": c[4], "status": c[5], "firstStep": c[6],
                             "stream": c[7] if len(c) > 7 else "", "pe": c[8] if len(c) > 8 else "", "outside1": c[9] if len(c) > 9 else "", "outside2": c[10] if len(c) > 10 else ""})
        elif line.startswith("| M-"):
            c = cells(line)
            if len(c) >= 6:
                milestones.append({"id": c[0], "gate": c[1], "releaseGate": c[2], "lead": c[3], "supporting": c[4], "closesWhen": c[5]})
        elif line.startswith("| RL-"):
            c = cells(line)
            if len(c) >= 5:
                exps.append({"id": c[0], "hypothesis": c[1], "folder": c[2], "state": c[3], "prereg": c[4], "effort": c[5] if len(c) > 5 else ""})
    return {"digest": digest(path), "hypotheses": hyps, "rows": exps, "milestones": milestones}


def report_sections(md: str) -> dict:
    """The one-page report's lead-in paragraphs by their bold labels."""
    found, current = {}, None
    for block in re.split(r"\n\s*\n", md):
        m = re.match(r"^\*\*([^*]+?)\.?\*\*\s*(.*)$", block.strip(), re.S)
        if m:
            label = m.group(1).split("(")[0].split(":")[0].strip()
            key = {"Asked": "asked", "Measured": "measured", "What it means": "means", "What it does not show": "limits", "Proposal": "proposal", "For the W03 note": "note", "Disclosure first": "disclosure", "Context, not gated": "context", "Makespan, descriptive": "context", "What the rounds show": "context", "What the findings show": "context"}.get(label)
            if key is None and label.lower().startswith("verdict"):
                key = "verdict"
            if key is None and label.startswith("H-"):
                key = "context"
            current = key or "other"
            found[current] = (found.get(current, "") + "\n\n" + block.strip()).strip()
        elif block.strip().startswith("|") and current:
            found[current] = found[current] + "\n\n" + block.strip()
    return found


def experiments(reg_rows: list[dict]) -> list[dict]:
    out = []
    for folder in sorted((RES / "experiments").glob("RL-*")):
        if not folder.is_dir():
            continue
        exp = {"id": folder.name, "files": {}, "runs": [], "data": [], "claims": [], "checks": [], "verdict": None, "unresolved": [], "scores": {}}
        for name in ("PREREG.md", "RESULTS.json", "REPORT.md", "MAPPING.md", "PREREG.v1.md", "PREREG.v2.md", "RESULTS.v1.json", "REPORT.v1.md"):
            p = folder / name
            if p.exists():
                exp["files"][name] = digest(p)
        for p in sorted((folder / "runs").glob("*.md")) if (folder / "runs").exists() else []:
            first = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
            exp["runs"].append({"file": "runs/" + p.name, "digest": digest(p), "title": first})
        for p in sorted((folder / "data").glob("*")) if (folder / "data").exists() else []:
            if p.is_file():
                exp["data"].append({"file": "data/" + p.name, "digest": digest(p), "bytes": p.stat().st_size})
        prereg = folder / "PREREG.md"
        if prereg.exists():
            text = prereg.read_text(encoding="utf-8")
            exp["title"] = text.splitlines()[0].lstrip("# ").strip()
            m = re.search(r"^Status:\s*(.+?)(?:\n\n|\Z)", text, re.S | re.M)
            exp["preregStatus"] = " ".join(m.group(1).split()) if m else ""
        results = folder / "RESULTS.json"
        if results.exists():
            led = json.loads(results.read_text(encoding="utf-8"))
            exp["verdict"] = led["verdict"]["status"]
            exp["unresolved"] = led["verdict"].get("unresolvedChecks", [])
            exp["scores"] = led["verdict"].get("scores", {})
            exp["claims"] = [{"id": c["claimId"], "verdict": c["verdict"], "value": c.get("value", "")} for c in led.get("claimVerdicts", [])]
            exp["checks"] = [{"id": c["checkId"], "claim": c["claimId"], "outcome": c["outcome"], "target": c.get("target"), "value": c.get("establishedValue", "")} for c in led.get("checks", [])]
            exp["supersedes"] = led.get("supersedes")
            exp["ledgerId"] = led.get("ledgerId")
        report = folder / "REPORT.md"
        if report.exists():
            text = report.read_text(encoding="utf-8")
            exp["reportTitle"] = text.splitlines()[0].lstrip("# ").strip()
            exp["report"] = report_sections(text)
        exp["state"] = "COMPLETED" if results.exists() else ("ONGOING" if prereg.exists() else "PLANNED")
        row = next((r for r in reg_rows if r["id"] == folder.name), None)
        exp["hypothesisIds"] = re.findall(r"\bH-\d{2}\b", (row or {}).get("hypothesis", "")) or re.findall(r"\bH-\d{2}\b", exp.get("title", ""))
        exp["registerLine"] = (row or {}).get("state", "")
        dates = sorted(set(re.findall(r"\b2026-\d\d-\d\d\b", "\n".join((folder / "runs" / r["file"].split("/")[-1]).read_text(encoding="utf-8") for r in exp["runs"]) if exp["runs"] else "")))
        exp["dates"] = dates
        out.append(exp)
    return out


def charter() -> dict:
    text = (RES / "README.md").read_text(encoding="utf-8")
    sections, current, buf = {}, "lead", []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            sections[current] = "\n".join(buf).strip(); current, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    sections[current] = "\n".join(buf).strip()
    return {"digest": digest(RES / "README.md"), "title": text.splitlines()[0].lstrip("# ").strip(), "sections": sections}


def lane() -> dict:
    text = LANE.read_text(encoding="utf-8")
    # the header is the rest of the heading line up to its last ")", so nested parentheses inside it are kept
    m = re.search(r"^## Resume here \(([^\n]*)\)[ \t]*\n(.*?)(?=^## )", text, re.S | re.M)
    header, body = (m.group(1), m.group(2)) if m else ("", "")
    hu = header.upper()
    status = "ACTIVE" if "ACTIVE" in hu else ("PAUSED" if "PAUSED" in hu or "STANDING BY" in body.upper() else "ACTIVE")
    out = {"digest": digest(LANE), "header": header, "status": status, "body": body.strip()}
    if ARCHIVE.exists():  # rule I: entries older than the lane file's last ten, text unchanged, under a one-line title
        out["archive"] = {"digest": digest(ARCHIVE), "body": ARCHIVE.read_text(encoding="utf-8").partition("\n")[2].strip()}
    return out


def tools() -> list[dict]:
    return [{"file": "tools/" + p.name, "digest": digest(p), "doc": (re.search(r'"""(.*?)(?:\n|""")', p.read_text(encoding="utf-8"), re.S) or [None, ""])[1].strip()[:160]} for p in sorted((RES / "tools").glob("*.py"))]


def reads() -> list[dict]:
    out = []
    for p in sorted((RES / "progress").glob("*.md")) + (sorted((RES / "reads").glob("*.md")) if (RES / "reads").exists() else []):
        out.append({"file": ("progress/" if p.parent.name == "progress" else "reads/") + p.name, "digest": digest(p), "title": p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()})
    return out


def bridge_commit() -> str:
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True, env={"PATH": "/usr/bin:/bin", "GIT_OPTIONAL_LOCKS": "0"}).stdout.strip()
    except Exception:
        return "unknown"


# ------------------------------------------------------------------------------------------------------- the record --

def build_record() -> dict:
    reg = register(); exps = experiments(reg["rows"])
    by_h = {}
    for e in exps:
        for h in e["hypothesisIds"]:
            by_h.setdefault(h, []).append(e["id"])
    for h in reg["hypotheses"]:
        h["experiments"] = by_h.get(h["id"], [])
        h["bucket"] = ("BLOCKED" if h["status"].upper().startswith("BLOCKED") else "READY") if not h["experiments"] else "RUN"
    counts = {"hypotheses": len(reg["hypotheses"]), "withExperiment": sum(1 for h in reg["hypotheses"] if h["experiments"]),
              "ready": sum(1 for h in reg["hypotheses"] if h["bucket"] == "READY"), "blocked": sum(1 for h in reg["hypotheses"] if h["bucket"] == "BLOCKED"),
              "experiments": len(exps), "completed": sum(1 for e in exps if e["state"] == "COMPLETED"), "ongoing": sum(1 for e in exps if e["state"] == "ONGOING"),
              "verdicts": {v: sum(1 for e in exps if e["verdict"] == v) for v in ("PASS", "FAIL", "UNRESOLVED")},
              "runs": sum(len(e["runs"]) for e in exps)}
    return {"title": "Research-Lab living page", "generatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), "bridgeCommit": bridge_commit(),
            "lane": lane(), "charter": charter(), "register": reg, "experiments": exps, "tools": tools(), "reads": reads(), "counts": counts}


def update_history(data: dict, force: bool) -> list[dict]:
    path = RES / "history.json"
    history = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    snap = {"generatedAt": data["generatedAt"], "bridgeCommit": data["bridgeCommit"], "lane": data["lane"]["status"], "counts": data["counts"],
            "verdicts": {e["id"]: e["verdict"] for e in data["experiments"]}, "registerDigest": data["register"]["digest"]}
    last = history[-1] if history else None
    if force or last is None or any(last.get(k) != snap[k] for k in ("lane", "counts", "verdicts", "registerDigest")):
        history.append(snap); path.write_text(json.dumps(history, indent=1, sort_keys=True), encoding="utf-8")
    return history


# ------------------------------------------------------------------------------------- the progress view (rule I) --
# progress/README.md and the S files come from the data record and the hand-kept map progress/scopes.json; hand-written context
# in the map carries its date. No timestamp enters the files: the same record and map give the same bytes.

def cut(text: object, limit: int) -> str:
    text = " ".join(str(text).replace(" | ", " / ").split())
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "…"


def result_line(e: dict) -> str:
    """A finished experiment's result in one line: its report's verdict paragraph without markup, else its register entry."""
    text = re.sub(r"\*\*", "", e.get("report", {}).get("verdict", "")) or e.get("registerLine", "")
    text = re.sub(r"\s*\(RESULTS\.json[^)]*\)", "", re.sub(r"^Verdict[:.]?\s*", "", text.strip()))
    return cut(text, 320)


def progress_files(data: dict) -> dict:
    """File name to text for research/progress/, from the record and the scope map; stops when an experiment has no scope."""
    doc = json.loads(SCOPES.read_text(encoding="utf-8"))
    exps = {e["id"]: e for e in data["experiments"]}; hyps = {h["id"]: h for h in data["register"]["hypotheses"]}
    effort = {r["id"]: r.get("effort", "") for r in data["register"]["rows"]}
    placed = [x for s in doc["scopes"] for x in s["experiments"]]
    problems = {"without a scope": sorted(set(exps) - set(placed)), "unknown experiment": sorted(set(placed) - set(exps)),
                "in two scopes": sorted({x for x in placed if placed.count(x) > 1}),
                "unknown hypothesis": sorted({h for s in doc["scopes"] for h in s["hypotheses"]} - set(hyps))}
    if any(problems.values()):
        fail("progress/scopes.json: " + "; ".join("%s %s" % (k, ", ".join(v)) for k, v in problems.items() if v))
    head = ("Generated by `research/build_research.py` from the data record `research.json` (register `%s`) and the scope map\n"
            "`progress/scopes.json`; never edited by hand: change the records or the map and rebuild. Hand-written context carries its date."
            % data["register"]["digest"])
    word = {"RUN": "tested", "READY": "ready", "BLOCKED": "blocked"}
    files, table, in_scope = {}, [], set()
    for s in doc["scopes"]:
        mine = [exps[x] for x in s["experiments"]]; r, date = s["reading"], s["readingDate"]
        ids = sorted(set(s["hypotheses"]) | {h for e in mine for h in e["hypothesisIds"] if h in hyps})
        in_scope.update(ids)
        done = [e for e in mine if e["state"] == "COMPLETED"]; open_ = [e for e in mine if e["state"] != "COMPLETED"]
        tally = {v: sum(1 for e in done if e["verdict"] == v) for v in ("PASS", "FAIL", "UNRESOLVED")}
        buckets = {b: sum(1 for h in ids if hyps[h]["bucket"] == b) for b in word}
        later = [e["id"] for e in mine if e["state"] != "COMPLETED" or (e["dates"] and max(e["dates"]) > date)]
        since = (" (later run records or unfinished work: %s)" % ", ".join(later)) if later else ""
        out = ["# " + s["title"], "", head, "", "**Question.** " + s["question"], "", "**Observe (context written %s).** %s" % (date, r["observe"]), "",
               "**Hypotheses.** %d in this scope: %d tested, %d ready, %d blocked." % (len(ids), buckets["RUN"], buckets["READY"], buckets["BLOCKED"]), ""]
        if r.get("hypotheses"):
            out += ["Reading of %s: %s" % (date, r["hypotheses"]), ""]
        out += ["| id | hypothesis | status | experiments |", "|---|---|---|---|"]
        out += ["| %s | %s | %s | %s |" % (h, cut(hyps[h]["hypothesis"], 220), word[hyps[h]["bucket"]], ", ".join(hyps[h]["experiments"]) or "none") for h in ids]
        out += ["", "**Data (context written %s).** %s" % (date, r["data"]), ""]
        if s.get("listReads"):
            reads_ = [x for x in data.get("reads", []) if x["file"].startswith("reads/")]
            out += ["**Experiments.** None of its own; the %d design reads and asks on file:" % len(reads_), ""]
            if r.get("experiments"):
                out += ["Reading of %s: %s" % (date, r["experiments"]), ""]
            # no digest column: a read may list this file's digest (the bridge-changes read does), and the two must not chase each other
            out += ["| file | title |", "|---|---|"] + ["| `%s` | %s |" % (x["file"], cut(x["title"], 200)) for x in reads_]
        else:
            out += ["**Experiments.** %d: %d finished (%d pass, %d fail, %d unresolved), %d not finished." % (len(mine), len(done), tally["PASS"], tally["FAIL"], tally["UNRESOLVED"], len(open_)), "",
                    "| id | tests | state | verdict | last run | effort (rule J: preparation / review / run) |", "|---|---|---|---|---|---|"]
            out += ["| %s | %s | %s | %s | %s | %s |" % (e["id"], ", ".join(e["hypothesisIds"]) or "none", WORDS.get(e["state"], (e["state"], ""))[0], e["verdict"] or "none yet",
                                                       (e["dates"][-1] if e["dates"] and e["state"] == "COMPLETED" else "not yet"), cut(effort.get(e["id"], "").split(" (")[0], 200) or "n/r") for e in mine]
        out += ["", "**Results and proof.** " + ("One line per finished experiment, from its report's verdict paragraph or its register entry:" if done else "No finished experiment in this scope."), ""]
        out += ["- %s (%s): %s" % (e["id"], e["verdict"], result_line(e)) for e in done]
        out += ([""] if done else []) + ["Reading of %s%s: %s" % (date, since, r["results"]), "", "**Next.** From the register:", ""]
        nxt = ["- Not finished: %s: %s" % (e["id"], cut(e.get("registerLine", ""), 300)) for e in open_]
        nxt += ["- Ready, no experiment yet: %s: %s" % (h, cut(hyps[h]["firstStep"], 220)) for h in ids if hyps[h]["bucket"] == "READY"]
        nxt += ["- Blocked: %s: %s" % (h, cut(hyps[h]["status"], 220)) for h in ids if hyps[h]["bucket"] == "BLOCKED"]
        out += (nxt or ["- Nothing open in the register for this scope."]) + ["", "Reading of %s%s: %s" % (date, since, r["next"]), ""]
        files[s["file"]] = "\n".join(out)
        table.append("| %s | %s | `%s` | %s | %d: %d tested, %d ready, %d blocked |" % (s["id"], s["question"], s["file"], ", ".join("%s %s" % (e["id"], e["verdict"] or "running") for e in mine) or "none (reads only)",
                                                                              len(ids), buckets["RUN"], buckets["READY"], buckets["BLOCKED"]))
    rest = sorted(set(hyps) - in_scope)
    files["README.md"] = "\n".join(["# Research-Lab progress by scope (the owner's reading view; generated at every page build)", "", head, "", doc["intro"], "",
                                     "| scope | question | document | experiments | hypotheses |", "|---|---|---|---|---|"] + table + ["",
                                     "Hypotheses not in a scope yet (%d): %s." % (len(rest), ", ".join(rest) or "none"), "",
                                     "Every document has the same six sections (Observe, Hypotheses, Data, Experiments, Results and proof, Next). The tables and",
                                     "the one-line results follow the records; a \"Reading of\" paragraph is the lab's own summary on that date and names the",
                                     "experiments with later run records or unfinished work. The living page `research/research.html` lists these documents beside the experiments.", ""])
    return files


# ------------------------------------------------------------------------------------------------------- rendering --
# The page wears the shared sheet design/tokens/pages.css (Design-UX's; P1 of visionary/PAGES-PREP-56.md): inlined unchanged
# in the first style block, its digest prefix in a meta tag and a comment; page-own rules follow in a second block and use the
# tokens only (no colour literal, nothing under 12 px). The page is script-free: views and detail panels open by :target, the
# colour mode by the three radios. The build fails closed without the sheet or the glossary file.

SHEET = ROOT / "design" / "tokens" / "pages.css"
GLOSSARY = ROOT / "design" / "pages" / "glossary-families.md"
VIEWS = (("start", "Start here"), ("experiments", "Experiments"), ("hypotheses", "Hypotheses"), ("approach", "Approach"), ("history", "History"))
# the research page's code families (glossary-families.md, research table, from number 21); the wording is the lab's (S3)
FAMILIES = (
    ("experiment", "Experiment", "one preregistered study in the lab's folder, frozen before any run, with its run records, verdict ledger and report."),
    ("hypothesis", "Hypothesis", "one falsifiable statement of the register, with the experiments that test it and its status."),
    ("milestone-gate", "Milestone gate", "a decision gate of the programme that closes on a verdict of its lead hypothesis, never on a date."),
    ("claim", "Claim", "one clause of a hypothesis that an experiment's ledger judges supported, contradicted or unresolved."),
    ("check", "Check", "one deterministic test of a verdict ledger, with its bound and the value it measured."),
    ("stream", "Stream", "the research roadmap stream a hypothesis belongs to, with its heavy-queue class in brackets."),
)
# stored words -> display labels (S3); the old page showed the stored words
WORDS = {"COMPLETED": ("Finished", "is-ok"), "ONGOING": ("Running", "is-info"), "PLANNED": ("Planned", ""),
         "PASS": ("Pass", "is-ok"), "FAIL": ("Fail", "is-closed"), "UNRESOLVED": ("Unresolved", "is-open"), "NONE": ("Pending", ""),
         "RUN": ("Tested", "is-ok"), "READY": ("Ready", "is-info"), "BLOCKED": ("Blocked", "is-closed"), "OWNER": ("Waiting on you", "is-open"),
         "SUPPORTED": ("Supported", "is-ok"), "CONTRADICTED": ("Contradicted", "is-closed"), "NEW_VALUE_ESTABLISHED": ("New value", "is-info"),
         "INCONCLUSIVE": ("Inconclusive", "is-open"), "PAUSED": ("Paused", "is-open"), "ACTIVE": ("Active", "is-ok")}


def fail(message: str) -> None:
    raise SystemExit("build_research: " + message)


def read_sheet() -> tuple[str, str]:
    if not SHEET.exists():
        fail("the shared sheet %s is missing (P1 condition 1: the build fails closed)" % SHEET.relative_to(ROOT))
    raw = SHEET.read_bytes()
    return raw.decode("utf-8"), hashlib.sha256(raw).hexdigest()[:16]


def read_glossary() -> tuple[dict, list[str]]:
    """The family rows of the glossary file by key, and the research keys still missing there. A research row whose family or
    sentence differs from FAMILIES fails the build; a missing row is reported (Design-UX adds the rows before the lock applies)."""
    if not GLOSSARY.exists():
        fail("the glossary family list %s is missing" % GLOSSARY.relative_to(ROOT))
    rows = re.findall(r"^\| \d+ \| ([^|]+?) \| `([a-z-]+)` \| ([^|]+?) \|$", GLOSSARY.read_text(encoding="utf-8"), re.M)
    gl = {key: (family.strip(), sentence.strip()) for family, key, sentence in rows}
    for key, family, sentence in FAMILIES:
        if key in gl and gl[key] != (family, sentence):
            fail("glossary row %s differs from the page's wording" % key)
    return gl, [key for key, _, _ in FAMILIES if key not in gl]


def glossary_css() -> str:
    return "".join('.pg-term[data-g="%s"]{--pg-tip:"%s: %s"}\n' % (k, f, s) for k, f, s in FAMILIES)


def term(code: str, key: str) -> str:
    return '<span class="pg-term" tabindex="0" data-g="%s">%s</span>' % (key, esc(code))


def code(value: str) -> str:
    return "<code>%s</code>" % esc(value)


def chip(word: str, href: str | None = None) -> str:
    label, cls = WORDS.get(word, (word, ""))
    tag, at = ("a", ' href="%s"' % esc(href)) if href else ("span", "")
    return '<%s class="pg-chip%s"%s>%s</%s>' % (tag, (" " + cls) if cls else "", at, esc(label), tag)


PAGE_CSS = """
code{font:var(--pg-fs-small) var(--mono);background:var(--surface-hover);padding:0 var(--sp-1);border-radius:var(--r-sm)}
table.md,table.ledger{width:100%;border-collapse:collapse;margin:var(--sp-2) 0 var(--sp-3);font-size:var(--fs-caption)}
table.md th,table.ledger th{text-align:left;padding:var(--sp-1) var(--sp-2);border-bottom:1px solid var(--line);color:var(--muted);font-size:var(--pg-fs-small);font-weight:600}
table.md td,table.ledger td{padding:var(--sp-1) var(--sp-2);border-bottom:1px solid var(--line);vertical-align:top}
.pg-prose p,.pg-prose ul,.pg-prose h4,.pg-prose h5{margin:var(--sp-2) 0}
.pg-prose h4,.pg-prose h5{font-family:var(--display);font-weight:600;color:var(--ink-strong);font-size:var(--fs-data)}
.pg-view h2{margin-top:var(--sp-6)} .pg-view h3{margin-top:var(--sp-4)}
.pg-panel h3{margin-top:var(--sp-4)} .pg-panel dl{display:grid;grid-template-columns:minmax(110px,max-content) minmax(0,1fr);gap:var(--sp-1) var(--sp-4);margin:var(--sp-2) 0}
.pg-panel dt{color:var(--muted)} .pg-panel dd{margin:0}
.files a{display:inline-block;margin:0 var(--sp-3) var(--sp-1) 0;text-decoration:none} .files code{margin-left:var(--sp-1)}
ul.log{margin:0;padding-left:var(--sp-4)} ul.log li{margin:var(--sp-2) 0;max-width:var(--pg-measure)}
.pg-list td.pg-name{min-width:220px} .pg-list td.pg-name .pg-term{display:block;margin-top:2px}
.ask-text{min-width:0} .ask-text p{margin-top:var(--sp-1)}
/* views by :target, no script: Start here shows while nothing else is targeted; a panel target opens its view */
.pg-view{display:none} #v-start{display:block}
.pg-view:target,.pg-view:has(:target){display:block}
body:has(.pg-view:not(#v-start):target) #v-start,body:has(.pg-view:not(#v-start) :target) #v-start{display:none}
.pg-tabs>a[href="#v-start"]{border-bottom-color:var(--focus);color:var(--ink-strong);font-weight:600}
body:has(.pg-view:not(#v-start):target) .pg-tabs>a[href="#v-start"],body:has(.pg-view:not(#v-start) :target) .pg-tabs>a[href="#v-start"]{border-bottom-color:transparent;color:var(--muted);font-weight:400}
"""


def page_css() -> str:
    css = PAGE_CSS + "".join('body:has(#v-%s:target) .pg-tabs>a[href="#v-%s"],body:has(#v-%s :target) .pg-tabs>a[href="#v-%s"]{border-bottom-color:var(--focus);color:var(--ink-strong);font-weight:600}\n' % (k, k, k, k) for k, _ in VIEWS[1:])
    literal = re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(", css)
    if literal:
        fail("a colour literal in the page-own rules: %r" % literal.group(0))
    small = [float(v) for v in re.findall(r"font(?:-size)?\s*:[^;}]*?(\d+(?:\.\d+)?)px", css) if float(v) < 12]
    if small:
        fail("a font size under 12 px in the page-own rules: %s" % small)
    return css


def effort_cells() -> dict:
    """The register's effort column (rule J; recorded from RL-23 on) by experiment id, read at page time: the data record keeps
    the five register columns it always had, so the record stays byte-equal across the redesign."""
    out = {}
    for line in (RES / "hypotheses" / "REGISTER.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("| RL-"):
            c = cells(line)
            if len(c) >= 6 and c[5] and not c[5].startswith("n/r"):
                out[c[0]] = c[5]
    return out


def newest_line(header: str) -> str:
    """The newest dated milestone of the lane header (its last '; YYYY-MM-DD ...' segment), cut to one line."""
    segs = [s.strip() for s in header.split("; ") if re.match(r"^\d{4}-\d{2}-\d{2}\b", s.strip())]
    text = re.sub(r"\s*\b[0-9a-f]{8,64}\b", "", segs[-1] if segs else header)
    if len(text) > 170:
        text = text[:170].rsplit(" ", 1)[0] + "…"
    return text


def hyp_links(ids: list[str]) -> str:
    return " ".join('<a href="#%s">%s</a>' % (esc(h), code(h)) for h in ids) or "–"


def exp_panel(e: dict, effort: dict) -> str:
    rep = e.get("report", {})
    body = ['<aside class="pg-panel is-target" id="%s" aria-label="Experiment %s"><header><h2>%s %s</h2><a class="pg-btn" href="#v-experiments">Close</a></header>'
            % (esc(e["id"]), esc(e["id"]), inline(e.get("title", e["id"])), term(e["id"], "experiment")),
            '<p class="pg-small pg-muted">%s %s · dates %s · runs %d</p>' % (chip(e["state"]), chip(e["verdict"] or "NONE"), esc(", ".join(e["dates"]) or "–"), len(e["runs"])),
            '<dl><dt>Tests</dt><dd>%s</dd><dt>Preregistration</dt><dd>%s</dd>%s</dl>'
            % (hyp_links(e["hypothesisIds"]), inline(e.get("preregStatus", "") or "–"), ("<dt>Effort</dt><dd>%s</dd>" % inline(effort[e["id"]])) if e["id"] in effort else "")]
    for key, title in (("asked", "Asked"), ("measured", "Measured"), ("verdict", "Verdict"), ("context", "Context"), ("means", "What it means"), ("limits", "What it does not show"), ("note", "For the note"), ("proposal", "Proposal"), ("disclosure", "Disclosure")):
        if rep.get(key):
            body.append('<h3>%s</h3><div class="pg-prose">%s</div>' % (title, md_to_html(rep[key])))
    if e["claims"]:
        body.append('<h3>Claim verdicts</h3><p class="pg-small pg-muted">ledger %s%s</p><table class="ledger"><thead><tr><th>claim</th><th>verdict</th><th>value</th></tr></thead><tbody>%s</tbody></table>'
                    % (code(e.get("ledgerId", "") or "–"), (", supersedes " + code(e["supersedes"][7:15])) if e.get("supersedes") else "",
                       "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (code(cl["id"]), chip(cl["verdict"]), inline(cl["value"])) for cl in e["claims"])))
    if e["checks"]:
        body.append('<details class="pg-more"><summary>Checks (%d), unresolved: %s</summary><table class="ledger"><thead><tr><th>check</th><th>claim</th><th>outcome</th><th>established value</th></tr></thead><tbody>%s</tbody></table></details>'
                    % (len(e["checks"]), esc(", ".join(e["unresolved"]) or "none"),
                       "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (code(ch["id"]), code(ch["claim"]), chip(ch["outcome"]), inline(ch["value"])) for ch in e["checks"])))
    links = "".join('<a href="experiments/%s/%s">%s <code>%s</code></a>' % (esc(e["id"]), esc(f), esc(f), d) for f, d in e["files"].items())
    links += "".join('<a href="experiments/%s/%s">%s <code>%s</code></a>' % (esc(e["id"]), esc(r["file"]), esc(r["file"]), r["digest"]) for r in e["runs"])
    links += "".join('<a href="experiments/%s/%s">%s <code>%s</code></a>' % (esc(e["id"]), esc(d["file"]), esc(d["file"]), d["digest"]) for d in e["data"])
    body.append('<details class="pg-more"><summary>Evidence: the register entry, the files and their sha256 prefixes</summary><p class="pg-small">%s</p><div class="files">%s</div></details></aside>' % (inline(e.get("registerLine", "") or "–"), links))
    return "".join(body)


def hyp_panel(h: dict, owner: bool) -> str:
    rows = (("Kind", esc(h["kind"])), ("Section", inline(h["section"])), ("Inputs", inline(h["inputs"])), ("First step", inline(h["firstStep"])),
            ("Stream", term(h["stream"], "stream") if h.get("stream") else "–"), ("P/E score", esc(h.get("pe", "") or "–")),
            ("Outside RS-1", esc(h.get("outside1", "") or "–")), ("Outside RS-2", esc(h.get("outside2", "") or "–")),
            ("Status", chip("OWNER" if owner else h["bucket"])),
            ("Experiments", " ".join('<a href="#%s">%s</a>' % (esc(x), code(x)) for x in h["experiments"]) or "none yet"))
    return ('<aside class="pg-panel is-target" id="%s" aria-label="Hypothesis %s"><header><h2>Hypothesis %s</h2><a class="pg-btn" href="#v-hypotheses">Close</a></header>'
            '<p class="pg-prose">%s</p><dl>%s</dl><details class="pg-more"><summary>Status note from the register</summary><p class="pg-small">%s</p></details></aside>'
            % (esc(h["id"]), esc(h["id"]), term(h["id"], "hypothesis"), inline(h["hypothesis"]), "".join("<dt>%s</dt><dd>%s</dd>" % r for r in rows), inline(h["status"])))


def log_entries(body: str) -> tuple[str, list[str]]:
    """The lane body split into its preamble and its dated entries (newest first)."""
    pre, entries = [], []
    for raw in body.splitlines():
        if raw.startswith("- 20"):
            entries.append(raw[2:])
        elif raw.startswith("  ") and entries:
            entries[-1] += " " + raw.strip()
        else:
            pre.append(raw)
    entries.sort(key=lambda t: t[:10], reverse=True)
    return "\n".join(pre).strip(), entries


def frame(title: str, sheet: str, sheet_digest: str, updated: str, body: str, own_css: str = "") -> str:
    top = ('<header class="pg-top"><div class="pg-wrap"><span class="pg-brand">Harness-Onion</span><nav class="pg-pages" aria-label="Pages">'
           '<a href="../roadmap/roadmap.html">Roadmap</a><a href="../roadmap/architecture.html">Architecture</a><a href="research.html" aria-current="page">Research</a></nav>'
           '<div class="pg-tools"><span class="pg-updated">Updated %s</span><a class="pg-btn" href="research.html#gloss">Glossary</a>'
           '<fieldset class="pg-mode"><legend class="pg-sr">Colour mode</legend><input type="radio" name="pg-mode" id="pg-mode-auto" value="auto" checked><label for="pg-mode-auto">Auto</label>'
           '<input type="radio" name="pg-mode" id="pg-mode-light" value="light"><label for="pg-mode-light">Light</label><input type="radio" name="pg-mode" id="pg-mode-dark" value="dark"><label for="pg-mode-dark">Dark</label></fieldset></div></div></header>') % esc(updated)
    foot = '<footer class="pg-foot">Research-Lab living page · the data record research.json and the snapshots history.json beside it are its source of truth; the shared style sheet is pages.css <code>%s</code>.</footer>' % sheet_digest[:8]
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            '<title>%s</title><meta name="pages-css" content="%s"><meta name="color-scheme" content="light dark">\n'
            '<style>/* pages.css %s (design/tokens/pages.css, inlined unchanged) */\n%s</style>\n<style>/* page-own rules */\n%s%s</style></head>\n'
            '<body>%s<div class="pg-wrap">%s%s</div></body></html>\n' % (esc(title), sheet_digest, sheet_digest, sheet, glossary_css(), own_css, top, body, foot))


def render_log(data: dict, sheet: str, sheet_digest: str) -> str:
    """research/resume-log.html: the lane file's whole Resume here block, newest entry first (History keeps the ten newest)."""
    lane_ = data["lane"]; pre, entries = log_entries(lane_["body"]); arch = lane_.get("archive") or {}
    old_pre, older = log_entries(arch.get("body", ""))
    kept = len(entries); entries = sorted(entries + older, key=lambda t: t[:10], reverse=True)
    archived = ('<h2>Archived notes</h2><p class="pg-small pg-muted">The lane file keeps its resume block and the last ten entries (%d now); %d older entries and the superseded notes below live in resume-log-archive.md <code>%s</code>, text unchanged.</p>'
                '<details class="pg-more"><summary>Show the archived notes</summary><div class="pg-prose">%s</div></details>' % (kept, len(older), arch["digest"], md_to_html(old_pre))) if arch else ""
    body = ('<section class="pg-view"><h1>Resume log</h1><p class="pg-lead">The lane file\'s Resume here block (<code>%s</code>), every dated entry newest first; <a href="research.html#v-history">back to History</a>.</p>'
            '<h2>The note</h2><p class="pg-prose">%s</p><h2>Preamble</h2><div class="pg-prose">%s</div><h2>Entries (%d)</h2><ul class="log">%s</ul>%s</section>'
            % (lane_["digest"], esc(lane_["header"]), md_to_html(pre), len(entries), "".join("<li>%s</li>" % inline(t) for t in entries), archived))
    return frame("Research-Lab resume log", sheet, sheet_digest, data["generatedAt"], body, page_css())


def render(data: dict, history: list[dict], sheet: str, sheet_digest: str) -> str:
    c = data["counts"]; lane_ = data["lane"]; exps = data["experiments"]; hyps = data["register"]["hypotheses"]; effort = effort_cells()
    owner_ids = {h["id"] for h in hyps if h["bucket"] == "BLOCKED" and "owner" in h["status"].lower()}
    by_id = {e["id"]: e for e in exps}
    finished = [e for e in exps if e["state"] == "COMPLETED"]
    last = max(finished, key=lambda e: (max(e["dates"]) if e["dates"] else "", e["id"])) if finished else None
    # ---- start here
    state = WORDS.get(lane_["status"], (lane_["status"], ""))[0]
    asks = "".join('<div class="pg-ask"><div class="ask-text"><strong>%s</strong> %s<p class="pg-small pg-muted pg-clamp">%s</p></div><a class="pg-btn is-primary" href="#%s">Open</a></div>'
                   % (term(h["id"], "hypothesis"), inline(h["hypothesis"]), inline(re.sub(r"\b[0-9a-f]{8,64}\b", "…", h["status"])), esc(h["id"])) for h in hyps if h["id"] in owner_ids)
    kpis = "".join('<div class="pg-kpi"><b>%s</b><span class="pg-small pg-muted">%s</span></div>' % (n, l) for n, l in (
        ('<a class="pg-count" href="#v-experiments">%d</a>' % c["experiments"], "experiments"), ("%d" % c["completed"], "finished"), ("%d" % c["ongoing"], "running"),
        ("%d" % c["verdicts"]["PASS"], "pass"), ("%d" % c["verdicts"]["FAIL"], "fail"), ("%d" % c["verdicts"]["UNRESOLVED"], "unresolved"), ("%d" % c["runs"], "run records")))
    cost = ("Effort recorded from RL-23 on (rule J; preparation, review and run minutes): " + " · ".join('<a href="#%s">%s</a> %s' % (esc(k), code(k), inline(v.split(" (")[0])) for k, v in sorted(effort.items()))
            + ". Earlier experiments carry no effort figure; every run so far was light work on this host, heavy-run seconds 0 except RL-03's heavy slot (3 GOs).") if effort else "No effort figure is recorded yet."
    start = ('<section class="pg-view" id="v-start"><h1>Where the lab stands</h1><p class="pg-lead">%s. %s</p>'
             '<div class="pg-grid"><div><div class="pg-card is-attn"><header><h2>Waiting on you</h2><a class="pg-count" href="#v-hypotheses">%d</a></header>%s</div>'
             '<div class="pg-card"><header><h2>Hypotheses</h2><a class="pg-count" href="#v-hypotheses">%d</a></header>'
             '<div class="pg-line"><span>With an experiment</span><a class="pg-count" href="#v-hypotheses">%d</a></div><div class="pg-line"><span>Ready, no experiment yet</span><a class="pg-count" href="#v-hypotheses">%d</a></div>'
             '<div class="pg-line"><span>Blocked on a named item or answer</span><a class="pg-count" href="#v-hypotheses">%d</a></div></div></div>'
             '<div><div class="pg-card"><header><h2>Last finished experiment</h2>%s</header><p class="pg-prose">%s</p></div>'
             '<div class="pg-card"><header><h2>Cost to date</h2></header><p class="pg-small">%s</p></div></div></div>'
             '<div class="pg-kpis">%s</div>'
             '<h2>Status note</h2><p class="pg-clamp pg-prose">%s</p><details class="pg-more"><summary>Show the full note</summary><p class="pg-prose">%s</p></details>'
             '<p class="pg-small pg-muted">Generated %s at bridge %s.</p><details class="pg-more"><summary>Sources and their sha256 prefixes</summary><p class="pg-small">register <code>%s</code> · charter <code>%s</code> · lane file <code>%s</code></p></details></section>'
             % (esc(state), inline(newest_line(lane_["header"])), len(owner_ids), asks or '<p class="pg-muted">nothing</p>',
                c["hypotheses"], c["withExperiment"], c["ready"], c["blocked"],
                ('<a href="#%s">%s</a>' % (esc(last["id"]), term(last["id"], "experiment"))) if last else "", (inline(one_line(last)) + (" (%s)" % esc(last["dates"][-1]) if last["dates"] else "")) if last else "none yet",
                cost, kpis, esc(lane_["header"]), esc(lane_["header"]), esc(data["generatedAt"]), esc(data["bridgeCommit"]), data["register"]["digest"], data["charter"]["digest"], lane_["digest"]))
    # ---- experiments
    rows = "".join('<tr><td class="pg-name"><a href="#%s">%s</a> %s</td><td class="is-meta" data-label="Tests">%s</td><td class="is-meta" data-label="State">%s</td><td class="is-meta" data-label="Verdict">%s</td><td class="is-meta pg-num" data-label="Last run">%s</td></tr>'
                   % (esc(e["id"]), inline(e.get("title", e["id"])), term(e["id"], "experiment"), hyp_links(e["hypothesisIds"]), chip(e["state"]), chip(e["verdict"] or "NONE"), esc(e["dates"][-1] if e["dates"] else "–")) for e in exps)
    experiments = ('<section class="pg-view" id="v-experiments"><h1>Experiments</h1><p class="pg-lead">Each folder holds PREREG (frozen before any run), run records, RESULTS in the verdict-ledger form and a one-page REPORT; the name opens the detail, and its Evidence lists the files relative to this page.</p>'
                   '<div class="pg-split"><table class="pg-list"><thead><tr><th>experiment</th><th>tests</th><th>state</th><th>verdict</th><th>last run</th></tr></thead><tbody>%s</tbody></table>%s</div></section>'
                   % (rows, "".join(exp_panel(e, effort) for e in exps)))
    # ---- hypotheses
    hrows = "".join('<tr><td class="pg-name"><a href="#%s">%s</a> %s</td><td class="is-meta" data-label="Kind">%s</td><td class="is-meta" data-label="Stream">%s</td><td class="is-meta" data-label="Status">%s</td><td class="is-meta" data-label="Experiments">%s</td></tr>'
                    % (esc(h["id"]), inline(h["hypothesis"]), term(h["id"], "hypothesis"), esc(h["kind"]), code(h["stream"]) if h.get("stream") else "–", chip("OWNER" if h["id"] in owner_ids else h["bucket"]),
                       " ".join('<a href="#%s">%s</a>' % (esc(x), code(x)) for x in h["experiments"]) or "–") for h in hyps)
    ms = data["register"].get("milestones", [])
    mtable = ('<h2>Milestones</h2><p class="pg-small pg-muted">The four decision gates, tied to a lead hypothesis; a milestone closes on a verdict, not a date.</p><table class="ledger"><thead><tr><th>gate</th><th>release gate</th><th>lead</th><th>supporting</th><th>closes when</th></tr></thead><tbody>%s</tbody></table>'
              % "".join("<tr><td>%s %s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (inline(m["gate"]), term(m["id"], "milestone-gate"), esc(m["releaseGate"]), hyp_links(re.findall(r"\bH-\d{2}\b", m["lead"])) if re.findall(r"\bH-\d{2}\b", m["lead"]) else esc(m["lead"]), inline(m["supporting"]), inline(m["closesWhen"])) for m in ms)) if ms else ""
    hypotheses = ('<section class="pg-view" id="v-hypotheses"><h1>Hypotheses</h1><p class="pg-lead">Seeded from the R&amp;D report; the lab keeps the status current. Tested = at least one experiment; Ready = runnable now; Blocked = waits on the named item; Waiting on you = waits on an owner answer.</p>'
                  '<div class="pg-split"><table class="pg-list"><thead><tr><th>hypothesis</th><th>kind</th><th>stream</th><th>status</th><th>experiments</th></tr></thead><tbody>%s</tbody></table>%s</div>%s'
                  '<p class="pg-small pg-muted">Columns in the detail: stream = the owner-supplied R&amp;D roadmap\'s S1-S4 with the heavy-queue class in brackets (Q 60 / T 25 / X 15); P/E = the lab\'s potential/effort and score; outside = the two owner-supplied documents\' rank and scores for the lead section, advisory only.</p></section>'
                  % (hrows, "".join(hyp_panel(h, h["id"] in owner_ids) for h in hyps), mtable))
    # ---- approach
    ch = data["charter"]
    approach = ['<section class="pg-view" id="v-approach"><h1>%s</h1><div class="pg-prose">%s</div>' % (inline(ch["title"]), md_to_html(ch["sections"].get("lead", "")))]
    for name, body in ch["sections"].items():
        if name != "lead":
            approach.append('<details class="pg-more"><summary>%s</summary><div class="pg-prose">%s</div></details>' % (inline(name), md_to_html(body)))
    approach.append('<details class="pg-more"><summary>The lab\'s tools (standard library, run with python3 -I -B)</summary><table class="ledger"><thead><tr><th>file</th><th>sha256</th><th>what it does</th></tr></thead><tbody>%s</tbody></table></details>'
                    % "".join('<tr><td><a href="%s">%s</a></td><td><code>%s</code></td><td>%s</td></tr>' % (esc(t["file"]), esc(t["file"]), t["digest"], inline(t["doc"])) for t in data["tools"]))
    if data.get("reads"):
        approach.append('<details class="pg-more"><summary>Progress by scope (the owner\'s reading view) and design reads</summary><table class="ledger"><thead><tr><th>file</th><th>sha256</th><th>title</th></tr></thead><tbody>%s</tbody></table></details>'
                        % "".join('<tr><td><a href="%s">%s</a></td><td><code>%s</code></td><td>%s</td></tr>' % (esc(r["file"]), esc(r["file"]), r["digest"], inline(r["title"])) for r in data["reads"]))
    approach.append('<details class="pg-more"><summary>How to read a verdict</summary><p class="pg-prose">Every RESULTS.json is a verdict ledger: claims, deterministic checks with the bound and the measured value, evidence by content digest, a claim verdict (SUPPORTED, CONTRADICTED, UNRESOLVED, NEW_VALUE_ESTABLISHED) and one status (PASS, FAIL, UNRESOLVED). A FAIL on a preregistered bound is recorded as a finding and never re-tuned under the same id; a restatement is a new id that names the first. Unresolved checks are listed by id so a reader can see what the verdict does not cover.</p></details>')
    approach.append('<h2 id="gloss">Glossary</h2><p class="pg-small pg-muted">The code families of this page; the same sentence shows on hover, on keyboard focus and on tap.</p><dl class="pg-gloss">%s</dl></section>'
                    % "".join("<dt>%s</dt><dd>%s</dd>" % (esc(f), esc(s)) for _, f, s in FAMILIES))
    # ---- history
    pre, entries = log_entries(lane_["body"]); total = len(entries) + len(log_entries((lane_.get("archive") or {}).get("body", ""))[1])
    snaps = "".join('<tr><td class="pg-name"><b>%s</b></td><td class="is-meta" data-label="Bridge"><code>%s</code></td><td class="is-meta" data-label="Lab">%s</td><td class="is-meta pg-num" data-label="Experiments">%d</td><td class="is-meta pg-num" data-label="Pass / fail / unresolved">%d / %d / %d</td><td class="is-meta pg-num" data-label="With experiment">%d / %d</td></tr>'
                    % (esc(s["generatedAt"]), esc(s["bridgeCommit"]), chip(s["lane"]), s["counts"]["experiments"], s["counts"]["verdicts"]["PASS"], s["counts"]["verdicts"]["FAIL"], s["counts"]["verdicts"]["UNRESOLVED"], s["counts"]["withExperiment"], s["counts"]["hypotheses"]) for s in reversed(history))
    history_v = ('<section class="pg-view" id="v-history"><h1>History</h1><p class="pg-lead">The snapshots of this page, newest first, and the lane file\'s resume log.</p>'
                 '<table class="pg-list"><thead><tr><th>generated</th><th>bridge</th><th>lab</th><th>experiments</th><th>pass / fail / unresolved</th><th>with experiment</th></tr></thead><tbody>%s</tbody></table>'
                 '<h2>Resume log</h2><p class="pg-small pg-muted">From the lane file\'s Resume here block (<code>%s</code>); <a href="resume-log.html">all %d entries</a> are on their own page.</p><details class="pg-more"><summary>The preamble and the ten newest entries</summary><div class="pg-prose">%s</div><ul class="log">%s</ul></details></section>'
                 % (snaps, lane_["digest"], total, md_to_html(pre), "".join("<li>%s</li>" % inline(t) for t in entries[:10])))
    # ---- frame
    tabs = '<nav class="pg-tabs" aria-label="Research views">%s</nav>' % "".join('<a href="#v-%s">%s</a>' % (k, n) for k, n in VIEWS)
    return frame("Research-Lab living page", sheet, sheet_digest, data["generatedAt"], tabs + start + experiments + hypotheses + "".join(approach) + history_v, page_css())


def one_line(e: dict) -> str:
    rep = e.get("report", {}).get("verdict", "")
    m = re.search(r"\*\*Verdict[^*]*\*\*\s*(.*)", rep, re.S)
    text = (m.group(1) if m else rep or e.get("registerLine", "")).replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    first = re.split(r"(?<=[.;])\s", text, 1)[0]
    return first[:260] + ("…" if len(first) > 260 else "")


def main() -> None:
    check, page_only = "--check" in sys.argv, "--page-only" in sys.argv
    sheet, sheet_digest = read_sheet()
    _, pending = read_glossary()
    if check or page_only:
        data = json.loads((RES / "research.json").read_text(encoding="utf-8"))
        history = json.loads((RES / "history.json").read_text(encoding="utf-8"))
    else:
        data = json.loads(json.dumps(build_record(), sort_keys=True))  # the key order research.json will hold, so this page equals what --check renders
        for name, text in progress_files(data).items():  # rule I: the reading view is written from the record, then its digests enter the record
            (RES / "progress" / name).write_text(text, encoding="utf-8")
        data["reads"] = reads()
        history = update_history(data, "--force-snapshot" in sys.argv)
        (RES / "research.json").write_text(json.dumps(data, indent=1, sort_keys=True), encoding="utf-8")
    page, log = render(data, history, sheet, sheet_digest), render_log(data, sheet, sheet_digest)
    if check:
        same = (RES / "research.html").read_bytes() == page.encode("utf-8") and (RES / "resume-log.html").read_bytes() == log.encode("utf-8")
        print("research.html + resume-log.html --check: %s (sheet %s; glossary rows pending %d)" % ("SAME" if same else "DIFFER", sheet_digest, len(pending)))
        stale = sorted(n for n, t in progress_files(data).items() if not (RES / "progress" / n).exists() or (RES / "progress" / n).read_text(encoding="utf-8") != t)
        print("progress --check: %s (%s)" % ("DIFFER" if stale else "SAME", ", ".join(stale) or "every generated file equals the record and the scope map"))
        sys.exit(0 if same and not stale else 1)
    (RES / "research.html").write_text(page, encoding="utf-8")
    (RES / "resume-log.html").write_text(log, encoding="utf-8")
    c = data["counts"]
    print("research.html written (%d bytes, sheet %s, glossary rows pending %d): %d experiments (%d completed), %d hypotheses (%d with experiment, %d ready, %d blocked), verdicts %s, lab %s, snapshots %d"
          % (len(page.encode("utf-8")), sheet_digest, len(pending), c["experiments"], c["completed"], c["hypotheses"], c["withExperiment"], c["ready"], c["blocked"], {v: c["verdicts"][v] for v in ("PASS", "FAIL", "UNRESOLVED")}, data["lane"]["status"], len(history)))


if __name__ == "__main__":
    main()
