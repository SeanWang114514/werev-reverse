# -*- coding: utf-8 -*-
import sys, struct, re, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
recs=[d[offs[i]:offs[i+1]] for i in range(cnt-1)]
print('records', len(recs), 'avg', sum(len(r) for r in recs)//max(1,len(recs)))
# utf8 cjk decode attempt
ok=0; tot=0
for r in recs[:20]:
    try:
        s=r.decode('utf-8')
    except Exception: continue
    cjk=[c for c in s if '\u4e00'<=c<='\u9fff']
    tot+=1
    if len(cjk)>=2: ok+=1; print('UTF8CJK', repr(s[:60]))
print('utf8 with cjk', ok, '/', tot)
# gbk cjk decode attempt
ok=0
for r in recs[:20]:
    s=r.decode('gbk','replace')
    cjk=[c for c in s if '\u4e00'<=c<='\u9fff']
    if len(cjk)>=2: ok+=1; print('GBKCJK', repr(s[:60]))
print('gbk with cjk', ok)