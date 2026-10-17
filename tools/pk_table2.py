
import pefile, struct, sys
sys.stdout.reconfigure(encoding='utf-8')
pe = pefile.PE(r"D:\werev\samples\wetype_tip_core.dll", fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
def rd(va,n):
    return pe.get_data(va-base,n)
def cstr(va,m=160):
    if not va: return "<0>"
    try: d=rd(va,m)
    except Exception: return "<bad>"
    z=d.find(b'\x00')
    return d[:z if z>=0 else len(d)].decode('utf-8','replace')
def wstr(va,m=160):
    if not va: return "<0>"
    try: d=rd(va,m)
    except Exception: return "<bad>"
    z=d.find(b'\x00\x00')
    if z%2: z+=1
    return d[:z if z>=0 else len(d)].decode('utf-16le','replace')
tbl=0x180363f50
print("=== entries stride 0x30 ===")
for k in range(6):
    off=tbl+k*0x30
    p=struct.unpack('<Q',rd(off,8))[0]
    a=struct.unpack('<I',rd(off+8,4))[0]
    b=struct.unpack('<I',rd(off+0xc,4))[0]
    q=struct.unpack('<Q',rd(off+0x10,8))[0]
    c=struct.unpack('<I',rd(off+0x18,4))[0]
    msk=struct.unpack('<Q',rd(off+0x28,8))[0]
    print("k=%d p=%x a=%d b=%d q=%x c=%d mask=0x%x"%(k,p,a,b,q,c,msk))
    print("    p-> %s"%" ".join("%02x"%x for x in rd(p,16)))
    print("    p-> as u32: %s"%[struct.unpack_from('<I',rd(p,8),j)[0] for j in (0,4)])
    print("    q-> ascii=%r utf16=%r"%(cstr(q,64),wstr(q,64)))
print()
print("=== all pointer targets in 0x180363ea8-0x180363f50 ===")
for va in range(0x180363ea8,0x180363f50,8):
    v=struct.unpack('<Q',rd(va,8))[0]
    if 0x180000000<v<0x180600000:
        print("%x -> %x  ascii=%r utf16=%r"%(va,v,cstr(v,48),wstr(v,48)))
    else:
        print("%x -> %x"%(va,v))
