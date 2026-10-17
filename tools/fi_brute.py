# -*- coding: utf-8 -*-
import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
def u16h(seg):
    if len(seg)%2: return None
    try: s=seg.decode('utf-16le')
    except Exception: return None
    cjk=sum(1 for c in s if '\u4e00'<=c<='\u9fff')
    return cjk
tot=0; hit=0; ex=[]
for k in range(cnt-1):
    r=d[offs[k]:offs[k+1]]
    for start in range(0, min(len(r),12)):
        for ln in range(4, min(len(r)-start,40)+1, 2):
            c=u16h(r[start:start+ln])
            if c is None: continue
            tot+=1
            if c>=2 and c*1.0>=(ln/2)*0.9:
                hit+=1
                if len(ex)<15: ex.append((k,start,ln, r[start:start+ln].decode('utf-16le')))
print('attempts', tot, 'hits', hit)
for e in ex: print(e)