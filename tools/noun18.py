import sys, struct, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
c=collections.Counter()
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    L=len(r)
    if L<8: c[('short',L)]+=1; continue
    t=struct.unpack_from('<I',r,0)[0]
    body=r[4:]
    # pattern of body: bytes; check last 7 look like small ints
    tail=body[-7:] if len(body)>=7 else body
    c[(t, len(body))]+=1
print(c.most_common(12))
# print a full 60-byte record from idx 1000 with body split
r=d[offs[1000]:ends[1000]]
print('rec1000 len', len(r), r.hex())
t=struct.unpack_from('<I',r,0)[0]
print('t',t)