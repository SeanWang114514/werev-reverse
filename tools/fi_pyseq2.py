import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
py=re.compile(rb'[a-z]{1,10}(?:,[a-z]{1,10}){1,9}')
best=[]
for k in range(cnt-1):
    r=d[offs[k]:offs[k+1]]
    for m in py.finditer(r):
        best.append((m.start(), m.group().decode()))
print('total', len(best))
good=[s for s in best if len(s[1])>=6]
print('long', len(good))
for o,s in good[:40]: print(s)