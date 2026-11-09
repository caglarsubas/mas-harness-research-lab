#!/usr/bin/env python3
"""Completeness check of the review-record data dictionary against a record schema or a folder of records.

Usage:
  python3 -I -B research/tools/review_record_dictionary_check.py DICTIONARY.json --schema review-record.schema.json [--schema review-identity.schema.json]
  python3 -I -B research/tools/review_record_dictionary_check.py DICTIONARY.json --records DIR

For every dictionary field it prints its candidate paths and whether each exists in a schema (by property path,
'identity.' prefixes map to the second schema) or is filled in the records (count of records with a non-empty
value). Derived and 'new' candidates are reported as such. Prints names and counts only, never record values.
Standard library only; read-only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def schema_paths(schema: dict, prefix: str = "") -> set[str]:
    out = set()
    props = schema.get("properties") or {}
    for k, v in props.items():
        out.add(prefix + k)
        if isinstance(v, dict):
            if v.get("type") == "object" or "properties" in v:
                out |= schema_paths(v, prefix + k + ".")
            items = v.get("items")
            if isinstance(items, dict):
                out |= schema_paths(items, prefix + k + "[].")
    return out


def record_filled(doc, path: str) -> bool:
    parts = path.replace("[]", "").split(".")
    cur = [doc]
    for part in parts:
        nxt = []
        for c in cur:
            if isinstance(c, dict) and part in c:
                v = c[part]
                nxt.extend(v if isinstance(v, list) else [v])
        cur = nxt
        if not cur:
            return False
    return any(v not in (None, "", [], {}) for v in cur)


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 2
    dictionary = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    schemas, records_dir = [], None
    i = 2
    while i < len(argv):
        if argv[i] == "--schema":
            schemas.append(Path(argv[i + 1])); i += 2
        elif argv[i] == "--records":
            records_dir = Path(argv[i + 1]); i += 2
        else:
            print("unknown argument: %s" % argv[i]); return 2
    paths_by_schema = [(s.name, schema_paths(json.loads(s.read_text(encoding="utf-8")))) for s in schemas]
    records = []
    if records_dir is not None:
        for p in sorted(records_dir.rglob("*.json")):
            try:
                records.append(json.loads(p.read_text(encoding="utf-8")))
            except ValueError:
                print("UNREADABLE: %s" % p.name)
    present = missing = derived = 0
    for f in dictionary["fields"]:
        status = []
        found_any = False
        for cand in f["candidates"]:
            if cand.startswith("derived") or cand.startswith("none in v2"):
                status.append("%s -> DERIVED_OR_NEW" % cand); derived += 1; continue
            if ":" in cand:
                status.append("%s -> OTHER_RECORD" % cand); continue
            key = cand.split(" (")[0]
            hit = []
            for name, paths in paths_by_schema:
                probe = key[len("identity."):] if key.startswith("identity.") and "identity" in name else key
                if probe in paths:
                    hit.append(name)
            if records:
                n = sum(1 for r in records if record_filled(r, key))
                status.append("%s -> filled in %d of %d records" % (key, n, len(records)))
                found_any = found_any or n > 0
            elif hit:
                status.append("%s -> in %s" % (key, ", ".join(hit))); found_any = True
            else:
                status.append("%s -> NOT_IN_SCHEMA" % key)
        if found_any:
            present += 1
        elif not any("DERIVED_OR_NEW" in s or "OTHER_RECORD" in s for s in status):
            missing += 1
        print("%s: %s" % (f["name"], "; ".join(status)))
    other = sum(1 for f in dictionary["fields"] if all(":" in c for c in f["candidates"]))
    print("DICTIONARY: %d fields; %d with a present candidate; %d in another record form; %d missing from the checked forms; %d derived-or-new candidates" % (
        len(dictionary["fields"]), present, other, missing, derived))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
