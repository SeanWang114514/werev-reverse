import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
out=open(sys.argv[2],'w',encoding='utf-8')
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    if len(r)<8: continue
    t=struct.unpack_from('<I',r,0)[0]
    body=r[4:]
    h=body[:4*t]
    rest=body[4*t:]
    hashes=[h[i:i+4].hex() for i in range(0,len(h),4)]
    out.write(chr(9).join([str(k),str(t),','.join(hashes),rest.hex()])+chr(10))
out.close()
print('done')