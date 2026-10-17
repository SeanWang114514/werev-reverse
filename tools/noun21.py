import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
# count char distribution over u16 values
import collections
c=collections.Counter()
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    for i in range(0,len(r)-1,2):
        v=struct.unpack_from('<H',r,i)[0]
        if 0x4e00<=v<=0x9fff: c[v]+=1
print('distinct cjk chars', len(c))
print('top', [(chr(v),n) for v,n in c.most_common(30)])