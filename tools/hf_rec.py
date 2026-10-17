# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
pat=bytes.fromhex('5001051162')
idx=[]; i=0
while True:
    j=d.find(pat,i)
    if j<0: break
    idx.append(j); i=j+1
print('count',len(idx))
# candidate: record = utf16 word (n chars) + 0x50 + 01 05 11 62 + freq bytes
for k in range(len(idx)-1):
    end=idx[k+1]-1
    seg=d[idx[k]+5:end]
    if len(seg)%2: seg=seg[:-1]
    try:
        s=seg.decode('utf-16le')
    except Exception:
        continue
    print(hex(idx[k]), len(seg), repr(s))