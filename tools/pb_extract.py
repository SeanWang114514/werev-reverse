#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Locate serialized protobuf FileDescriptorProto blobs inside a PE and render .proto schemas."""
import sys, os, re, json
from pathlib import Path

def rd_varint(b, i):
    s = 0; r = 0
    while i < len(b):
        c = b[i]; r |= (c & 0x7F) << s; i += 1; s += 7
        if not (c & 0x80): return r, i
        if s > 63: raise ValueError("varint too long")
    raise ValueError("eof")

def parse_fields(b, i, end):
    """Yield (field_no, wire, value, start, next) greedily."""
    out = []
    while i < end:
        start = i
        try:
            tag, i = rd_varint(b, i)
        except Exception:
            break
        fno, wt = tag >> 3, tag & 7
        if fno == 0 or fno > 200 or wt in (3, 4, 6, 7):
            i = start; break
        if wt == 0:
            try: v, i = rd_varint(b, i)
            except Exception: i = start; break
            out.append((fno, wt, v, start, i))
        elif wt == 1:
            if i + 8 > end: i = start; break
            out.append((fno, wt, b[i:i+8], start, i+8)); i += 8
        elif wt == 5:
            if i + 4 > end: i = start; break
            out.append((fno, wt, b[i:i+4], start, i+4)); i += 4
        elif wt == 2:
            try: ln, j = rd_varint(b, i)
            except Exception: i = start; break
            if ln < 0 or j + ln > end: i = start; break
            out.append((fno, wt, b[j:j+ln], start, j+ln)); i = j + ln
    return out, i

NAME_RE = re.compile(rb"\x0a[\x01-\x7f]?[\x20-\x7e]{2,120}\.proto")

def scan(data):
    found = {}
    for m in NAME_RE.finditer(data):
        start = m.start()
        try:
            _, i = rd_varint(data, start + 1)
        except Exception:
            continue
        name = data[i:m.end()].decode("ascii", "replace")
        if not name.endswith(".proto"): continue
        # greedy parse forward up to 512KB
        end = min(len(data), start + 524288)
        fields, consumed = parse_fields(data, start, end)
        if not fields: continue
        # validate: field 1 must be the name string we found
        f1 = [f for f in fields if f[0] == 1]
        if not f1 or f1[0][2] != name.encode(): continue
        # require presence of field 4 (message_type) or 2 (package) or 5 (enum) or 6 (service)
        has = any(f[0] in (2, 4, 5, 6, 7, 8) for f in fields)
        if not has: continue
        blob = data[start:consumed]
        if name in found and len(found[name][1]) >= len(blob): continue
        found[name] = (start, blob)
    return found

def rlabel(n):
    return {1: "optional", 2: "required", 3: "repeated"}.get(n, "optional")
def rtype(n):
    T = {1:"double",2:"float",3:"int64",4:"uint64",5:"int32",6:"fixed64",7:"fixed32",8:"bool",9:"string",
         10:"group",11:"message",12:"bytes",13:"uint32",14:"enum",15:"sfixed32",16:"sfixed64",17:"sint32",18:"sint64"}
    return T.get(n, f"type{n}")

