import sys, struct, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
print('cnt', cnt, 'last off', hex(offs[-1]))
import os
ends=offs[1:]+[len(d)]
# decode: rec = u32 token, then varint len, then utf8 text
words=[]
bad=0
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    if len(r)<5: bad+=1; continue
    tok=struct.unpack_from('<I',r,0)[0]
    pos=4
    # varint
    v=0; sh=0
    while pos<len(r):
        b=r[pos]; pos+=1
        v |= (b&0x7f)<<sh; sh+=7
        if not b&0x80: break
    txt=r[pos:pos+v]
    try:
        s=txt.decode('utf-8')
    except:
        bad+=1; continue
    words.append((k, tok, s))
print('ok', len(words), 'bad', bad)
for w in words[:80]: print(w)