import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
# find first record with length 18 and dump fully
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    if len(r)==18:
        print('idx', k, 'off', hex(offs[k]))
        print(r.hex())
        break
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    if len(r)==25:
        print('idx25', k, 'off', hex(offs[k]))
        print(r.hex())
        break