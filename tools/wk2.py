import sys, struct, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
c=collections.Counter()
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    c[len(r)]+=1
print('cnt',cnt,'lens',c.most_common(8))
print('rec0',d[offs[0]:ends[0]].hex())
print('rec1',d[offs[1]:ends[1]].hex()[:120])