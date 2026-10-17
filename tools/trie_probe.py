# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
print('size', len(d))
pos = d.find(b'Ime trie header')
print('hdr at', pos)
i = pos + len(b'Ime trie header') + 1
def rv(b,i):
    r=0;s=0
    while i<len(b):
        c=b[i];i+=1;r|=(c&0x7f)<<s
        if not c&0x80: return r,i
        s+=7
    return None,i
v,i = rv(d,i)
print('after-marker varint', v, 'at', i)
print('next 64 bytes', d[i:i+64].hex())
# interpret u32s after
print('u32 after', [hex(x) for x in struct.unpack_from('<8I', d, i)])
print('ascii window', d[i:i+200])
