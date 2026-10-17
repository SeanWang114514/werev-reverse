import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
for k in [0,1,2,3,4,5,10,100,1000]:
    r=d[offs[k]:ends[k]]
    print(k, len(r), r.hex())
print('--- region after offsets end', hex(8+4*cnt))
print(d[8+4*cnt:8+4*cnt+64].hex())