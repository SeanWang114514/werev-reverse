# -*- coding: utf-8 -*-
import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
pat=re.compile(rb'(?:[a-z]{1,12},){2,}[a-z]{1,12}')
runs=[]
i=0
while i<len(d):
    m=pat.match(d,i)
    if m:
        runs.append((i,m.group())); i=m.end()
    else: i+=1
print('pinyin runs', len(runs))
for off,s in runs[:12]: print(hex(off), s.decode())
for off,s in runs[-6:]: print(hex(off), s.decode())