import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
cnt=struct.unpack_from('<I',d,0x0c)[0]
offs=[struct.unpack_from('<I',d,0x10+4*i)[0] for i in range(cnt)]
print('size',n,'records',cnt,'last off',offs[-1])
seg=d[offs[-1]:]
print('tail len', len(seg))
print('tail hex', seg[:80].hex())
for k in range(cnt-6, cnt-1):
    r=d[offs[k]:offs[k+1]]
    print(k, len(r), r.hex()[:120])