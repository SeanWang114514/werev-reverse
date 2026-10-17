# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
print('count', cnt)
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
print('offsets first', offs[:8], 'last', offs[-4:])
print('file size', len(d))
c=[]
for i in range(cnt-1):
    seg=d[offs[i]:offs[i+1]]
    s=seg.decode('gbk','replace')
    c.append(s)
print('CJK ratio ok:', c[:20])