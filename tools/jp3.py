# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
# region right after header: 12 bytes
print('u32[0:3]', [struct.unpack_from('<I',d,4*i)[0] for i in range(3)])
print('u32[2]', struct.unpack_from('<I',d,8)[0])
print('bytes 0x0c..0x40', d[0x0c:0x40].hex())
print('    as u32', [struct.unpack_from('<I',d,0x0c+4*i)[0] for i in range(6)])