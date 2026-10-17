# -*- coding: utf-8 -*-
import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
res=[]
for k in range(cnt-1):
    r=d[offs[k]:offs[k+1]]
    j=0
    while j < len(r)-3:
        if r[j]==0x50 and r[j+1]==0x01:
            n=r[j+2]
            body=r[j+3:j+3+n]
            if len(body)==n and n>=3:
                py=body.decode('utf-8','replace')
                res.append((k,py))
            j+=3+n
        else: j+=1
print('tokens', len(res))
for k,py in res[:40]: print(k, repr(py))