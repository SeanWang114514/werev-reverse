#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan MSVC RTTI type descriptors (.?AV / .?AU) and export tables across samples."""
import re, sys, json
from pathlib import Path

def scan_rtti(blob):
    out = []
    for m in re.finditer(rb"\.\?A[VU][!-~]{2,400}?@@", blob):
        s = m.group(0)[:-2].decode("ascii", "replace")
        out.append(s)
    return out

def main():
    d = Path(sys.argv[1]); outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
    summary = {}
    for p in sorted(d.iterdir()):
        if not p.is_file():
            continue
        blob = p.read_bytes()
        rtti = sorted(set(scan_rtti(blob)))
        summary[p.name] = len(rtti)
        (outdir / (p.name + ".rtti.txt")).write_text("\n".join(rtti), encoding="utf-8")
    print(json.dumps(summary, indent=1))

if __name__ == "__main__":
    main()
