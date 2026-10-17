# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
for k in [5,6,7,12,13,18]:
    r=d[offs[k]:offs[k+1]]
    print(k, 'len', len(r))
    print('  hex', r.hex())