import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
def probe(seg):
    for s in range(0, min(len(seg),20)):
        b=seg[s:]
        if len(b)%2: b=b[:-1]
        try: t=b.decode('utf-16le')
        except Exception: continue
        cjk=sum(1 for c in t if '\u4e00'<=c<='\u9fff')
        if len(t)>=2 and cjk==len(t):
            return (s, t)
    return None
hits=[]
for k in range(cnt-1):
    r=probe(d[offs[k]:offs[k+1]])
    if r: hits.append((k,r))
print('records with pure-cjk utf16:', len(hits))
for k,(s,t) in hits[:30]: print(k, s, t)