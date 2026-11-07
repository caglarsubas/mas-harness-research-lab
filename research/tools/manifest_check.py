#!/usr/bin/env python3
"""Verify research/MANIFEST.json against the repository tree.

Usage: python3 -I -B research/tools/manifest_check.py research/MANIFEST.json

Refuses: a malformed manifest (schemaVersion, bridgeCommit 40 hex, files path -> 64 hex); a
listed file that is missing or whose sha256 differs; a file in the tree that is not listed
(`.git/**`, `.DS_Store` and the manifest itself excepted); any symlink; bytecode (`__pycache__`,
`*.pyc`); a `.github` directory. Exit 0 prints `MANIFEST OK: <n> files`.
"""
from __future__ import annotations

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
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def walk(root: Path, problems: list[str]) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root).as_posix()
        for name in list(dirnames):
            rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            if name in EXCLUDED_DIRS and rel_dir == ".":
                dirnames.remove(name)
                continue
            if name == ".github":
                problems.append(f"GITHUB_DIR_PRESENT: {rel}")
            if name == "__pycache__":
                problems.append(f"BYTECODE: {rel}")
            if Path(dirpath, name).is_symlink():
                problems.append(f"SYMLINK: {rel}")
                dirnames.remove(name)
        for name in filenames:
            path = Path(dirpath, name)
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                problems.append(f"SYMLINK: {rel}")
                continue
            if name.endswith(".pyc"):
                problems.append(f"BYTECODE: {rel}")
            if rel == MANIFEST_PATH or name in EXCLUDED_NAMES:
                continue
            found[rel] = path
    return found


def load_manifest(path: Path, problems: list[str]) -> dict[str, str]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        problems.append(f"MANIFEST_UNREADABLE: {error}")
        return {}
    if not isinstance(document, dict) or set(document) != {"schemaVersion", "bridgeCommit", "files"}:
        problems.append("MANIFEST_SHAPE: expected exactly schemaVersion, bridgeCommit, files")
        return {}
    if document["schemaVersion"] != SCHEMA_VERSION:
        problems.append(f"MANIFEST_SCHEMA: {document['schemaVersion']!r}")
    if not isinstance(document["bridgeCommit"], str) or not COMMIT_RE.match(document["bridgeCommit"]):
        problems.append("MANIFEST_BRIDGE_COMMIT: not 40 lowercase hex digits")
    files = document["files"]
    if not isinstance(files, dict):
        problems.append("MANIFEST_FILES: not an object")
        return {}
    for rel, digest in files.items():
        if not isinstance(rel, str) or rel.startswith("/") or ".." in rel.split("/"):
            problems.append(f"MANIFEST_PATH: {rel!r}")
        if not isinstance(digest, str) or not SHA_RE.match(digest):
            problems.append(f"MANIFEST_DIGEST: {rel}")
    return files


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    manifest = Path(argv[0]).resolve()
    root = manifest.parent.parent
    if manifest.relative_to(root).as_posix() != MANIFEST_PATH:
        print(f"manifest_check: the manifest must live at {MANIFEST_PATH}", file=sys.stderr)
        return 2
    problems: list[str] = []
    listed = load_manifest(manifest, problems)
    found = walk(root, problems)
    for rel in sorted(set(listed) - set(found)):
        problems.append(f"MISSING: {rel}")
    for rel in sorted(set(found) - set(listed)):
        problems.append(f"UNLISTED: {rel}")
    for rel in sorted(set(listed) & set(found)):
        actual = sha256_of(found[rel])
        if actual != listed[rel]:
            problems.append(f"CHANGED: {rel} {listed[rel][:8]} -> {actual[:8]}")
    if problems:
        for line in problems:
            print(line)
        print(f"MANIFEST FAIL: {len(problems)} problem(s)")
        return 1
    print(f"MANIFEST OK: {len(found)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
