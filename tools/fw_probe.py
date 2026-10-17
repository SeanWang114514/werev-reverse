# -*- coding: utf-8 -*-
import sys, struct, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
print('size',len(d))
print('u32[0:8]', [struct.unpack_from('<I',d,4*i)[0] for i in range(8)])
print('u32[0:8] hex', [hex(struct.unpack_from('<I',d,4*i)[0]) for i in range(8)])
# scan for UTF-8 CJK triplets
res=[]
i=0
while i < len(d)-3:
    b=d[i]
    if 0xe4<=b<=0xe9:
        try:
            s=d[i:i+3].decode('utf-8')
            if len(s)==1 and '\u4e00'<=s<='\u9fff':
                res.append(i); i+=3; continue
        except Exception: pass
    i+=1
print('cjk chars', len(res))
for off in res[:20]:
    print(hex(off), d[off:off+30])