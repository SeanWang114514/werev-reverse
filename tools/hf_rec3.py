# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
pat=bytes.fromhex('5001051162')
idx=[]; i=0
while True:
    j=d.find(pat,i)
    if j<0: break
    idx.append(j); i=j+1
for k in range(len(idx)-1):
    seg=d[idx[k]+5:idx[k+1]-1]
    s=seg.decode('gbk','replace')
    print(hex(idx[k]), repr(s))