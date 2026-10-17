import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
import re
# collect text region: 0x40e76f.. is likely id->text map
# find region with long utf-8 CJK runs
best=(0,0); i=0; L=len(d)
while i<L:
    b=d[i]
    if 0xe4<=b<=0xe9:
        j=i; good=0
        while j+2<L:
            b0=d[j]
            if 0xe0<=b0<=0xef and 0x80<=d[j+1]<=0xbf and 0x80<=d[j+2]<=0xbf:
                good+=1; j+=3
            else: break
        if good>=20:
            print('cjk run at', hex(i), 'chars', good, d[i:i+3*good].decode('utf-8','replace')[:60])
            i=j; continue
    i+=1