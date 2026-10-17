import sys, struct, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
c=collections.Counter()
firsts=collections.Counter()
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    if len(r)>=4: firsts[struct.unpack_from('<I',r,0)[0] if len(r)>=4 else -1]+=1
    l=len(r)
    c[l]+=1
print('len dist top', c.most_common(15))
print('first u32 top', firsts.most_common(10))
# print a few small recs hex
shown=0
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    if 6<=len(r)<=12:
        print(k, len(r), r.hex())
        shown+=1
    if shown>=15: break