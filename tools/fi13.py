import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
print('cnt',cnt)
for k in [22,33,44]:
    r=d[offs[k]:offs[k+1]]
    i=r.find(b'\x50\x01')
    if i<0: continue
    n=r[i+2]
    body=r[i+3:i+3+n]
    print(k, 'n=',n, 'hex', body.hex())
    print('  gbk', body.decode('gbk','replace'))
    print('  utf16', body.decode('utf-16le','replace'))