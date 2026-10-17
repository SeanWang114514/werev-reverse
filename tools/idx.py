#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract and filter Ghidra IndexDump output sections."""
import sys, re
from pathlib import Path

def sections(p):
    txt = Path(p).read_text(encoding="utf-8", errors="replace").splitlines()
    out, cur = {}, None
    for l in txt:
        if l.startswith("=== ") and l.endswith(" ==="):
            cur = l.strip("= ").strip(); out[cur] = []
        elif cur:
            out[cur].append(l)
    return out

if __name__ == "__main__":
    p = sys.argv[1]; sec = sys.argv[2]; pat = sys.argv[3] if len(sys.argv) > 3 else None
    lim = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    s = sections(p)
    key = [k for k in s if k.upper().startswith(sec.upper())][0]
    rx = re.compile(pat, re.I) if pat else None
    n = 0
    for l in s[key]:
        if rx and not rx.search(l):
            continue
        print(l); n += 1
        if n >= lim:
            break
    print(f"--- shown {n} of {len(s[key])} lines in [{key}] ---", file=sys.stderr)
