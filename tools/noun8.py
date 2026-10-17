import sys, struct, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
names=collections.Counter()
n=0
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    # pattern: [type u8][8B hash]*type, then 01 00 02 00 03 ... marker
    t=struct.unpack_from('<I',r,0)[0] & 0xfe
    body=r[4:]
    nent=len(body)//7 - 0
    pos=0
    ok=True
    ents=[]
    while pos+7<=len(body) and len(ents)<t:
        if body[pos+1:pos+3] in (b'\x01\x00',):
            # end of hash list
            break
        ents.append(body[pos:pos+8]); pos+=8
    txt=body[pos:]
    if 32<=t<=100: names[t]+=1
print('ok')
# instead: harvest raw ascii runs across file
runs=[]
i=0;L=len(d)
while i<L:
    if d[i]==0 and i+1<L and 0x20<=d[i+1]<0x7f:
        j=i+1; buf=bytearray()
        while j+1<L and 0x20<=d[j]<0x7f:
            buf.append(d[j]); j+=1
        if len(buf)>=3 and j<L and d[j]==0:
            runs.append((i,bytes(buf).decode()))
            i=j+1; continue
    i+=1
print('nul-delimited ascii', len(runs))
for o,s in runs[:60]: print(hex(o), s[:70])