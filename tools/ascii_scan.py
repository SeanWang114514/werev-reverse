# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p=sys.argv[1]
d=open(p,"rb").read()
n=int(sys.argv[2]) if len(sys.argv)>2 else 60
pat=re.compile(rb"(?:[\x20-\x7e]{2,})")
hits=[]
i=0
while i < len(d):
    m=pat.match(d,i)
    if m:
        s=m.group()
        if len(s)>=3: hits.append((i,s.decode()));
        i=m.end()
    else: i+=1
print("ascii hits", len(hits))
for off,s in hits[:n]:
    print(hex(off), s)