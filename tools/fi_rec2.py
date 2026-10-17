# -*- coding: utf-8 -*-
import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
# record parse: try to interpret from offsets
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
recs=[d[offs[i]:offs[i+1]] for i in range(cnt-1)]
pat=re.compile(rb'[\x20-\x7e\x00]{4,}')
shown=0
for r in recs:
    ms=[]
    for m in pat.finditer(r):
        s=m.group().replace(b'\x00',b'')
        if len(s)>=3: ms.append(s.decode('ascii','replace'))
    if ms:
        print(len(r), '|', ' ; '.join(ms)[:140])
        shown+=1
    if shown>=30: break