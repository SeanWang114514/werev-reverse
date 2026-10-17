# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
print('size', n)
for k in range(12):
    v=struct.unpack_from('<I',d,4*k)[0]
    print('u32[%d]=%d 0x%x' % (k,v,v))
# tail 64
print('tail', d[-64:].hex())
# sample around 0x251d00
print('mid', d[0x251d00:0x251d60].hex())