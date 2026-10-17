import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
rows=open(sys.argv[2],'w',encoding='utf-8')
n=0
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    L=len(r)
    if L<8: continue
    t=struct.unpack_from('<I',r,0)[0]
    body=r[4:]
    # per-token stride = 8 for t>=2 ? test: rec1 t=3 body21 -> 21-7=14 not div 8
    # try stride where body = t*8 + 7 -> t=3 => 31 no
    # alternate: body = t*(7)?? rec1 t=3 body 21 = 3*7 exactly!
    if len(body)%7==0 and len(body)//7==t:
        ents=[body[i*7:(i+1)*7] for i in range(t)]
        rows.write(chr(9).join([str(k),str(t),'7','|'.join(e.hex() for e in ents)])+chr(10))
        n+=1
rows.close()
print('7-byte-stride rows', n)