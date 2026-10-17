import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
off=int(sys.argv[2],16)
ln=int(sys.argv[3])
d=open(p,'rb').read()
seg=d[off:off+ln]
print('hex', seg.hex())
print('u32', [hex(x) for x in struct.unpack_from('<%dI'%(len(seg)//4), seg, 0)])
print('ascii', ''.join(chr(b) if 32<=b<127 else '.' for b in seg))