#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dump binary headers of WeType BuildIn dictionary files and detect container structure."""
import sys, struct, json, hashlib
from pathlib import Path

def hexdump(b, n=64):
    out = []
    for i in range(0, min(len(b), n), 16):
        chunk = b[i:i+16]
        hx = " ".join(f"{c:02x}" for c in chunk)
        asc = "".join(chr(c) if 32 <= c < 127 else "." for c in chunk)
        out.append(f"  {i:04x}  {hx:<47}  {asc}")
    return "\n".join(out)

def main():
    d = Path(sys.argv[1])
    idx = json.loads((d / "index.json").read_text(encoding="utf-8"))
    meta = {e["name"]: e for e in idx}
    print("name\tfile_size\tmd5_ok\ttype\tuniqueID\tversion\tdict_type\tfirst16_hex\tmagic_ascii")
    for p in sorted(d.iterdir()):
        if p.suffix == ".json": continue
        b = p.read_bytes()
        m = meta.get(p.name, {})
        md5 = hashlib.md5(b).hexdigest()
        ok = (md5 == m.get("md5"))
        magic = b[:16].hex()
        asc = "".join(chr(c) if 32 <= c < 127 else "." for c in b[:16])
        print(f"{p.name}\t{len(b)}\t{ok}\t{m.get('type')}\t{m.get('uniqueID')}\t{m.get('version')}\t{m.get('dict_type')}\t{magic}\t{asc}")
    print()
    for p in sorted(d.iterdir()):
        if p.suffix == ".json": continue
        b = p.read_bytes()
        print(f"===== {p.name} ({len(b)} bytes) =====")
        print(hexdump(b, 64))
        # try to find a leading length field
        if len(b) >= 8:
            v0, v1 = struct.unpack_from("<II", b, 0)
            print(f"  u32[0]={v0} (0x{v0:x})  u32[1]={v1} (0x{v1:x})  filesize={len(b)} (0x{len(b):x})")
        if len(b) >= 24:
            print("  u64[0..2] =", [struct.unpack_from("<Q", b, i*8)[0] for i in range(3)])
        print()

if __name__ == "__main__":
    main()
