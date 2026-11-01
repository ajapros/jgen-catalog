#!/usr/bin/env python3
"""Validates catalog.json: schema, names, github: sources, optional tags/versions/blueprint."""
import json, re, sys

NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*$")
SOURCE = re.compile(r"github:[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9._-]+$")
SHA = re.compile(r"[0-9a-fA-F]{64}$")

def main(path):
    errors = []
    with open(path) as f:
        catalog = json.load(f)
    if catalog.get("schema") != "jgen.catalog/1":
        errors.append('schema must be "jgen.catalog/1"')
    blueprints = catalog.get("blueprints")
    if not isinstance(blueprints, dict):
        errors.append("blueprints must be an object")
        blueprints = {}
    for name, entry in blueprints.items():
        where = f"blueprints.{name}"
        if not NAME.match(name):
            errors.append(f"{where}: invalid name")
        if not isinstance(entry, dict):
            errors.append(f"{where}: must be an object"); continue
        if not SOURCE.match(str(entry.get("source", ""))):
            errors.append(f"{where}.source: must be github:owner/repo")
        if not isinstance(entry.get("description", ""), str) or not entry.get("description"):
            errors.append(f"{where}.description: required")
        if not isinstance(entry.get("tags", []), list):
            errors.append(f"{where}.tags: must be a list")
        for version, sha in (entry.get("versions") or {}).items():
            if not SHA.match(str(sha)):
                errors.append(f"{where}.versions.{version}: must be a 64-digit SHA-256")
        unknown = set(entry) - {"source", "description", "tags", "versions", "blueprint"}
        if unknown:
            errors.append(f"{where}: unknown keys {sorted(unknown)}")
    for e in errors:
        print("error:", e)
    print(f"{len(blueprints)} blueprint(s), {len(errors)} error(s)")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "catalog.json"))
