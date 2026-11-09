"""Zero-bill scan (LAB-REPO-001): walks the checkout and refuses any file under .github/ (WORKFLOW_PRESENT), any
symbolic link (SYMLINK), any bytecode entry (BYTECODE) and, in text files outside research/, the hosted-runner tokens
(HOSTED_RUNNER). Exit 0 and no output when clean; one problem line per hit otherwise. Standard library.

usage: python3 -I -B ci/zero_bill_scan.py   (from the repository root)
"""
import os
import sys
from pathlib import Path

# The tokens are assembled at run time so this file does not hold them literally.
TOKENS = ("runs" + "-on", "actions" + "/", "uses" + ":")


def main() -> int:
    root = Path.cwd()
    problems = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        parts = rel_dir.parts
        if parts and parts[0] == ".git":
            dirnames[:] = []
            continue
        for name in list(dirnames):
            path = Path(dirpath) / name
            rel = (rel_dir / name).as_posix()
            if path.is_symlink():
                problems.append("SYMLINK:" + rel)
                dirnames.remove(name)
            elif name == "__pycache__":
                problems.append("BYTECODE:" + rel)
                dirnames.remove(name)
        for name in sorted(filenames):
            path = Path(dirpath) / name
            rel = (rel_dir / name).as_posix()
            if path.is_symlink():
                problems.append("SYMLINK:" + rel)
                continue
            if ".github" in (rel_dir / name).parts:
                problems.append("WORKFLOW_PRESENT:" + rel)
            if name.endswith(".pyc") or "__pycache__" in parts:
                problems.append("BYTECODE:" + rel)
            if not (parts and parts[0] == "research"):
                try:
                    text = path.read_bytes().decode("utf-8")
                except UnicodeDecodeError:
                    continue
                if any(token in text for token in TOKENS):
                    problems.append("HOSTED_RUNNER:" + rel)
    for line in problems:
        print(line)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
