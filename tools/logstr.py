#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract embedded log-macro source paths and qualified function names from all samples."""
import re, sys, json
from pathlib import Path
from collections import defaultdict

def extract_ascii(blob, minlen=6):
    out = []
    cur = bytearray()
    for b in blob:
        if 32 <= b < 127:
            cur.append(b)
        else:
            if len(cur) >= minlen:
                out.append(cur.decode("ascii", "replace"))
            cur = bytearray()
    if len(cur) >= minlen:
        out.append(cur.decode("ascii", "replace"))
    return out

PATH_RX = re.compile(r"^[A-Za-z]:[\\/][!-~]{6,300}$")
FUNC_RX = re.compile(r"^(?:[A-Za-z_][A-Za-z0-9_]*::)+[~A-Za-z_][A-Za-z0-9_:<>~]*$")

def main():
    d = Path(sys.argv[1]); outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
    totals = {}
    for p in sorted(d.iterdir()):
        if not p.is_file(): continue
        blob = p.read_bytes()
        toks = set(extract_ascii(blob, 6))
        paths = sorted({t for t in toks if PATH_RX.match(t) and ("\\" in t or "/" in t)})
        funcs = sorted({t for t in toks if FUNC_RX.match(t) and "::" in t and len(t) < 260})
        (outdir / (p.name + ".paths.txt")).write_text("\n".join(paths), encoding="utf-8")
        (outdir / (p.name + ".funcs.txt")).write_text("\n".join(funcs), encoding="utf-8")
        totals[p.name] = {"paths": len(paths), "funcs": len(funcs)}
    print(json.dumps(totals, indent=1))

if __name__ == "__main__":
    main()
