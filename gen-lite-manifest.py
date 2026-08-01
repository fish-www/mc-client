#!/usr/bin/env python3
"""Generate modpack-lite/server-manifest.json from modpack/server-manifest.json.

Files whose path starts with an excluded prefix (e.g. .voxy/) are dropped from
the "files" array. Metadata (name/author/version/description/addons) is copied
from the source, except fileApi which is rewritten to the "-lite" endpoint.

Usage:
    python3 gen-lite-manifest.py [options]

Options:
    -x, --exclude PREFIX     path prefix to exclude (repeatable)
                             default: .voxy
    -o, --output PATH        output manifest (default: modpack-lite/server-manifest.json)
    --file-api URL           override fileApi (default: derived from source, .../modpack -> .../modpack-lite)
    --version V              override version (default: keep existing output's version if present)
    --description D          override description (default: keep existing output's description if present)
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

DEFAULT_EXCLUDES = (".voxy",)


def resolve(name: str, leaf: str) -> str:
    return os.path.join(HERE, name, leaf)


def excluded(path: str, prefixes) -> bool:
    for p in prefixes:
        if path == p or path.startswith(p + "/"):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-x", "--exclude", action="append", default=[],
                        help="path prefix to exclude (repeatable)")
    parser.add_argument("-o", "--output", default=resolve("modpack-lite", "server-manifest.json"))
    parser.add_argument("--file-api", help="override fileApi")
    parser.add_argument("--version", help="override version")
    parser.add_argument("--description", help="override description")
    args = parser.parse_args()

    source = resolve("modpack", "server-manifest.json")
    excludes = tuple(args.exclude) or DEFAULT_EXCLUDES

    with open(source, encoding="utf-8") as f:
        manifest = json.load(f)

    files = manifest.get("files", [])
    kept, removed_by_prefix = [], {}
    for entry in files:
        path = entry.get("path", "")
        hit = next((p for p in excludes if path == p or path.startswith(p + "/")), None)
        if hit:
            removed_by_prefix[hit] = removed_by_prefix.get(hit, 0) + 1
        else:
            kept.append(entry)

    kept.sort(key=lambda e: e.get("path", ""))
    manifest["files"] = kept

    # fileApi: point at the lite bucket by default
    if args.file_api:
        manifest["fileApi"] = args.file_api
    elif manifest.get("fileApi", "").endswith("/modpack"):
        manifest["fileApi"] = manifest["fileApi"][:-len("/modpack")] + "/modpack-lite"

    # version/description: keep whatever the previous lite manifest had, if any
    if args.version:
        manifest["version"] = args.version
    elif os.path.isfile(args.output):
        try:
            with open(args.output, encoding="utf-8") as f:
                old = json.load(f)
            manifest["version"] = old.get("version", manifest.get("version"))
            manifest["description"] = old.get("description", manifest.get("description"))
        except (json.JSONDecodeError, OSError):
            pass
    if args.description:
        manifest["description"] = args.description

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=4)
        f.write("\n")

    print(f"{source}: {len(files)} files -> {args.output}: {len(kept)} files")
    for p in excludes:
        n = removed_by_prefix.get(p, 0)
        if n:
            print(f"  excluded {p}/ : {n} files")
    print(f"  fileApi: {manifest['fileApi']}")
    print(f"  version: {manifest['version']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
