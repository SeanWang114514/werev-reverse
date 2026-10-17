import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
# print tail region boundaries
print('last off', hex(offs[-1]), 'file', hex(len(d)))
print('tail hex', d[offs[-1]:offs[-1]+40].hex())
# offsets are into a data blob; check first off vs header size
print('header size guess', hex(offs[0]))
# Scan all records: after type + 8*type, look for 01 00 pattern then variable
import collections
cc=collections.Counter()
for k in range(0,3000):
    r=d[offs[k]:ends[k]]
    t=struct.unpack_from('<I',r,0)[0]
    rest=r[4+8*t:]
    cc[bytes(rest).hex()[:20]]+=1
print(cc.most_common(10))