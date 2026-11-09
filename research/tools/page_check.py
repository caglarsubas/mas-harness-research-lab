"""Page check (LAB-REPO-001): rebuilds the research page's data record in memory with build_research.py (the lane
reader replaced by a fixed stub) and compares it, minus generatedAt, lane and bridgeCommit, with the committed
research/research.json; every tool and read the record enumerates must be a manifest entry. Writes nothing; counts
only. Standard library.

usage: python3 -I -B research/tools/page_check.py MANIFEST_JSON   (exit 1 on any difference)
"""
import importlib.util
import json
import sys
from pathlib import Path

DROP = ("generatedAt", "lane", "bridgeCommit")


def load_builder(path: Path):
    spec = importlib.util.spec_from_file_location("research_page_builder", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list) -> int:
    if len(argv) != 1:
        print("usage: page_check.py MANIFEST_JSON")
        return 2
    manifest = Path(argv[0]).resolve()
    root = manifest.parent.parent
    research = root / "research"
    files = set(json.loads(manifest.read_text(encoding="utf-8"))["files"])
    builder = load_builder(research / "build_research.py")
    builder.lane = lambda: {"digest": "00000000", "header": "", "status": "", "body": ""}
    builder.bridge_commit = lambda: "none"
    built = builder.build_record()
    committed = json.loads((research / "research.json").read_text(encoding="utf-8"))
    for key in DROP:
        built.pop(key, None)
        committed.pop(key, None)
    problems = []
    keys = sorted(set(built) | set(committed))
    for key in keys:
        if built.get(key) != committed.get(key):
            problems.append("RECORD_DIFFERS:" + key)
    for tool in built.get("tools", []):
        if "research/" + tool["file"] not in files:
            problems.append("TOOL_UNLISTED:research/" + tool["file"])
    for read in built.get("reads", []):
        if "research/" + read["file"] not in files:
            problems.append("READ_UNLISTED:research/" + read["file"])
    if "research/research.json" not in files:
        problems.append("PAGE_UNLISTED:research/research.json")
    if problems:
        for line in problems:
            print(line)
        print("PAGE FAIL: %d problems" % len(problems))
        return 1
    print("PAGE OK: %d experiments, %d tools, %d reads, %d record keys"
          % (len(built.get("experiments", [])), len(built.get("tools", [])), len(built.get("reads", [])), len(keys)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
