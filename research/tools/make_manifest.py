#!/usr/bin/env python3
"""Write research/MANIFEST.json: every file in the repository by sha256.

Usage: python3 -I -B research/tools/make_manifest.py --bridge-commit <40 hex> [--root DIR]

The manifest lists every regular file under the repository root except the manifest itself,
`.git/**` and Finder's `.DS_Store`, with paths relative to the root. A symlink anywhere is an
error. The schema is `planeon.research.manifest/v1`:
{"schemaVersion": ..., "bridgeCommit": <40 hex>, "files": {<path>: <sha256>}}.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

SCHEMA_VERSION = "planeon.research.manifest/v1"
MANIFEST_PATH = "research/MANIFEST.json"
EXCLUDED_DIRS = frozenset({".git"})
EXCLUDED_NAMES = frozenset({".DS_Store"})
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS)
        for name in sorted(filenames):
            path = Path(dirpath, name)
            rel = path.relative_to(root).as_posix()
            if rel == MANIFEST_PATH or name in EXCLUDED_NAMES:
                continue
            yield rel, path


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--bridge-commit", required=True, help="bridge commit the research tree was exported from")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    args = parser.parse_args(argv)
    if not COMMIT_RE.match(args.bridge_commit):
        print("make_manifest: --bridge-commit must be 40 lowercase hex digits", file=sys.stderr)
        return 2
    root = Path(args.root).resolve()
    files: dict[str, str] = {}
    for rel, path in iter_files(root):
        if path.is_symlink():
            print(f"make_manifest: symlink refused: {rel}", file=sys.stderr)
            return 1
        files[rel] = sha256_of(path)
    document = {"schemaVersion": SCHEMA_VERSION, "bridgeCommit": args.bridge_commit, "files": files}
    target = root / MANIFEST_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"MANIFEST WRITTEN: {len(files)} files -> {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
