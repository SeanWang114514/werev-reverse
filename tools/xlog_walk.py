
import os, struct
D = r"D:\VibeCoding\微信输入法逆向\samples\runtime"
MAG={0x0A,0x0B,0x0C,0x0D}
def walk(b, lenOff, lenSize, hdr, trail):
    pos=0; ok=0; tot=0
    while pos < len(b)-1:
        if b[pos] not in MAG: return ok, pos
        if pos+lenOff+lenSize > len(b): return ok, pos
        if lenSize==2: L=struct.unpack_from("<H",b,pos+lenOff)[0]
        else: L=struct.unpack_from("<I",b,pos+lenOff)[0]
        nxt = pos+hdr+L+trail
        if nxt<=pos or nxt>len(b): return ok, pos
        ok+=1; pos=nxt
        if ok>60: return ok, pos
    return ok, pos
for n in ["MM_SERVER_20261017.xlog","MM_RENDER_20261017.xlog","MM_WETYPE_20261017.xlog"]:
    b=open(os.path.join(D,n),"rb").read()
    best=[]
    for lenOff in range(1,10):
        for lenSize in (2,4):
            for trail in (0,1):
                hdr=lenOff+lenSize
                ok,pos=walk(b,lenOff,lenSize,hdr,trail)
                if ok>=5: best.append((ok,lenOff,lenSize,hdr,trail,pos))
    best.sort(reverse=True)
    print("===",n,len(b))
    for x in best[:8]: print("   chain=%d lenOff=%d lenSize=%d hdr=%d trail=%d stop=%d"%x)
    if not best: print("   none")
