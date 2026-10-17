import sys, struct, re, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
recs=[d[offs[i]:offs[i+1]] for i in range(cnt-1)]

def try_utf16(rec):
    out=[]
    n=len(rec)
    for s in range(n-1):
        # attempt aligned utf-16 run of ascii chars
        j=s; txt=''
        while j+1 < n:
            c=rec[j] | (rec[j+1]<<8)
            if 32 <= c < 127: txt+=chr(c); j+=2
            else: break
        if len(txt)>=3: out.append((s,txt))
    return out
for k,r in enumerate(recs):
    t=try_utf16(r)
    if t: print(k, t)