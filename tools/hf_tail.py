# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
# tail structure: guess records of variable len
# scan for the repeating pattern 50 01 05 11 62
pat=bytes.fromhex('5001051162')
idx=[]
i=0
while True:
    j=d.find(pat,i)
    if j<0: break
    idx.append(j); i=j+1
print('pattern count', len(idx))
if idx:
    print('first', hex(idx[0]), 'last', hex(idx[-1]))
    gaps=[idx[k+1]-idx[k] for k in range(len(idx)-1)]
    from collections import Counter
    print('gap hist', Counter(gaps).most_common(8))
    # decode between markers
    for k in idx[:25]:
        seg=d[k+5:k+5+24]
        try: print(hex(k), seg.decode('utf-8'))
        except Exception: print(hex(k), [hex(c) for c in seg])