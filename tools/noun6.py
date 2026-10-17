import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
# group by first u32
groups={}
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    f=struct.unpack_from('<I',r,0)[0]
    groups.setdefault(f,[]).append(r[4:])
for f in sorted(groups)[:10]:
    g=groups[f]
    print('=== first u32', f, 'count', len(g), 'len', len(g[0]))
    hexes=[x.hex() for x in g[:8]]
    print(hexes)
    print('raw[0]', g[0].hex())