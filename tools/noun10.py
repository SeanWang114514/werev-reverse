import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
out=open(sys.argv[2],'w',encoding='utf-8')
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
ends=offs[1:]+[len(d)]
tot=0; okc=0
for k in range(cnt):
    r=d[offs[k]:ends[k]]
    if len(r)<8: continue
    tot+=1
    # skip type u32 then t entries of 8 bytes
    t=struct.unpack_from('<I',r,0)[0]
    hashes=r[4:4+8*t]
    rest=r[4+8*t:]
    # rest: sequence of <u8> until sentinel; then trailing flags
    # try decode rest as utf-8
    s=None
    for trim in range(0, 9):
        cand=rest[:len(rest)-trim] if trim else rest
        try:
            s=cand.decode('utf-8')
            if s and all(0x4e00<=ord(c)<=0x9fff or c.isascii() or c in '·—' for c in s):
                break
            s=None
        except Exception: s=None
    if s:
        okc+=1
        out.write(str(k)+chr(9)+s+chr(10))
out.close()
print('recs', tot, 'decoded', okc)