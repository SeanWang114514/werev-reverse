
import os, zlib, binascii, struct
D = r"D:\VibeCoding\微信输入法逆向\samples\runtime"
def try_all(b, label):
    hits=[]
    for off in range(0, min(len(b), 2048)):
        for key in ([0] if off==0 else range(0,256)):
            seg = b[off:off+256]
            if key: seg = bytes(x^key for x in seg)
            if seg[:1] not in (b"\x78", b"\x28", b"\x1f\x8b", b"\x5d"): 
                if key==0 and off==0: pass
            try:
                d=zlib.decompressobj()
                out=d.decompress(seg)
                if len(out)>=32:
                    hits.append((off,key,len(out),out[:80]))
                    if len(hits)>6: return hits
            except Exception: pass
    return hits
for n in ["MM_SERVER_20261017.xlog","MM_WETYPE_20261017.xlog","MM_RENDER_20261017.xlog"]:
    b=open(os.path.join(D,n),"rb").read()
    h=try_all(b,n)
    print("===",n,"hits",len(h))
    for off,key,ln,out in h: print("   off",off,"key",hex(key),"outlen",ln,out)
