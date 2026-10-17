# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
items=[]
for k in range(cnt-1):
    r=d[offs[k]:offs[k+1]]
    i=0
    while i < len(r)-3:
        if r[i]==0x50 and r[i+1]==0x01 and 3<=r[i+2]<40:
            n=r[i+2]
            seg=r[i+3:i+3+n]
            py=seg.decode('ascii','replace')
            items.append(py)
            i+=3+n
        else: i+=1
print('pinyin groups', len(items))
for s in items[:60]: print(repr(s))