"""Privacy check (LAB-REPO-001): scans the manifest's file set plus README.md, LICENSE and the lab's own ci/ files for
absolute home-path shapes, e-mail shapes, the legacy term (by the published sha256 prefix of a seven-letter run) and
name tokens (by sha256 of substrings, table empty unless RESEARCH_NAME_DIGESTS names an unpublished local digest file).
The four transport copies in ci/ are pinned byte for byte to the platform by the Transport contract and are not
scanned here (Q-LAB-8). Counts only; no token is printed. Standard library.

usage: python3 -I -B research/tools/privacy_check.py MANIFEST_JSON   (exit 1 on any hit)
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

NAME_TOKEN_SHA256: dict = {}
LEGACY_TERM_PREFIX = "3367f5675f6a2486"
ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9_.~-])/(?:Users|home|private|root)/")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SEVEN = re.compile(r"(?<![a-z])[a-z]{7}(?![a-z])")
HEX64 = re.compile(r"^[0-9a-f]{64}(?![\s\S])")
EXTRA = ("README.md", "LICENSE")
PINNED_TRANSPORT = ("ci/verify-offline.sh", "ci/warm-source-isolation.sh", "ci/network_canary.py", "ci/run_packet_argv.py")


def load_name_tokens(path: str) -> int:
    global NAME_TOKEN_SHA256
    with open(path, "rb") as handle:
        doc = json.loads(handle.read())
    if not (isinstance(doc, dict) and all(isinstance(n, str) and re.fullmatch(r"[1-9][0-9]?", n) and isinstance(d, list)
                                          and d and all(isinstance(x, str) and HEX64.match(x) for x in d)
                                          for n, d in doc.items())):
        raise ValueError("name digest file shape")
    NAME_TOKEN_SHA256 = {int(n): tuple(d) for n, d in doc.items()}
    return sum(len(d) for d in doc.values())


def privacy_hits(raw: bytes) -> dict:
    text = raw.decode("utf-8", "replace")
    low = text.lower()
    names = 0
    for n, digests in NAME_TOKEN_SHA256.items():
        for i in range(len(low) - n + 1):
            if hashlib.sha256(low[i:i + n].encode("utf-8")).hexdigest() in digests:
                names += 1
    term = sum(1 for m in SEVEN.finditer(low)
               if hashlib.sha256(m.group(0).encode("utf-8")).hexdigest().startswith(LEGACY_TERM_PREFIX))
    return {"names": names, "legacyTerm": term, "absolutePaths": len(ABSOLUTE_PATH.findall(text)),
            "emails": len(EMAIL.findall(text))}


def main(argv: list) -> int:
    if len(argv) != 1:
        print("usage: privacy_check.py MANIFEST_JSON")
        return 2
    manifest = Path(argv[0]).resolve()
    root = manifest.parent.parent
    doc = json.loads(manifest.read_text(encoding="utf-8"))
    paths = [rel for rel in sorted(doc["files"]) if rel not in PINNED_TRANSPORT]
    paths.append(manifest.relative_to(root).as_posix())
    for name in EXTRA:
        if (root / name).is_file() and name not in paths:
            paths.append(name)
    ci = root / "ci"
    if ci.is_dir():
        for p in sorted(ci.rglob("*")):
            rel = p.relative_to(root).as_posix()
            if p.is_file() and rel not in paths and rel not in PINNED_TRANSPORT:
                paths.append(rel)
    digest_file = os.environ.get("RESEARCH_NAME_DIGESTS")
    loaded = load_name_tokens(digest_file) if digest_file else 0
    scanned, total, problems = 0, {"names": 0, "legacyTerm": 0, "absolutePaths": 0, "emails": 0}, []
    for rel in paths:
        path = root / rel
        if not path.is_file():
            problems.append("FILE_MISSING:" + rel)
            continue
        hits = privacy_hits(path.read_bytes())
        scanned += 1
        for key in total:
            total[key] += hits[key]
        if any(hits.values()):
            problems.append("HIT:%s names=%d legacyTerm=%d absolutePaths=%d emails=%d"
                            % (rel, hits["names"], hits["legacyTerm"], hits["absolutePaths"], hits["emails"]))
    if problems:
        for line in problems:
            print(line)
        print("PRIVACY FAIL: %d files, %d problems" % (scanned, len(problems)))
        return 1
    print("PRIVACY OK: %d files, 0 hits, %d name digests loaded" % (scanned, loaded))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
