#!/usr/bin/env python3
"""Render the living Research-Lab page.

usage: python3 -I -B research/build_research.py [--force-snapshot]   (run from the bridge root)

Reads research/README.md (the charter), research/hypotheses/REGISTER.md (the two tables), every
research/experiments/RL-nn/ folder (PREREG.md, RESULTS.json, REPORT.md, MAPPING.md, runs/*.md, data/*), the lab's
tools, research/reads/*.md (design reads and asks), the register's milestone rows, and handoff/LANE-RESEARCH-LAB.md's "Resume here" block; writes research/research.json (the data record with a
sha256 prefix per source file), appends a snapshot to research/history.json when the counts or verdicts changed, and
writes the self-contained research/research.html. Standard library only; no local path and no handle enters the page:
every link is relative to research/. The monitor's checkpoint carries the three files with research/**.
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
                exps.append({"id": c[0], "hypothesis": c[1], "folder": c[2], "state": c[3], "prereg": c[4]})
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
    return {"digest": digest(LANE), "header": header, "status": status, "body": body.strip()}


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


# ------------------------------------------------------------------------------------------------------- rendering --

CSS = """
:root { --bg:#f6f6f3; --surface:#ffffff; --text:#1d1e20; --muted:#62666d; --line:#e2e2dc; --accent:#2f5bd3; --code:#f0f0ea; --barbg:#ececE6;
  --PASS:#2d7a4b; --FAIL:#b3261e; --UNRESOLVED:#a85d00; --COMPLETED:#2d7a4b; --ONGOING:#2f5bd3; --PLANNED:#62666d; --READY:#0d7c74; --BLOCKED:#7c818a; --RUN:#2d7a4b; --PAUSED:#a85d00; --ACTIVE:#2d7a4b; color-scheme: light; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#131416; --surface:#1b1d20; --text:#e7e8ea; --muted:#a2a6ad; --line:#2c2f34; --accent:#86a8ff; --code:#25282c; --barbg:#2a2d31;
  --PASS:#6cc28c; --FAIL:#ff8a80; --UNRESOLVED:#f0a64a; --COMPLETED:#6cc28c; --ONGOING:#86a8ff; --PLANNED:#a2a6ad; --READY:#4fc7bb; --BLOCKED:#8f949c; --RUN:#6cc28c; --PAUSED:#f0a64a; --ACTIVE:#6cc28c; color-scheme: dark; } }
:root[data-theme="dark"] { --bg:#131416; --surface:#1b1d20; --text:#e7e8ea; --muted:#a2a6ad; --line:#2c2f34; --accent:#86a8ff; --code:#25282c; --barbg:#2a2d31; color-scheme: dark; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text); font:14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
main { max-width:1000px; margin:0 auto; padding:18px 16px 40px; }
h1 { font-size:20px; margin:0 0 2px; } h2 { font-size:15px; margin:26px 0 8px; } h3 { font-size:14px; margin:18px 0 6px; } h4, h5 { margin:12px 0 4px; font-size:13px; }
.sub { color:var(--muted); font-size:12.5px; margin-bottom:10px; } .sub a { color:var(--accent); }
.banner { background:var(--surface); border:1px solid var(--line); border-left:4px solid var(--PAUSED); border-radius:8px; padding:10px 12px; margin:10px 0 14px; }
.banner.active { border-left-color:var(--ACTIVE); } .banner span { font-size:11px; text-transform:uppercase; letter-spacing:.06em; font-weight:700; color:var(--PAUSED); }
.banner.active span { color:var(--ACTIVE); }
.summary { display:flex; flex-wrap:wrap; gap:6px; margin:8px 0 12px; }
.chip { display:inline-block; padding:1px 8px; border-radius:999px; font-size:11.5px; font-weight:600; white-space:nowrap; border:1px solid currentColor; }
.c-PASS, .c-COMPLETED, .c-RUN, .c-ACTIVE { color:var(--PASS); } .c-FAIL { color:var(--FAIL); } .c-UNRESOLVED, .c-PAUSED { color:var(--UNRESOLVED); }
.c-ONGOING { color:var(--ONGOING); } .c-READY { color:var(--READY); } .c-BLOCKED, .c-PLANNED, .c-NONE { color:var(--BLOCKED); }
.tabs { display:flex; flex-wrap:wrap; gap:4px; margin:10px 0 14px; border-bottom:1px solid var(--line); position:sticky; top:0; z-index:2; background:var(--bg); }
.tabs label { cursor:pointer; padding:6px 12px; font-size:13px; color:var(--muted); border:1px solid transparent; border-radius:8px 8px 0 0; margin-bottom:-1px; }
main > input[type=radio] { position:absolute; opacity:0; pointer-events:none; width:1px; height:1px; }
section.tab { display:none; }
#t-overview:checked ~ #tab-overview, #t-experiments:checked ~ #tab-experiments, #t-hypotheses:checked ~ #tab-hypotheses, #t-approach:checked ~ #tab-approach, #t-log:checked ~ #tab-log { display:block; }
#t-overview:checked ~ .tabs label[for=t-overview], #t-experiments:checked ~ .tabs label[for=t-experiments], #t-hypotheses:checked ~ .tabs label[for=t-hypotheses], #t-approach:checked ~ .tabs label[for=t-approach], #t-log:checked ~ .tabs label[for=t-log] { color:var(--accent); border-color:var(--line); border-bottom-color:var(--bg); background:var(--surface); }
.row { background:var(--surface); border:1px solid var(--line); border-radius:8px; margin-bottom:6px; }
.row[data-verdict=PASS] { border-left:4px solid var(--PASS); } .row[data-verdict=FAIL] { border-left:4px solid var(--FAIL); } .row[data-verdict=UNRESOLVED] { border-left:4px solid var(--UNRESOLVED); } .row[data-verdict=NONE] { border-left:4px solid var(--ONGOING); }
summary { list-style:none; cursor:pointer; padding:9px 12px; display:grid; grid-template-columns:64px 1fr 110px 110px; gap:10px; align-items:center; }
summary::-webkit-details-marker { display:none; } summary:hover { background:color-mix(in srgb, var(--accent) 5%, transparent); border-radius:8px; }
.head { display:grid; grid-template-columns:64px 1fr 110px 110px; gap:10px; font-size:11px; text-transform:uppercase; letter-spacing:.05em; color:var(--muted); padding:0 12px 4px; }
.id { font-weight:700; font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:12.5px; }
.meta { display:block; color:var(--muted); font-size:11.5px; margin-top:1px; }
.detail { border-top:1px solid var(--line); padding:4px 14px 14px 14px; } .detail p { margin:8px 0; }
.facts { display:flex; flex-wrap:wrap; gap:6px 18px; font-size:12.5px; color:var(--muted); margin:6px 0; } .facts b { color:var(--text); }
table.md, table.ledger { width:100%; border-collapse:collapse; font-size:12.5px; margin:6px 0 10px; }
table.md th, table.ledger th { text-align:left; font-size:11px; color:var(--muted); font-weight:600; border-bottom:1px solid var(--line); padding:4px 6px; }
table.md td, table.ledger td { border-bottom:1px solid var(--line); padding:5px 6px; vertical-align:top; }
code { font:12px ui-monospace, SFMono-Regular, Menlo, monospace; background:var(--code); padding:0 4px; border-radius:4px; }
.files a { color:var(--accent); text-decoration:none; margin-right:10px; font-size:12px; } .files code { font-size:11px; }
.bar { display:block; height:6px; background:var(--barbg); border-radius:3px; margin:3px 0 6px; overflow:hidden; display:flex; }
.bar i { display:block; height:100%; } .bar .PASS { background:var(--PASS); } .bar .FAIL { background:var(--FAIL); } .bar .UNRESOLVED { background:var(--UNRESOLVED); } .bar .NONE { background:var(--ONGOING); }
.grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:8px; margin:8px 0 14px; }
.card { background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:10px 12px; } .card b { font-size:18px; } .card .meta { margin-top:2px; }
ul { margin:4px 0; padding-left:18px; } li { margin:2px 0; }
.hyp td.st { white-space:nowrap; }
pre.resume { white-space:pre-wrap; background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:10px 12px; font:12px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace; }
@media (max-width: 640px) { summary, .head { grid-template-columns:56px 1fr; } summary > :nth-child(n+3), .head > :nth-child(n+3) { display:none; } }
"""


def chip(label: str, cls: str | None = None) -> str:
    return "<span class=\"chip c-%s\">%s</span>" % (esc(cls or label), esc(label))


def render(data: dict, history: list[dict]) -> str:
    c = data["counts"]; lane_ = data["lane"]; exps = data["experiments"]; hyps = data["register"]["hypotheses"]
    parts = []
    parts.append("<h1>%s</h1>" % esc(data["title"]))
    parts.append("<div class=\"sub\">Generated %s at bridge %s · register %s · charter %s · lane file %s · <a href=\"../roadmap/roadmap.html\">Living roadmap</a> · <a href=\"../roadmap/architecture.html\">Architecture map</a></div>"
                 % (esc(data["generatedAt"]), esc(data["bridgeCommit"]), data["register"]["digest"], data["charter"]["digest"], lane_["digest"]))
    parts.append("<div class=\"banner %s\"><span>Lab %s</span> &nbsp; %s</div>" % ("active" if lane_["status"] == "ACTIVE" else "", esc(lane_["status"]), esc(lane_["header"])))
    parts.append("<div class=\"summary\">%s</div>" % "".join([chip("%d hypotheses" % c["hypotheses"], "NONE"), chip("%d with an experiment" % c["withExperiment"], "RUN"), chip("%d ready, no experiment yet" % c["ready"], "READY"),
                                                              chip("%d blocked" % c["blocked"], "BLOCKED"), chip("%d experiments" % c["experiments"], "NONE"), chip("%d completed" % c["completed"], "COMPLETED"), chip("%d ongoing" % c["ongoing"], "ONGOING"),
                                                              chip("PASS %d" % c["verdicts"]["PASS"], "PASS"), chip("FAIL %d" % c["verdicts"]["FAIL"], "FAIL"), chip("UNRESOLVED %d" % c["verdicts"]["UNRESOLVED"], "UNRESOLVED"), chip("%d run records" % c["runs"], "NONE")]))
    # tabs
    parts.append("".join("<input type=\"radio\" name=\"tab\" id=\"t-%s\"%s>" % (t, " checked" if t == "overview" else "") for t in ("overview", "experiments", "hypotheses", "approach", "log")))
    parts.append("<nav class=\"tabs\">" + "".join("<label for=\"t-%s\">%s</label>" % (t, n) for t, n in (("overview", "Overview"), ("experiments", "Experiments"), ("hypotheses", "Hypothesis register"), ("approach", "Approach"), ("log", "Resume log and history"))) + "</nav>")
    # overview
    total = max(1, c["experiments"])
    bar = "".join("<i class=\"%s\" style=\"width:%.1f%%\"></i>" % (v, 100.0 * n / total) for v, n in list(c["verdicts"].items()) + [("NONE", c["ongoing"])] if n)
    ov = ["<section class=\"tab\" id=\"tab-overview\"><h2>Where the programme stands</h2>",
          "<div class=\"grid\">",
          "<div class=\"card\"><b>%d / %d</b><span class=\"meta\">hypotheses with at least one experiment</span></div>" % (c["withExperiment"], c["hypotheses"]),
          "<div class=\"card\"><b>%d</b><span class=\"meta\">experiments run; verdicts PASS %d · FAIL %d · UNRESOLVED %d</span><span class=\"bar\">%s</span></div>" % (c["completed"], c["verdicts"]["PASS"], c["verdicts"]["FAIL"], c["verdicts"]["UNRESOLVED"], bar),
          "<div class=\"card\"><b>%d</b><span class=\"meta\">hypotheses blocked on a named roadmap item or owner answer</span></div>" % c["blocked"],
          "<div class=\"card\"><b>%d</b><span class=\"meta\">ready hypotheses without an experiment yet</span></div>" % c["ready"],
          "</div>",
          "<h3>Every experiment in one line</h3><table class=\"ledger\"><thead><tr><th>id</th><th>hypothesis</th><th>state</th><th>verdict</th><th>one line</th></tr></thead><tbody>"]
    for e in exps:
        ov.append("<tr><td class=\"id\"><a href=\"#%s\" onclick=\"document.getElementById('t-experiments').checked=true\">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                  % (esc(e["id"]), esc(e["id"]), esc(", ".join(e["hypothesisIds"])), chip(e["state"]), chip(e["verdict"] or "pending", e["verdict"] or "NONE"), inline(one_line(e))))
    ov.append("</tbody></table>")
    ov.append("<h3>What waits, and on what</h3><ul>")
    for h in hyps:
        if h["bucket"] == "BLOCKED":
            ov.append("<li><b>%s</b> %s — <i>%s</i></li>" % (esc(h["id"]), inline(h["hypothesis"][:140] + ("…" if len(h["hypothesis"]) > 140 else "")), inline(h["status"])))
    ov.append("</ul><h3>Ready, no experiment yet</h3><ul>")
    for h in hyps:
        if h["bucket"] == "READY":
            ov.append("<li><b>%s</b> %s — first step: %s</li>" % (esc(h["id"]), inline(h["hypothesis"][:140] + ("…" if len(h["hypothesis"]) > 140 else "")), inline(h["firstStep"])))
    ov.append("</ul></section>")
    parts.extend(ov)
    # experiments
    ex = ["<section class=\"tab\" id=\"tab-experiments\"><h2>Experiments</h2><p class=\"sub\">Each folder holds PREREG (frozen before any run), run records, RESULTS in the verdict-ledger form and a one-page REPORT; links open the files relative to this page.</p>",
          "<div class=\"head\"><span>id</span><span>title</span><span>state</span><span>verdict</span></div>"]
    for e in exps:
        ex.append("<details class=\"row\" id=\"%s\" data-verdict=\"%s\"><summary><span class=\"id\">%s</span><span>%s<span class=\"meta\">%s</span></span><span>%s</span><span>%s</span></summary><div class=\"detail\">"
                  % (esc(e["id"]), esc(e["verdict"] or "NONE"), esc(e["id"]), inline(e.get("title", e["id"])), inline(e.get("registerLine", "")[:220]), chip(e["state"]), chip(e["verdict"] or "pending", e["verdict"] or "NONE")))
        ex.append("<div class=\"facts\"><span>hypotheses <b>%s</b></span><span>dates <b>%s</b></span><span>runs <b>%d</b></span><span>preregistration <b>%s</b></span></div>"
                  % (esc(", ".join(e["hypothesisIds"]) or "–"), esc(", ".join(e["dates"]) or "–"), len(e["runs"]), inline(e.get("preregStatus", "")[:300])))
        rep = e.get("report", {})
        for key, title in (("asked", "Asked"), ("measured", "Measured"), ("verdict", "Verdict"), ("context", "Context"), ("means", "What it means"), ("limits", "What it does not show"), ("note", "For the note"), ("proposal", "Proposal"), ("disclosure", "Disclosure")):
            if rep.get(key):
                ex.append("<h4>%s</h4>%s" % (title, md_to_html(rep[key])))
        if e["claims"]:
            ex.append("<h4>Claim verdicts (ledger %s%s)</h4><table class=\"ledger\"><thead><tr><th>claim</th><th>verdict</th><th>value</th></tr></thead><tbody>%s</tbody></table>"
                      % (esc(e.get("ledgerId", "")), (", supersedes " + esc(e["supersedes"][7:15])) if e.get("supersedes") else "",
                         "".join("<tr><td class=\"id\">%s</td><td>%s</td><td>%s</td></tr>" % (esc(cl["id"]), chip(cl["verdict"], {"SUPPORTED": "PASS", "CONTRADICTED": "FAIL", "UNRESOLVED": "UNRESOLVED", "NEW_VALUE_ESTABLISHED": "ONGOING"}.get(cl["verdict"], "NONE")), inline(cl["value"])) for cl in e["claims"])))
        if e["checks"]:
            ex.append("<details><summary style=\"display:block;padding:4px 0\"><b>Checks (%d)</b> — unresolved: %s</summary><table class=\"ledger\"><thead><tr><th>check</th><th>claim</th><th>outcome</th><th>established value</th></tr></thead><tbody>%s</tbody></table></details>"
                      % (len(e["checks"]), esc(", ".join(e["unresolved"]) or "none"), "".join("<tr><td class=\"id\">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (esc(ch["id"]), esc(ch["claim"]), chip(ch["outcome"], {"PASS": "PASS", "FAIL": "FAIL", "INCONCLUSIVE": "UNRESOLVED"}.get(ch["outcome"], "NONE")), inline(ch["value"])) for ch in e["checks"])))
        links = "".join("<a href=\"experiments/%s/%s\">%s <code>%s</code></a>" % (esc(e["id"]), esc(f), esc(f), d) for f, d in e["files"].items())
        links += "".join("<a href=\"experiments/%s/%s\">%s <code>%s</code></a>" % (esc(e["id"]), esc(r["file"]), esc(r["file"]), r["digest"]) for r in e["runs"])
        links += "".join("<a href=\"experiments/%s/%s\">%s <code>%s</code></a>" % (esc(e["id"]), esc(d["file"]), esc(d["file"]), d["digest"]) for d in e["data"])
        ex.append("<h4>Files (sha256 prefixes)</h4><div class=\"files\">%s</div></div></details>" % links)
    ex.append("</section>")
    parts.extend(ex)
    # hypotheses
    hy = ["<section class=\"tab\" id=\"tab-hypotheses\"><h2>Hypothesis register</h2><p class=\"sub\">Seeded from the R&amp;D report; the lab keeps the status column current. RUN = at least one experiment; READY = runnable now; BLOCKED = waits on the named item.</p>",
          "<table class=\"ledger hyp\"><thead><tr><th>id</th><th>hypothesis</th><th>kind</th><th>stream</th><th>P/E</th><th>status</th><th>experiments</th></tr></thead><tbody>"]
    for h in hyps:
        hy.append("<tr><td class=\"id\">%s</td><td>%s<span class=\"meta\">inputs: %s · first step: %s</span></td><td>%s</td><td>%s</td><td>%s<span class=\"meta\">outside: %s · %s</span></td><td class=\"st\">%s<span class=\"meta\">%s</span></td><td>%s</td></tr>"
                  % (esc(h["id"]), inline(h["hypothesis"]), inline(h["inputs"]), inline(h["firstStep"]), esc(h["kind"]), esc(h.get("stream", "")), esc(h.get("pe", "")), esc(h.get("outside1", "")), esc(h.get("outside2", "")), chip(h["bucket"]), inline(h["status"]), ", ".join("<a href=\"#%s\" onclick=\"document.getElementById('t-experiments').checked=true\">%s</a>" % (esc(x), esc(x)) for x in h["experiments"]) or "–"))
    hy.append("</tbody></table>")
    ms = data["register"].get("milestones", [])
    if ms:
        hy.append("<h3>Milestones (the four decision gates, tied to a lead hypothesis; a milestone closes on a verdict, not a date)</h3><table class=\"ledger\"><thead><tr><th>id</th><th>gate</th><th>release gate</th><th>lead</th><th>supporting</th><th>closes when</th></tr></thead><tbody>%s</tbody></table>"
                  % "".join("<tr><td class=\"id\">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (esc(m["id"]), inline(m["gate"]), esc(m["releaseGate"]), esc(m["lead"]), inline(m["supporting"]), inline(m["closesWhen"])) for m in ms))
    hy.append("<p class=\"sub\">Columns: stream = the owner-supplied R&amp;D roadmap's S1-S4 with the heavy-queue class in brackets (Q 60 / T 25 / X 15); P/E = the lab's potential/effort and score; outside = the two owner-supplied documents' rank and scores for the lead section, advisory only.</p></section>")
    parts.extend(hy)
    # approach
    ch = data["charter"]
    ap = ["<section class=\"tab\" id=\"tab-approach\"><h2>%s</h2>%s" % (inline(ch["title"]), md_to_html(ch["sections"].get("lead", "")))]
    for name, body in ch["sections"].items():
        if name != "lead":
            ap.append("<h3>%s</h3>%s" % (inline(name), md_to_html(body)))
    ap.append("<h3>The lab's tools (standard library, run with python3 -I -B)</h3><table class=\"ledger\"><thead><tr><th>file</th><th>sha256</th><th>what it does</th></tr></thead><tbody>%s</tbody></table>"
              % "".join("<tr><td class=\"id\"><a href=\"%s\">%s</a></td><td><code>%s</code></td><td>%s</td></tr>" % (esc(t["file"]), esc(t["file"]), t["digest"], inline(t["doc"])) for t in data["tools"]))
    if data.get("reads"):
        ap.append("<h3>Progress by scope (the owner's reading view) and design reads</h3><table class=\"ledger\"><thead><tr><th>file</th><th>sha256</th><th>title</th></tr></thead><tbody>%s</tbody></table>"
                  % "".join("<tr><td class=\"id\"><a href=\"%s\">%s</a></td><td><code>%s</code></td><td>%s</td></tr>" % (esc(r["file"]), esc(r["file"]), r["digest"], inline(r["title"])) for r in data["reads"]))
    ap.append("<h3>How to read a verdict</h3><p>Every RESULTS.json is a verdict ledger: claims, deterministic checks with the bound and the measured value, evidence by content digest, a claim verdict (SUPPORTED, CONTRADICTED, UNRESOLVED, NEW_VALUE_ESTABLISHED) and one status (PASS, FAIL, UNRESOLVED). A FAIL on a preregistered bound is recorded as a finding and never re-tuned under the same id; a restatement is a new id that names the first. Unresolved checks are listed by id so a reader can see what the verdict does not cover.</p></section>")
    parts.extend(ap)
    # log
    lg = ["<section class=\"tab\" id=\"tab-log\"><h2>Resume block (from the lane file, %s)</h2><pre class=\"resume\">%s</pre>" % (esc(lane_["header"]), esc(lane_["body"])),
          "<h2>Snapshot history</h2><table class=\"ledger\"><thead><tr><th>generated</th><th>bridge</th><th>lab</th><th>experiments</th><th>PASS / FAIL / UNRESOLVED</th><th>with experiment</th></tr></thead><tbody>"]
    for s in reversed(history):
        cc = s["counts"]
        lg.append("<tr><td>%s</td><td><code>%s</code></td><td>%s</td><td>%d</td><td>%d / %d / %d</td><td>%d / %d</td></tr>" % (esc(s["generatedAt"]), esc(s["bridgeCommit"]), chip(s["lane"]), cc["experiments"], cc["verdicts"]["PASS"], cc["verdicts"]["FAIL"], cc["verdicts"]["UNRESOLVED"], cc["withExperiment"], cc["hypotheses"]))
    lg.append("</tbody></table></section>")
    parts.extend(lg)
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>Research-Lab living page</title><style>%s</style></head><body><main>%s</main></body></html>"
            % (CSS, "\n".join(parts)))


def one_line(e: dict) -> str:
    rep = e.get("report", {}).get("verdict", "")
    m = re.search(r"\*\*Verdict[^*]*\*\*\s*(.*)", rep, re.S)
    text = (m.group(1) if m else rep or e.get("registerLine", "")).replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    first = re.split(r"(?<=[.;])\s", text, 1)[0]
    return first[:260] + ("…" if len(first) > 260 else "")


def main() -> None:
    data = build_record()
    history = update_history(data, "--force-snapshot" in sys.argv)
    (RES / "research.json").write_text(json.dumps(data, indent=1, sort_keys=True), encoding="utf-8")
    (RES / "research.html").write_text(render(data, history), encoding="utf-8")
    c = data["counts"]
    print("research.html written: %d experiments (%d completed), %d hypotheses (%d with experiment, %d ready, %d blocked), verdicts %s, lab %s, snapshots %d"
          % (c["experiments"], c["completed"], c["hypotheses"], c["withExperiment"], c["ready"], c["blocked"], c["verdicts"], data["lane"]["status"], len(history)))


if __name__ == "__main__":
    main()
