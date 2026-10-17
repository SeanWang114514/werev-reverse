import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
r=d[offs[1]:offs[2]]
print('rec1 len', len(r))
i=0
while i<len(r):
    print('%02x %3d %r' % (r[i], r[i], chr(r[i]) if 32<=r[i]<127 else ''))
    i+=1