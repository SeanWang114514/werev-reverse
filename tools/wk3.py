import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
import collections
cc=collections.Counter()
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    i=0
    while i < len(r)-6:
        if r[i]==0x50 and r[i+1]==0x01 and r[i+2] in (2,3,4):
            ln=r[i+2]
            txt=r[i+3:i+3+ln]
            if all(0x30<=b<0x7f for b in txt):
                cc[txt.decode('ascii')]+=1
            i+=3+ln
        else: i+=1
print('distinct ascii tokens', len(cc))
print(cc.most_common(25))