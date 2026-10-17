# -*- coding: utf-8 -*-
import sys, struct, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
back=struct.unpack_from('<I',d,offs[0]-4)[0]
print('count', cnt, 'offs[0]', offs[0], 'back ptr', back)
rec=d[offs[0]:offs[1]]
print('rec0 hex', rec.hex())