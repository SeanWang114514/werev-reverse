
import os, zstandard
D = r"D:\VibeCoding\微信输入法逆向\samples\runtime"
MAG=b"\x28\xb5\x2f\xfd"
def try_rep(b, off, L, magic=MAG):
    if off+L>len(b): return None
    key=bytes(b[off+j]^magic[j%4] for j in range(L))
    seg=bytes(b[off+i]^key[i%L] for i in range(0, min(len(b)-off, 300000)))
    try:
        d=zstandard.ZstdDecompressor()
        out=d.decompressobj().decompress(seg)
        if len(out)>16: return key,out
    except Exception: pass
    return None
for n in ["MM_SERVER_20261017.xlog","MM_WETYPE_20261017.xlog","MM_RENDER_20261017.xlog"]:
    b=open(os.path.join(D,n),"rb").read()
    print("===",n,len(b)); found=False
    for off in range(0, 300):
        for L in range(1,17):
            r=try_rep(b,off,L)
            if r:
                print("   HIT off",off,"L",L,"key",r[0].hex()); print("   ",r[1][:400]); found=True; break
        if found: break
    if not found: print("   no zstd hit")
