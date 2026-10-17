# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
toks=[]
for k in range(cnt-1):
    r=d[offs[k]:offs[k+1]]
    j=0
    while j < len(r)-4:
        if r[j]==0x50 and r[j+1]==0x01:
            n=r[j+2]
            body=r[j+3:j+3+n]
            if len(body)==n and n>=2:
                toks.append(body)
            j+=3+n
        else: j+=1
print('tokens', len(toks), 'total bytes', sum(len(t) for t in toks))
joined=b''.join(toks)
print('joined head', joined[:200].hex())
gb=joined.decode('gbk','replace')
print('gbk', gb[:200])
try:
    print('utf8', joined.decode('utf-8')[:200])
except Exception as e: print('utf8 fail', e)