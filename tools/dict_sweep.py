# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
skip=int(sys.argv[2]) if len(sys.argv)>2 else 8192
d=open(p,'rb').read()
print('size',len(d))
for off in range(0, min(len(d), 200000), skip):
    chunk=d[off:off+skip]
    try:
        s=chunk.decode('gbk')
        cjk=sum(1 for c in s if '\u4e00'<=c<='\u9fff')
    except Exception:
        cjk=0
    print(hex(off), 'cjk=',cjk)
print('---tail---')
print(d[-2000:].hex()[:800])
