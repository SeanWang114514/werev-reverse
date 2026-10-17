#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deep-dive WeType BuildIn dictionary container formats."""
import sys, struct, json, hashlib, re
from pathlib import Path

def hexdump(b, off=0, n=256):
    out = []
    for i in range(off, min(len(b), off+n), 16):
        chunk = b[i:i+16]
        hx = " ".join(f"{c:02x}" for c in chunk)
        asc = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
        out.append(f"  {i:06x}  {hx:<47}  {asc}")
    return "\n".join(out)

def scan_str(b, pat, limit=5, ctx=32):
    res = []
    for m in re.finditer(pat.encode(), b):
        res.append(m.start())
        if len(res) >= limit: break
    return res

def main():
    d = Path(sys.argv[1])
    names = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    for p in sorted(d.iterdir()):
        if p.suffix == ".json": continue
        if names and p.name not in names: continue
        b = p.read_bytes()
        print("="*100)
        print(f"FILE {p.name}  size={len(b)} (0x{len(b):x})")
        print(hexdump(b, 0, 160))
        # look for known markers
        for pat in ["Ime trie header", "TFL3", "PK\x03\x04", "zlib", "huffman", "word_huffman"]:
            offs = scan_str(b, pat, 3)
            if offs: print(f"  marker {pat!r} at {offs}")
        # candidate u32/u64 tables at start
        if len(b) >= 64:
            u32 = struct.unpack_from("<16I", b, 0)
            print("  u32[0:16] =", [f"{v}(0x{v:x})" for v in u32])
        print()

if __name__ == "__main__":
    main()
