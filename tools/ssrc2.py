import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
n=len(d)
h=d.find(b'Ime trie header')
print('marker at', h)
i=h+len(b'Ime trie header')+1
print('after marker bytes', d[i:i+24].hex())
# u32 at i, then N, then N u32 offsets
for start in range(i, i+12):
    N=struct.unpack_from('<I',d,start)[0]
    if 0<N<n//8:
        offs=[struct.unpack_from('<I',d,start+4+4*k)[0] for k in range(min(N,8))]
        print('start',hex(start),'N',N,'offs',offs)