# -*- coding: utf-8 -*-
import sys, struct, re, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
res=[]
i=len(d)-60
# walk backwards decoding length-prefixed utf8 records
print('tail hex', d[-24:].hex())
# forward walk from 0x251d40
pos=0x251d40
cnt=0
out=[]
while pos < len(d) and cnt < 40:
    ln=d[pos]
    if 1<=ln<=12:
        seg=d[pos+1:pos+1+ln]
        try:
            s=seg.decode('utf-8')
            out.append((hex(pos), s)); pos+=1+ln; cnt+=1; continue
        except Exception: pass
    pos+=1
for a,b in out: print(a, repr(b))