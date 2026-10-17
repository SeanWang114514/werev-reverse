# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
print('size', n)
print('first 32 u32', [struct.unpack_from('<I',d,4*i)[0] for i in range(32)])
# try: u32[1]=0x80000001 => magic; u32[2]=count
cnt=struct.unpack_from('<I',d,8)[0]
print('u32[2]=', cnt)
off = 12
lens=[struct.unpack_from('<I',d,off+4*i)[0] for i in range(min(cnt,12))]
print('lens first', lens)
# walk
pos=off+4*cnt
print('data start', hex(pos))
j=pos
for k in range(min(cnt,10)):
    ln=struct.unpack_from('<I',d,off+4*k)[0]
    seg=d[j:j+ln]; j+=ln
    try: print(k, ln, seg.decode('utf-16le'))
    except Exception: print(k, ln, seg.hex()[:60])