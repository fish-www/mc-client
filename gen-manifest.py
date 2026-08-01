#!/usr/bin/env python3
"""Scan modpack/overrides/ and emit a JSON manifest of every file + sha1.

Output format mirrors modpack/server-manifest.json:
{
    "files": [
        { "path": "config/RuOK.toml", "hash": "826a2556..." },
        ...
    ]
}

Usage:
    python gen-manifest.py [overrides_dir] [output_file]
Defaults: overrides_dir=modpack/overrides  output_file=modpack/overrides-manifest.json
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha1(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    overrides = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "modpack", "overrides")
    output = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "modpack", "overrides-manifest.json")

    if not os.path.isdir(overrides):
        print(f"error: not a directory: {overrides}", file=sys.stderr)
        return 1

    files = []
    for root, dirs, names in os.walk(overrides):
        dirs.sort()
        for name in sorted(names):
            full = os.path.join(root, name)
            rel = os.path.relpath(full, overrides).replace(os.sep, "/")
            files.append({"path": rel, "hash": sha1(full)})

    files.sort(key=lambda e: e["path"])
    manifest = {"files": files}
    with open(output, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=4)
        f.write("\n")

    print(f"wrote {len(files)} files -> {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
