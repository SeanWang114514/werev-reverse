import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
# Check type==3 record: len 21 -> body 17 = 12 hash + 5 rest
r=d[offs[3]:ends[3]]
print('rec3', r.hex(), 'len', len(r))
body=r[4:]
print('body len', len(body))
# see relation: t=3 -> 3 entries. 17 = ?
for ne in range(1,4):
    print('n',ne,'4n',4*ne,'rest',len(body)-4*ne)
# print rec4 (t=2) body
r4=d[offs[4]:ends[4]]
print('rec4', r4.hex(), len(r4), 'body', len(r4)-4)
r1=d[offs[1]:ends[1]]
print('rec1', r1.hex(), len(r1))