import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
out=open(sys.argv[2],'w',encoding='utf-8')
n=0
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    t=struct.unpack_from('<I',r,0)[0]
    if t==0:
        rest=r[4:]
        out.write(str(k)+chr(9)+'0'+chr(9)+'-'+chr(9)+rest.hex()+chr(10))
        n+=1; continue
    total=len(r)
    nent=(total-7)//8
    hashes=[r[4+8*i:8+8*i] for i in range(nent)]
    rest=r[4+8*nent:]
    out.write(str(k)+chr(9)+str(nent)+chr(9)+'|'.join(h.hex() for h in hashes)+chr(9)+rest.hex()+chr(10))
    n+=1
out.close()
print('rows', n)