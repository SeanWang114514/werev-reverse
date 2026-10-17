# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
ref=d[offs[0]:offs[0]+8]
print('ref bytes', ref.hex())
hits=[]; start=0
while True:
    j=d.find(ref,start)
    if j<0: break
    hits.append(j); start=j+1
print('ref hits', len(hits), [hex(x) for x in hits[:20]])