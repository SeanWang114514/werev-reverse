import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
rows=open(sys.argv[2],'w',encoding='utf-8')
seqs=0
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    if len(r)<8: continue
    t=struct.unpack_from('<I',r,0)[0]
    body=r[4:]
    if len(body)!=4*t+7: continue
    toks=[body[i:i+4].hex() for i in range(0,4*t,4)]
    rest=body[4*t:]
    # rest: pairs (i, tag) preceded by 01; assume rest = 01 + pairs + trailing
    if rest[0]!=1: continue
    pairs=[(rest[1+2*i],rest[2+2*i]) for i in range(t)]
    tail=rest[1+2*t:]
    rows.write(chr(9).join([str(k),str(t),','.join(toks),','.join('%d/%d'%p for p in pairs),tail.hex()])+chr(10))
    seqs+=1
rows.close()
print('word rows', seqs)