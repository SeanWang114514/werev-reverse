#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a C++ class/namespace inventory from MSVC RTTI descriptors."""
import re, sys, json
from pathlib import Path
from collections import defaultdict, Counter

def split_msvc(inner):
    """Split an MSVC qualified name into components (handles ?$template@args)."""
    # top-level split on '@' not inside ?$ ... template nesting
    parts, cur, depth = [], [], 0
    i = 0
    while i < len(inner):
        ch = inner[i]
        if ch == "?" and i + 1 < len(inner) and inner[i+1] == "$":
            depth += 1
            cur.append("?$")
            i += 2
            continue
        if ch == "@":
            if depth > 0:
                depth -= 1
                cur.append("@")
            else:
                parts.append("".join(cur)); cur = []
            i += 1
            continue
        cur.append(ch); i += 1
    if cur:
        parts.append("".join(cur))
    return [p for p in parts if p]

def main():
    d = Path(sys.argv[1]); outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
    for f in sorted(d.glob("*.rtti.txt")):
        binname = f.name.replace(".rtti.txt", "")
        ns = defaultdict(list)
        for ln in f.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            inner = ln[4:] if ln.startswith(".?A") else ln
            comps = split_msvc(inner)
            if not comps:
                continue
            cls = comps[0]
            if cls.startswith("<lambda_"):
                continue
            namespace = "::".join(reversed(comps[1:])) if len(comps) > 1 else "(global)"
            ns[namespace].append(cls)
        lines = []
        total = 0
        for k in sorted(ns, key=lambda x: -len(ns[x])):
            cls = sorted(set(ns[k]))
            total += len(cls)
            lines.append(f"### {k}  ({len(cls)})")
            for c in cls:
                lines.append(f"    {c}")
        (outdir / f"{binname}.classes.txt").write_text("\n".join(lines), encoding="utf-8")
        print(f"{binname}: namespaces={len(ns)} classes={total}")
        # print top namespaces
        top = sorted(ns, key=lambda x: -len(ns[x]))[:12]
        for t in top:
            print(f"    {len(set(ns[t])):5d}  {t}")

if __name__ == "__main__":
    main()
