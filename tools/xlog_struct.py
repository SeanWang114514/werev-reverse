
import os, struct, binascii
D = r"D:\VibeCoding\微信输入法逆向\samples\runtime"
for n in ["MM_SERVER_20261017.xlog","MM_RENDER_20261017.xlog"]:
    b=open(os.path.join(D,n),"rb").read()
    print("===",n,len(b))
    pos=[i for i,c in enumerate(b) if c in (0x0A,0x0B,0x0C,0x0D)]
    print("  magic-ish count",len(pos),"first 40:",pos[:40])
    # deltas
    d=[pos[i+1]-pos[i] for i in range(min(30,len(pos)-1))]
    print("  deltas:",d)
    for p in pos[:12]:
        u32_1=struct.unpack_from("<I",b,p+1)[0] if p+5<=len(b) else -1
        u32_5=struct.unpack_from("<I",b,p+5)[0] if p+9<=len(b) else -1
        print("   @%d magic=%02x u32@+1=%d u32@+5=%d"%(p,b[p],u32_1,u32_5))
