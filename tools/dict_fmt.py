
import os, sys, json, hashlib, struct
ROOT = r"C:\Program Files\Tencent\WeType\2.1.4.6"
BI = os.path.join(ROOT, "BuildIn")
idx = json.load(open(os.path.join(BI,"index.json"), encoding="utf-8"))
items = idx
if isinstance(items, dict): items = items.get("list", [])
out = []
def u32s(b, off, n):
    return [struct.unpack_from("<I", b, off+4*i)[0] for i in range(n)]
def u64s(b, off, n):
    return [struct.unpack_from("<Q", b, off+8*i)[0] for i in range(n)]
for it in items:
    name = it.get("name")
    p = os.path.join(BI, name)
    if not os.path.exists(p): continue
    b = open(p,"rb").read()
    rec = {"name":name, "size":len(b), "md5ok": hashlib.md5(b).hexdigest()==it.get("md5"),
           "type":it.get("type"), "dict_type":it.get("dict_type"), "is_cell":it.get("is_cell"),
           "version":it.get("version"), "ts":it.get("timestamp"),
           "head32":b[:32].hex(), "u32_0_8":u32s(b,0,8), "u64_0_2":u64s(b,0,2)}
    # marker scan
    for m in (b"Ime trie header", b"TFL3", b"PK\x03\x04", b"huffman", b"mmkv", b"leveldb", b"LGBM", b"\x00\x00\x00\x00"):
        i = b.find(m)
        if i >= 0 and m != b"\x00\x00\x00\x00":
            rec.setdefault("markers", {})[m.decode("latin1")] = i
    # timestamp 0x56eaea00 family anywhere in first 256
    ts = b[:256].find(struct.pack("<I", 0x56eaea00))
    if ts>=0: rec["ts56eaea00_off"]=ts
    out.append(rec)
print(json.dumps(out, ensure_ascii=False, indent=1))
