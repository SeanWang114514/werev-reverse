import sys, struct, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
c=collections.Counter()
c2=collections.Counter()
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    if len(r)>=30:
        c[r[26:-7].hex()]+=1
        c2[r[-7:].hex()]+=1
print('f26 pattern', c.most_common(8))
print('tail7', c2.most_common(8))
r=d[offs[0]:ends[0]]
print('sample rec', r.hex())