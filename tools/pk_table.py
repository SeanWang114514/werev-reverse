
import pefile, struct, sys, io
sys.stdout.reconfigure(encoding='utf-8')
pe = pefile.PE(r"D:\werev\samples\wetype_tip_core.dll", fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
def rva(va): return va - base
def read(va, n):
    r = rva(va)
    return pe.get_data(r, n)
def cstr(va, maxn=120):
    if va == 0: return "<null>"
    try:
        d = read(va, maxn)
    except Exception as e:
        return "<bad %x>" % va
    z = d.find(b'\x00')
    if z < 0: z = len(d)
    return d[:z].decode('utf-8','replace')
# table start guess: 0x180363f50, stride 0x30
tbl = 0x180363f50
print("=== raw dump 0x%x .. +0x300 ===" % tbl)
d = read(tbl, 0x300)
for i in range(0, len(d), 16):
    row = d[i:i+16]
    print("%08x  %s  |  %s" % (tbl+i, ' '.join('%02x'%b for b in row),
        ' '.join(str(struct.unpack_from('<I', row, j)[0]) for j in (0,4,8,12))))
print()
print("=== interpreted entries (stride 0x30) ===")
for k in range(24):
    off = tbl + k*0x30
    try:
        p = struct.unpack('<Q', read(off, 8))[0]
        vk_mod = read(p, 8)
        vk, mod = struct.unpack('<II', vk_mod)
        namep = struct.unpack('<Q', read(off+0x10, 8))[0]
        act = struct.unpack('<I', read(off+0x18, 4))[0]
        mask = struct.unpack('<Q', read(off+0x28, 8))[0]
        print("%2d off=%08x p=%012x vk=0x%02x mod=0x%x act=%d mask=0x%x name=%s" % (
            k, off, p, vk, mod, act, mask, cstr(namep)))
    except Exception as e:
        print("%2d off=%08x ERR %s" % (k, off, e))