def render(blob):
    fields, _ = parse_fields(blob, 0, len(blob))
    def get(fn):
        return [f[2] for f in fields if f[0] == fn]
    name = get(1)[0].decode("utf-8", "replace")
    pkg  = get(2)[0].decode("utf-8", "replace") if get(2) else ""
    deps = [d.decode("utf-8","replace") for d in get(3)]
    syntax = ""
    for f in fields:
        if f[0] == 12 and f[1] == 2: syntax = f[2].decode("utf-8","replace")
    L = [f'// file: {name}  package: {pkg or "-"}  syntax: {syntax or "proto2"}  deps: {deps or "-"}']
    if pkg: L.append(f"package {pkg};")
    def emsg(mblob, indent):
        mf, _ = parse_fields(mblob, 0, len(mblob))
        g = lambda fn: [f[2] for f in mf if f[0] == fn]
        mname = g(1)[0].decode("utf-8","replace") if g(1) else "?"
        pad = "  " * indent
        L.append(f"{pad}message {mname} {{")
        for fblob in g(2):
            ff, _ = parse_fields(fblob, 0, len(fblob))
            h = lambda fn: [f[2] for f in ff if f[0] == fn]
            fname = h(1)[0].decode("utf-8","replace") if h(1) else "?"
            num = h(3)[0] if h(3) else 0
            lab = rlabel(h(4)[0]) if h(4) else "optional"
            ty = rtype(h(5)[0]) if h(5) else "?"
            tname = h(6)[0].decode("utf-8","replace") if h(6) else ""
            jt = h(10)[0].decode("utf-8","replace") if h(10) else ""
            L.append(f"{pad}  {lab} {ty}{'<' + (tname or jt) + '>' if (tname or jt) else ''} {fname} = {num};")
        for nblob in g(3):
            emsg(nblob, indent + 1)
        for eblob in g(4):
            ef, _ = parse_fields(eblob, 0, len(eblob))
            hh = lambda fn: [f[2] for f in ef if f[0] == fn]
            en = hh(1)[0].decode("utf-8","replace") if hh(1) else "?"
            L.append(f"{pad}  enum {en} {{")
            for vblob in hh(2):
                vf, _ = parse_fields(vblob, 0, len(vblob))
                vv = lambda fn: [f[2] for f in vf if f[0] == fn]
                vn = vv(1)[0].decode("utf-8","replace") if vv(1) else "?"
                vnum = vv(2)[0] if vv(2) else 0
                L.append(f"{pad}    {vn} = {vnum};")
            L.append(f"{pad}  }}")
        L.append(f"{pad}}}")
    for mblob in get(4): emsg(mblob, 0)
    for eblob in get(5):
        ef, _ = parse_fields(eblob, 0, len(eblob))
        hh = lambda fn: [f[2] for f in ef if f[0] == fn]
        en = hh(1)[0].decode("utf-8","replace") if hh(1) else "?"
        L.append(f"enum {en} {{")
        for vblob in hh(2):
            vf, _ = parse_fields(vblob, 0, len(vblob))
            vv = lambda fn: [f[2] for f in vf if f[0] == fn]
            L.append(f"  {vv(1)[0].decode('utf-8','replace') if vv(1) else '?'} = {vv(2)[0] if vv(2) else 0};")
        L.append("}")
    for sblob in get(6):
        sf, _ = parse_fields(sblob, 0, len(sblob))
        hh = lambda fn: [f[2] for f in sf if f[0] == fn]
        sn = hh(1)[0].decode("utf-8","replace") if hh(1) else "?"
        L.append(f"service {sn} {{")
        for mblob in hh(2):
            mf, _ = parse_fields(mblob, 0, len(mblob))
            mm = lambda fn: [f[2] for f in mf if f[0] == fn]
            mn = mm(1)[0].decode("utf-8","replace") if mm(1) else "?"
            it = mm(2)[0].decode("utf-8","replace") if mm(2) else ""
            ot = mm(3)[0].decode("utf-8","replace") if mm(3) else ""
            L.append(f"  rpc {mn} ({it}) returns ({ot});")
        L.append("}")
    return "\n".join(L)

def main():
    src = Path(sys.argv[1]); outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    found = scan(data)
    print(f"{src.name}: {len(found)} FileDescriptorProto blobs")
    idx = []
    for name, (off, blob) in sorted(found.items()):
        try:
            txt = render(blob)
        except Exception as e:
            txt = f"// render failed: {e}"
        safe = name.replace("/", "_")
        (outdir / safe).write_text(txt, encoding="utf-8")
        idx.append({"proto": name, "offset": hex(off), "bytes": len(blob)})
    (outdir / "_index.json").write_text(json.dumps(idx, indent=1), encoding="utf-8")

if __name__ == "__main__":
    main()
