# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
# header: u32[0]=0 u32[1]=0 u32[2]=ts u32[3]=111610 u32[4]=0 u32[5]=0
for i in range(0,40,4):
    print('u32[%d]=%d (0x%x)' % (i//4, struct.unpack_from('<I',d,i)[0], struct.unpack_from('<I',d,i)[0]))
print()
for i in range(6, 20):
    v=struct.unpack_from('<I',d,i*4)[0]
    print('u32[%d] = %d = 0x%x' % (i, v, v))