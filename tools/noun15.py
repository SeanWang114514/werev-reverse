import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
import collections
types=collections.Counter()
shape=collections.Counter()
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    t=struct.unpack_from('<I',r,0)[0]
    types[t]+=1
    shape[len(r)-4-8*t]+=1
print('types', types.most_common(10))
print('residual len', shape.most_common(10))