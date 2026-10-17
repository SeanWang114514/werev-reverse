
import os, binascii
D = r"D:\VibeCoding\微信输入法逆向\samples\runtime"
def pr(b): 
    return sum(1 for c in b if 32<=c<127 or c in (9,10,13))/max(1,len(b))
for n in ["MM_SERVER_20261017.xlog","MM_WETYPE_20261017.xlog","MM_RENDER_20261017.xlog"]:
    b=open(os.path.join(D,n),"rb").read()
    print("===",n,len(b),"raw printable ratio %.3f"%pr(b[9:]))
    best=[]
    for key in range(256):
        s=bytes(x^key for x in b[9:9+4096]); best.append((pr(s),key))
    best.sort(reverse=True); print("  best xor keys:", [(round(r,3),hex(k)) for r,k in best[:5]])
    # xor with key+i
    for key in range(256):
        s=bytes((b[9+i]^((key+i)&0xff)) for i in range(min(4096,len(b)-9)))
        if pr(s)>0.9: print("  xor key+i key",hex(key),"ratio",round(pr(s),3), s[:60]); break
    # tail dump
    print("  tail:", binascii.hexlify(b[-64:]).decode())
