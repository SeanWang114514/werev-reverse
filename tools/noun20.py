import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
# Look at regions where CJK might be encoded with a nibble scheme; test u16 values
cjkpairs=0
for k in range(0,2000):
    r=d[offs[k]:ends[k]]
    for i in range(0,len(r)-1,2):
        v=struct.unpack_from('<H',r,i)[0]
        if 0x4e00<=v<=0x9fff: cjkpairs+=1
print('u16 cjk pairs in first 2000 recs', cjkpairs)
# check whether any record contains 'noun' marker
print('noun marker', d.find(b'noun'))
print('CJK in header region 0x200-0xbcd00?', any(0x4e00<=struct.unpack_from('<H',d,i)[0]<=0x9fff for i in range(0x200, 0x4000, 2)))