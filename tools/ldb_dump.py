# -*- coding: utf-8 -*-
# LevelDB .ldb (SSTable) reader -> readable dump
import sys, struct, os, re, json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def varint(b, i):
    r = 0; s = 0
    while i < len(b):
        c = b[i]; i += 1
        r |= (c & 0x7f) << s
        if not (c & 0x80): return r, i
        s += 7
        if s > 63: break
    return None, i

def block_entries(block):
    if len(block) < 5: return []
    nrest = struct.unpack_from('<I', block, len(block)-4)[0]
    header_end = len(block) - 4 - 4*nrest
    if header_end < 0: return []
    entries = []; i = 0; key = b''
    while i < header_end:
        shared, i = varint(block, i)
        non_shared, i = varint(block, i)
        vlen, i = varint(block, i)
        if shared is None or non_shared is None or vlen is None: break
        key = key[:shared] + block[i:i+non_shared]; i += non_shared
        val = block[i:i+vlen]; i += vlen
        entries.append((key, val))
    return entries

def tkey(k):
    """æ½å user key / åé¨ key åç±»å"""
    if len(k) >= 8:
        seq = int.from_bytes(k[-8:-1], 'little')
        typ = k[-1]
        return k[:-8], seq, typ
    return k, 0, 0

def printable(b):
    return ''.join(chr(c) if (32 <= c < 127 or c >= 0xE0) else '.' for c in b)

def main():
    p = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'text'
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
    d = open(p,'rb').read()
    if len(d) < 48:
        print('too small'); return
    footer = d[-48:]
    magic = struct.unpack_from('<Q', footer, 40)[0]
    if magic != 0xdb4775248b80fb57:
        print('# WARNING footer magic mismatch: 0x%x' % magic)
    i = 0
    mo, i = varint(footer, i); ms, i = varint(footer, i)
    io_, i = varint(footer, i); is_, i = varint(footer, i)
    idx = block_entries(d[io_:io_+is_])
    recs = []
    for k, v in idx:
        j = 0
        off, j = varint(v, j); sz, j = varint(v, j)
        for key, val in block_entries(d[off:off+sz]):
            uk, seq, typ = tkey(key)
            payload = val[:-1] if len(val) >= 1 else b''
            comp = val[-1] if len(val) >= 1 else 0
            recs.append((uk, seq, typ, payload, comp))
    if mode == 'jsonl':
        out = []
        for uk, seq, typ, payload, comp in recs[:limit]:
            out.append({
                'key_hex': uk.hex(),
                'key_text': uk.decode('utf-8','replace'),
                'seq': seq, 'type': typ,
                'comp': comp,
                'val_hex': payload.hex(),
                'val_len': len(payload),
                'val_utf8': payload.decode('utf-8','replace'),
            })
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    print('# %s  size=%d  blocks=%d  records=%d' % (os.path.basename(p), len(d), len(idx), len(recs)))
    for uk, seq, typ, payload, comp in recs[:limit]:
        print('KEY %-6s %-70s | VAL(%d) %s' % (
            ('D' if typ == 0 else 'P'),
            printable(uk)[:70],
            len(payload),
            printable(payload)[:120]))

main()
