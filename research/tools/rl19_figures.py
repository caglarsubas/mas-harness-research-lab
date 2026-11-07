"""RL-19: the figures three owner-supplied syntheses attribute to five held papers, checked against the papers' own
text with a standard-library extractor (PDF text operators after zlib; HTML tags stripped). No network.
usage: python3 -I -B rl19_figures.py HELD_DIR CLAIMS_JSON OUT.json
Output: per claim FOUND or NOT_FOUND with the count of occurrences and up to 12 words of context around the first
occurrence (a short quotation, as the charter's grounding records keep); never the papers' text in full."""
import hashlib
import json
import pathlib
import re
import sys
import zlib

FILES = {"F2": "F2/paper.pdf", "F4a": "F4a/paper.pdf", "F4b": "F4b/paper.pdf", "F5": "F5/body.bin", "F6": "F6/paper.pdf"}


def pdf_text(data: bytes) -> str:
    out = []
    pos = 0
    while True:
        i = data.find(b"stream", pos)
        if i < 0: break
        j = data.find(b"endstream", i)
        if j < 0: break
        raw = data[i + 6:j].strip(b"\r\n")
        pos = j + 9
        try:
            dec = zlib.decompress(raw)
        except Exception:
            continue
        for tm in re.finditer(rb"\[((?:[^\]\\]|\\.)*)\]\s*TJ|\(((?:[^)\\]|\\.)*)\)\s*Tj", dec):
            if tm.group(1) is not None:
                parts = re.findall(rb"\(((?:[^)\\]|\\.)*)\)", tm.group(1))
                out.append(b"".join(parts).decode("latin-1", "replace"))
            else:
                out.append(tm.group(2).decode("latin-1", "replace"))
            out.append(" ")
        out.append("\n")
    t = "".join(out)
    return re.sub(r"\\\(|\\\)", "", t)


def html_text(data: bytes) -> str:
    t = data.decode("utf-8", "replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return re.sub(r"<[^>]+>", " ", t)


def norm(t: str) -> str:
    t = t.replace("−", "-").replace(" ", " ").replace(" ", " ")
    return re.sub(r"[ \t\r\n]+", " ", t)


def main(held, claims_path, out_path):
    held = pathlib.Path(held)
    texts, digests = {}, {}
    for tag, rel in FILES.items():
        data = (held / rel).read_bytes()
        digests[tag] = hashlib.sha256(data).hexdigest()
        texts[tag] = norm(html_text(data) if rel.endswith(".bin") else pdf_text(data))
    claims = json.load(open(claims_path, encoding="utf-8"))["claims"]
    results = []
    for c in claims:
        t = texts[c["paper"]]
        pat = c["pattern"]
        variants = [pat, pat.replace(",", ""), pat.replace("%", " %"), pat.replace("%", " percent")]
        found_at, n = -1, 0
        for v in variants:
            n += len(re.findall(re.escape(v), t, re.I))
            k = t.lower().find(v.lower())
            if k >= 0 and (found_at < 0 or k < found_at): found_at = k
        ctx = ""
        if found_at >= 0:
            words = t[max(0, found_at - 60): found_at + 60].split()
            ctx = " ".join(words[1:-1])[:120]
        results.append({"id": c["id"], "paper": c["paper"], "pattern": pat, "status": "FOUND" if found_at >= 0 else "NOT_FOUND", "occurrences": n, "context": ctx, "sources": c["sources"]})
    by_src = {}
    for r in results:
        for s in r["sources"]:
            d = by_src.setdefault(s, {"claims": 0, "found": 0}); d["claims"] += 1; d["found"] += r["status"] == "FOUND"
    by_paper = {}
    for r in results:
        d = by_paper.setdefault(r["paper"], {"claims": 0, "found": 0}); d["claims"] += 1; d["found"] += r["status"] == "FOUND"
    out = {"heldDigests": digests, "textChars": {k: len(v) for k, v in texts.items()}, "claims": len(results), "found": sum(r["status"] == "FOUND" for r in results),
           "bySource": by_src, "byPaper": by_paper, "results": results}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(json.dumps({k: out[k] for k in ("claims", "found", "bySource", "byPaper")}))
    print("not found:", [r["id"] for r in results if r["status"] == "NOT_FOUND"])


if __name__ == "__main__":
    main(*sys.argv[1:4])
